# Taskvine Cold And Hot Caches

This experiment shows how TaskVine populates caches at the workers so that
tasks and workflows can reuse already transfered data.

The experiment is divided in two. First we will show a smaller run with a local
worker to make sure that everything is working correctly. Then we will show how
to run at scale to reproduce the results in the paper.

## To reproduce the figures in the paper, you can run:  

```sh
utils/plot_txn_log_as_in_paper paper_results/a.cold-cache.transactions cold.pdf
utils/plot_txn_log_as_in_paper paper_results/b.hot-cache.transactions hot.pdf
```

## Small Run

For this experiment you will need two terminals on the same host. In the first
terminal we will execute the manager, and in the second a local worker. In **both**
terminals you will need to activate the conda environment:

```sh
conda activate $(realpath ../../taskvine-env)
```

If you get an error, please make sure that you executed the `setup-taskvine`
script at the root directory of this repository.

### Executing The Manager, Cold Cache Case. (Time to run: ~5min)

In the first terminal run:

```sh
python vine_example_blast.py
```

This will execute a bioinformatics workflow with 10 tasks. After the submission messages, look for a
message like this:

```text
TaskVine listening for workers on 9123
```

That will tell you which port to configure the workers. If you get an error such as:

```text
Exception: Could not create manager on port 9123
```

Rerun `vine_example_blast.py` using the `--port XXXX` option, where `XXXX` is
some available port in your host. Alternatevely, you can use `--port 0` to let
the manager pick a free port.

### Executing A Local Worker

In the second terminal run:

```sh
vine_worker -dall --cores 4 -b 30  localhost 9123
```

This creates a local worker with debug information printed to the terminal
(`-dall`), with 4 cores, and connecting to a manager running in the localhost
on port 9123. Replace the port number if you needed to change the default in
the previous step. When the worker cannot find the manager, it retries the
connection increasing the time waiting between the attempts; we can use the `-b 30`
to tell the worker never to wait more than 30s between attempts.

If everything goes well, the manager will report that all tasks were completed,
and the worker will disconnect. Do not terminate the worker yet! It is still
trying to work for a manager at the given address, with the difference that now
it has the data needed already cached.


### Executing The Manager, Hot Cache Case. (Time to run: ~2min)

Go back to to the first terminal and re-run the manager with:

```sh
python vine_example_blast.py
```

After some time, the worker will reconnect and start performing tasks for the
manager. This time the workflow should run much faster, as the worker already
has the data.

At this point you can terminate the worker by pressing control-c.


## Large Run (between 2 and 5min)

To reproduce the run presented in the paper you will need access to a batch
system that will let you run 100 4-core workers. Each batch job will run a
single worker such as:

```sh
# 4 cores, 12 GB of memory and disk
vine_worker --cores 4 --memory 12000 --disk 12000 IP_OF_MANAGER PORT_OF_MANAGER
```

Alternatevely, you can use the catalog server service provided by the
University of Notre Dame, and use:

```sh
# 4 cores, 12 GB of memory and disk
vine_worker --cores 4 --memory 12000 --disk 12000 -M MANAGER_NAME
```

where `MANAGER_NAME` is by default `vine-blast-$USER`. You can change this name
by running `vine_example_blast.py --name some-other-manager-name`.


We recommend first to run a short example before running with the full 100
workers. For this, simply re-run:

```sh
vine_example_blast.py
```

and submit a single worker as appropriate for your batch system.

To run the complete experiment, run:

```sh
vine_example_blast.py --task-count 1000
```

and submit 100 workers. The run with cold cache should complete in 5min once the batch system schedules the workers.

Once the run finishes, re-run it to test the hot cache. It should run in about 2min.



### Example Of Submission File To HTCondor

The file `condor.submit` show how to submit a worker to a generic HTCondor
pool. Modify the `arguments` line to match the name or IP address of your
manager. To request 100 workers, change `queue 1` to `queue 100`.

And then run:

```sh
condor_submit condor.submit
```

### Example of submission file for SLURM

For SLURM, check with your system administrators how many cores the compute
node have. For example, for nodes that have 64 cores, you can submit a single
worker as:

```sh
sbatch --job-name vine_worker --ntasks=1 --nodes=1  --cpus-per-task 64 --mem 0 --time 2:00:00 --account=ACCOUNT -- <<EOF
#!/bin/sh
vine_worker --cores 64 -M vine-blast-$USER
EOF
```

Change the time and account arguments as apropriate for your site. To more
closely reproduce the results in the paper you will need to launch as many
workers as to get close to 4x100 = 400 cores. (E.g., with 64-core workers, we
would between 6 and 7 workers).

## Plotting the results

By default, TaskVine writes its execution logs to the directory
`vine-run-info`. The logs of every run are kept in a directory named by the
start time of the manager. The `most-recent` directory is a link to logs of the
manager that executed last.

For plotting we are interested in the transactions log:


```sh
vine_plot_txn_log vine-run-info/most-recent/vine-logs/transactions output.pdf
```

