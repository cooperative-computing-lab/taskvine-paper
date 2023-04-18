# Using topEFT to Compare TaskVine File Transfer Modes

This experiment shows how topEFT can take advantage of TaskVine facility to
leave the results of computations in place so that they can be reused by further
tasks.

As explained in [fig-13a.TopEFT](../fig-13a.TopEFT/), the full scale topEFT
experiments presented in the paper cannot be easily reproducible as the data is
not yet publicly available. Please refer to
[fig-13a.TopEFT](../fig-13a.TopEFT/) for an explanation on how to run a minimal
topEFT workflow.

## To reproduce the figures in the paper, you can run:

```sh
# activate environment to get access to vine_plot_txn_log
source ./activate-environment

vine_plot_txn_log --mode workers paper_results/a.shared-storage.transactions workers.pdf
vine_plot_txn_log --mode tasks paper_results/b.in-cluster-storage.transactions tasks.pdf
```

