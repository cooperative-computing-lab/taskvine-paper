# Taskvine Executing a High Energy Physics Workflow

This experiment shows how TaskVine can be used to run topEFT, which is high
enerygy physics workflow. The data needed to run the workflow presented in the
paper is not publicly available, thus here we only show how to setup topEFT and
make a run with minimal local data.


## To reproduce the figures in the paper, you can run:

```sh
# activate environment to get access to vine_plot_txn_log
source ./activate-environment

vine_plot_txn_log --mode workers paper_results/a.topeft.transactions workers.pdf
vine_plot_txn_log --mode tasks paper_results/a.topeft.transactions tasks.pdf
```

## Setting Up TopEFT

TopEFT itself is built on top of Coffea, which is a python framework to write
high energy physics analysis. We modified TopEFT and Coffea to add TaskVine as
an executor, since these changes have not yet been merged upstream, we need to
install them from our github repositories. This installation was already
performed as part of the TaskVine setup in the `taskvine-env` directory.

### Download the data

To run this experiment, you need to download a data file with collision events.
This file is 151 MB:

```sh
(mkdir -p topeft_data && cd topeft_data && curl -C - -L -O https://zenodo.org/record/7838574/files/ttHJet_UL17_R1B14_NAOD-00000_10194_NDSkim.root)
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


### Executing The Manager


In the first terminal run:

```sh
python topeft_run.py cfgs/UL17_private_ttH_for_CI.json -s 2500
```

This will execute a small topEFT workflow using the local file we just
downloaded in which each processing tasks consists of 2500 particle collision
events.

NOTE: One of the libraries used in topEFT hijacks the terminal cursor. Thus,
when the workflow terminates you will have to type `reset` to get it back.

By default topEFT picks any available port, but you can pick an explicit one
with the `--port` option.


### Executing A Local Worker

In the second terminal start a single worker by running:

```sh
vine_worker -dall --cores 4 -t 900 localhost 9123
```

This creates a local worker with debug information printed to the terminal
(`-dall`), with 4 cores, and connecting to a manager running in the localhost
on port 9123. Replace the port number if you needed to change the default in
the previous step. We also tell the worker to shutdown after 900s (15min) of
inactivity.


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

