# ColmenaXTB Using TaskVine as an Executor

ColmenaXTB requires a more specialized setup, together with a larger disk
storage requirement to host the input data. We have prepared a separate DOI
with the instructions on how to reproduce our results with ColmenaXTB: [https://doi.org/10.5281/zenodo.7823513]()

From [https://doi.org/10.5281/zenodo.7823513]() download the `colmena-exp.tar.gz` 
tarball to the local machine, untar it, and follow the contained 
README.md. The tarball contains all software dependencies and workflow 
run scripts and molecular and machine learning datasets and should take around
**35-40 GBs** of local storage and 30 mins for the workflow to complete.


## To reproduce the figures in the paper, you can run:

```sh
source ./activate-environment
vine_plot_txn_log --mode workers paper_results/b.colmena-xtb.transactions workers.pdf
vine_plot_txn_log --mode tasks paper_results/b.colmena-xtb.transactions tasks.pdf
```

The plots in the paper were curated for presentation, so the legends, fonts,
etc. of these plots might be different but the plotted data is identical and
these plots should thus look identical to the paper's ones data-wise.

