# Shared Filesystem vs Worker Transfers

## Shared filesystem example

This experiment provides an example workflow that compares worker transfers to a shared filesystem (Panasas).
The workflow was deliberately designed to exploit a weakness in shared filesystems, which is rapid and concurrent metatada operations. For this
purpose, an arbitrary source of many small files was needed. The experiment shown in Figure 12 used the source repository of the python module matplotlib,
available at https://github.com/matplotlib/matplotlib/archive/refs/tags/v3.7.1.tar.gz. This contains approxiamately 4603 files.

vine\_example\_sharedfs.py simply dispatches 1000 tasks to perform a recursive directory listing
of a given path. The path is the first given argument to the program. This path should be the location in the shared filesystem
where each worker will perform its "ls -lR". The directory structure should be unpacked in the desired location before the manager
program is run.

To run this experiment, there must be a shared filesystem available with a unified path across all worker nodes.


## Worker transfer example

This experiment performs a comparable operation to the shared filesystem example. Worker to worker transfers are used to distribute the file to local node storage.
The directory structure is then unpacked, and a recursive directory listing is performed on the base directory of the worker.  

vine\_example\_peer\_compare.py downloads the matplotlib tarball and unpacks it at each worker. No manual file placement is needed before running this experiment. 

This experiment makes use of peer-to-peer transfers and therefore unimpeded 
communication between worker nodes is required. 

## Reproducing figure 12:

In both experiments, a 20 second wait is appended to each task. This is because the tasks by themselves are very short lived. Some tasks may finish before all 1000
are dispatched, and the manager may schedule a second task to run on one worker. The purpose of this experiment was to illustrate maximum concurrency, and maximize
the load on the shared filesystem. The 20 second wait provides enough time for the manager to dispatch all 1000 tasks to unique workers. 

This 20 second wait produces a graph with a distractingly long task execution time. To remedy this, the wait time was removed from each task for each experiment. This 
can be done using the included program plot\_txn\_remove\_delay instead of vine\_plot\_txn\_log.

```sh
vine_plot_txn_log --mode tasks --origin dispatched-first-task paper_results/sharedfs_transactions a.pdf
vine_plot_txn_log --mode tasks --origin dispatched-first-task paper_results/peer_transfer_transactions b.pdf
```

### Executing The Manager, Shared FS run (Time to run: ~2min)

In the terminal execute:

```sh
python vine_example_sharedfs.py /path/to/sharedfs/unpacked/files
```
See the section on HTCondor or SLURM to see about acquiring 1000 workers

### Executing The Manager, Shared FS run (Time to run: ~2min)

In the terminal execute:

```sh
python vine_example_peer_compare.py
```
See the section on HTCondor or SLURM to see about acquiring 1000 workers

### Example Of Submissions To HTCondor

If your HTCondor does not have special requirements, the generic script
provided may help you to submit the workers required, as:

```sh
# 1 cores, 12 GB of memory and disk
../../utils/condor_vine_workers --cores 1 --memory 12000 --disk 12000 IP_OF_MANAGER PORT_OF_MANAGER 1050
```

Or using names:

```sh
# 1 cores, 12 GB of memory and disk
../utils/condor_vine_worker --cores 1 --memory 12000 --disk 12000 -M MANAGER_NAME 1050
```


### Example of submission file for SLURM

SLURM nodes usually have many more cores than 1, thus we recommend running this
test with a reduced number of workers. E.g., to run with only 10 workers,
change the 500 in the command lines above to 100, and submit single workers to
the batch system with something like:

```sh
sbatch --job-name vine_worker  --ntasks=1 --nodes=100  --mem 0 --time 2:00:00 --account=ACCOUNT -- <<EOF
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

The alternative tool provided in the Figure 12 directory is previously discussed in reproducing the figures shown in the paper. The 
vine\_plot\_txn\_log tool will also illustrate the difference in experiments, however the task delay will be present in the execution time.




