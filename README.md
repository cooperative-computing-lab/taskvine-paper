[![DOI](https://zenodo.org/badge/613401833.svg)](https://zenodo.org/badge/latestdoi/613401833)


# TaskVine: Managing In-Cluster Data for High-Throughput Data Intensive Workflows

This repository describes how to setup a TaskVine installation to reproduce the
results in the paper submitted to Super Computing 2023.

Each experiment in the paper has its own directory in the directory
`experiments/`. The experiments are named after their corresponding figure
number and caption in the paper. For all the experiments we have included the
log files that generated the figures in the paper and describe how to generate
the figures from them. We also included instructions on how to reproduce the
results in the paper with two exceptions for the applications TopEFT and
Colmena. The data used by these applications is large and it is not not
publicly hosted. In these cases, we included smaller examples to show that
these applications work on top of TaskVine.

## Requirements

### Knowledge

- Familiarty with the Linux command line.
- Familiarty with submitting jobs to a batch system.

### Resources

- Linux, x86\_64 (amd64)
- 5GB of local disk for all but one experiment.
- 40GB of local disk for ColmenaXTB experiment.


## Setup (Time to run: 10min)

All the setup can be done in your `$HOME` directory, thus no admin privileges
are needed.

1. First, create the conda environment for TaskVine with the script
   `setup-taskvine`. This script will not modify anything outside the current
   directory. It will download the python package manager `conda` if it cannot
   find a local installation.

```sh
./setup-taskvine
```

2. For every terminal related to the experiments you will need to activate this
   environment:

```sh
source activate-environment
```


## Outline of Experiments

A TaskVine application consists of a vine manager process and several worker
processes. When ran at scale, TaskVine workers execute as batch jobs that
connect to the manager. For quick tests, manager and a handful of workers are
run on the same machine.

Experiments have the following outline:

1. Reproduction of figures in the paper from the logs included in this repository.
2. A small experiment that uses reduced input and local workers.
3. (Optional) If a cluster is available, a large run that mimics our setup for the paper.

We can provided detailed instructions for 1 and 2. For 3, submission across
batch systems greatly varies, thus we only provide examples on how to submit
jobs to generic HTCondor and SLURM clusters.


## Job Submission (Optional)

We provide the scripts `utils/condor_vine_worker` and `utils/slurm_vine_worker`
to ease submission of `vine_workers` to HTCondor and SLURM clusters. Note that
these scripts **most likely will need to be modified** to match your particular
site.


