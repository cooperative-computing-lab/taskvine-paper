# Transfer Methods In TaskVine

This experiment shows three different transfers modes of files in TaskVine:

- All workers fetching an input file from the same URL.
- Workers transferring the input file among themselves with a strict control from the manager.
- Workers transferring the input file among themselves with a loose control from the manager.

The experiment is divided in two. First we will show a smaller run with a local
worker to make sure that everything is working correctly. Then we will show how
to run at scale to reproduce the results in the paper.

This experiment makes use of peer-to-peer transfers and therefore unimpeded 
communication between worker nodes is required. 


## To reproduce the figures in the paper, you can run:  

```sh
vine_plot_txn_log --mode tasks --origin dispatched-first-task paper_results/a.worker-url.transactions  a.pdf
vine_plot_txn_log --mode tasks --origin dispatched-first-task paper_results/b.worker-to-worker-without-supervision.transactions b.pdf
vine_plot_txn_log --mode tasks --origin dispatched-first-task paper_results/c.worker-to-worker-limited-by-manager.transactions c.pdf
```

## Small Runs

For this experiment you will need three terminals on the same host. In the first
terminal we will execute the manager, and in the second and third we will
execute local workers. In the **three** terminals you will need to activate the
conda environment:

```sh
. ../../taskvine-env/bin/activate
```

If you get an error, please make sure that you executed the `setup-taskvine`
script at the root directory of this repository.

Note that for these runs are so small that the changes in transfers modes
cannot be detected.


### Executing The Manager, No Peer Transfers (Time to run: ~2min)

In the first terminal execute:

```sh
python manager.py --disable-peer-transfers
```

and in the second and third:

```sh
vine_worker -dall --cores 1 localhost 9123

```

This creates local workers with debug information printed to the terminal
(`-dall`), with 1 cores, and connecting to a manager running in the localhost
on port 9123. Replace the port number if you needed to change the default in
the previous step.


### Executing The Manager, Unlimited Worker-to-Worker transfers (Time to run: ~2min)

In the first terminal execute:

```sh
python manager.py --max-concurrent-transfers 9999
```

You may not need to relaunch the local workers if they have not timed-out.
Otherwise, follow the steps above to execute them.

### Executing The Manager, Limited Worker-to-Worker transfers (Time to run: ~2min)

In the first terminal execute:

```sh
# 3 is TaskVine's default when peer transfers are enabled
python manager.py --max-concurrent-transfers 3
```

As before, you may not need to relaunch the local workers if they have not
timed-out. Otherwise, follow the steps above to execute them.

Once the `python manager.py` finishes this last run, you can terminate the workers by
pressing control-c.


## Large Runs (Time to run:~3min)

To reproduce the run presented in the paper you will need access to a batch
system that will let you run 500 1-core workers. Each batch job will run a
single worker such as:

```sh
. ../../taskvine-env/bin/activate

# 1 cores, 12 GB of memory and disk
vine_worker --cores 1 --memory 12000 --disk 12000 IP_OF_MANAGER PORT_OF_MANAGER
```

Alternatively, you can use the catalog server service provided by the
University of Notre Dame, and use:

```sh
. ../../taskvine-env/bin/activate

# 1 cores, 12 GB of memory and disk
vine_worker --cores 1 --memory 12000 --disk 12000 -M MANAGER_NAME
```

Where `MANAGER_NAME` is by default `vine-transfers-$USER`. You can change this name
by running `python manager.py --name some-other-manager-name`.


To run the complete experiment, run in sequence:

```sh
python manager.py --worker-count 500 --disable-peer-transfers

python manager.py --worker-count 500 --max-concurrent-transfers 9999

python manager.py --worker-count 500 --max-concurrent-transfers 3
```

Submit 500 1-core workers to your batch system. Each run should finish in
about a minute once the batch system provides workers.


### Example Of Submissions To HTCondor

If your HTCondor does not have special requirements, the generic script
provided may help you to submit the workers required, as:

```sh
# 1 cores, 12 GB of memory and disk
../../utils/condor_vine_workers --cores 1 --memory 12000 --disk 12000 IP_OF_MANAGER PORT_OF_MANAGER 500
```

Or using names:

```sh
# 1 cores, 12 GB of memory and disk
../utils/condor_vine_worker --cores 1 --memory 12000 --disk 12000 -M MANAGER_NAME 500
```


### Example of submission file for SLURM

SLURM nodes usually have many more cores than 1, thus we recommend running this
test with a reduced number of workers. E.g., to run with only 10 workers,
change the 500 in the command lines above to 100, and submit single workers to
the batch system with something like:

```sh
sbatch --job-name vine_worker  --ntasks=1 --nodes=1  --mem 0 --time 2:00:00 --account=ACCOUNT -- <<EOF
#!/bin/sh
. ../../taskvine-env/activate
vine_worker --cores 64 -M vine-blast-$USER
EOF
```

Change the time and account arguments as appropriate for your site.


## Plotting the results

By default, TaskVine writes its execution logs to the directory
`vine-run-info`. The logs of every run are kept in a directory named by the
start time of the manager. The `most-recent` directory is a link to logs of the
manager that executed last.

For plotting we are interested in the transactions log:


```sh
vine_plot_txn_log --mode tasks --origin dispatched-first-task vine-run-info/most-recent/vine-logs/transactions output.pdf
```
