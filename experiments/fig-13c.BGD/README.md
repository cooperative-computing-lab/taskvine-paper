# Taskvine Using LibraryCalls to Run a Serverless Application (Batch Gradient Descent)

This experiment shows how TaskVine can use a task to install functions at a
worker -called Libraries- to which function calls can be made -called
FunctionCalls-. The initialization cost, e.g. that of a python interpreter, is
only paid by the Library installation.

The experiment is divided in two. First we will show a smaller run with a local
worker to make sure that everything is working correctly. Then we will show how
to run at scale to reproduce the results in the paper.

## To reproduce the figures in the paper, you can run:  

```sh
source ./activate-environment
./plot_bgd --mode tasks paper_results/c.bgd.transactions  c.bgd.tasks.pdf
./plot_bgd --mode workers paper_results/c.bgd.transactions  c.bgd.workers.pdf
```

## Small Run

For this experiment you will need two terminals on the same host. In the first
terminal we will execute the manager, and in the second a local worker. In **both**
terminals you will need to activate the conda environment:

```sh
source ./activate-environment
```

If you get an error, please make sure that you executed the `setup-taskvine`
script at the root directory of this repository.


### Executing The Manager (Time to run: ~5min)


In the first terminal run:

```sh
source ./activate-environment
python vine_run_bgd.py --tasks 20
```

This will execute a gradient descent workflow with 20 tasks. After the
submission messages, look for a message like this:


```text
TaskVine listening for workers on 9123
```
That will tell you which port to configure the workers. If you get an error such as:

```text
Exception: Could not create manager on port 9123
```

Rerun `vine_run_bgd.py` using the `--port XXXX` option, where `XXXX` is
some available port in your host. Alternatively, you can use `--port 0` to let
the manager pick a free port.


This workflow starts by creating the Library file and environment, which takes about 5
minutes. The workflow will not begin running until this is complete. Further
runs will reuse the Library environment created.

### Executing A Local Worker

In the second terminal start a single worker by running:

```sh
vine_worker -dall --cores 4 -t 900 localhost 9123
```

This creates a local worker with debug information printed to the terminal
(`-dall`), with 4 cores, and connecting to a manager running in the localhost
on port 9123. Replace the port number if you needed to change the default in
the previous step. We also tell the worker to shutdown after 900s (15min) of inactivity.

The worker will receive the Library and run all 20 tasks. Once this is
complete, the manager will output the set of weights with the least error. The
log file for this run will be present in
`vine-run-info/most-recent/vine-logs/transactions`

Note that if now you re-run the manager, the workflow should finish in less
than 30s as the environment for the FunctionCall's is already built and cached.


## Large Run (between 1 and 5min)

To reproduce the run presented in the paper you will need access to a batch
system that will let you run 200 2-core workers. Each batch job will run a
single worker such as:

```sh
source ./activate-environment

# 2 cores, 12 GB of memory and 12 GB of disk
vine_worker --cores 2 --memory 12000 --disk 12000 IP_OF_MANAGER PORT_OF_MANAGER
```

Alternatively, you can use the catalog server service provided by the
University of Notre Dame, and use:

```sh
source ./activate-environment

# 2 cores, 12 GB of memory and 12 GB of disk
vine_worker --cores 2 --memory 12000 --disk 12000 -M MANAGER_NAME
```

where `MANAGER_NAME` is by default `vine-bgd-$USER`. You can change this name
by running `vine_example_blast.py --name some-other-manager-name`.


We recommend first to run a short example before running with the full 200
workers. For this, simply re-run:

```sh
source ./activate-environment
python vine_run_bgd.py --tasks 20
```

and submit a single worker as appropriate for your batch system.

To execute the complete experiment, run:

```sh
python vine_run_bgd.py --params 100 --iterations 200000 --error 0.0000001 --rate 0.000005 --tasks 2000
```

The log	file for this run will be present in `vine-run-info/most-recent/vine-logs/transactions`.


### Example Of Submission File To HTCondor

If your HTCondor does not have special requirements, the generic script
provided may help you to submit the workers required, as:

```sh
source ./activate-environment
# 2 cores, 12 GB of memory and disk
../../utils/condor_vine_workers --cores 2 --memory 12000 --disk 12000 IP_OF_MANAGER PORT_OF_MANAGER 500
```

Or using names:

```sh
# 2 cores, 12 GB of memory and disk
../../utils/condor_vine_worker --cores 2 --memory 12000 --disk 12000 -M MANAGER_NAME 500
```


### Example of submission file for SLURM

For SLURM, check with your system administrators how many cores the compute
node have. For example, for nodes that have 64 cores, you can submit a single
worker as:

```sh
sbatch --job-name vine_worker --ntasks=1 --nodes=1  --cpus-per-task 64 --mem 0 --time 2:00:00 --account=ACCOUNT -- <<EOF
#!/bin/sh
source ./activate-environment
vine_worker --cores 64 -M vine-blast-$USER
EOF
```

Change the time and account arguments as appropriate for your site. To more
closely reproduce the results in the paper you will need to launch as many
workers as to get close to 2x500 = 1000 cores. (E.g., with 64-core workers, we
would between 15 and 16 workers).

## Plotting the results

By default, TaskVine writes its execution logs to the directory
`vine-run-info`. The logs of every run are kept in a directory named by the
start time of the manager. The `most-recent` directory is a link to logs of the
manager that executed last.

For plotting we are interested in the transactions log:


```sh
source ./activate-environment
vine_plot_txn_log --mode workers vine-run-info/most-recent/vine-logs/transactions worker.pdf
vine_plot_txn_log --mode tasks   vine-run-info/most-recent/vine-logs/transactions tasks.pdf
```


