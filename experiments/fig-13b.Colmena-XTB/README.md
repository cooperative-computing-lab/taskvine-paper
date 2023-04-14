To rerun the ColmenaXTB experiment, go to
`https://doi.org/10.5281/zenodo.7823513`, download the `colmena-exp.tar.gz` 
tarball to the local machine, untar the tarball, and follow the contained 
README.md. The tarball contains all software dependencies and workflow 
run scripts and molecular and machine learning datasets and should take around
35-40 GBs of local storage and 30 mins for the workflow to complete. The file
`peer-enabled-url-env.log` contains the interactions between the workflow 
manager and its workers during one instance of the run and was used to create
the figure. To recreate the figures 13b and 13e, and assuming that the cctools
Conda environment is activated, do:
`vine_plot_txn_log -- mode tasks peer-enabled-url-env.log fig-13b.svg` and
`vine_plot_txn_log -- mode workers peer-enabled-url-env.log fig-13e.svg` for
figures 13-b and 13-e, respectively. The plots in the paper were curated
presentationally, so the legends, fonts, etc. of these plots might be 
different but the plotted data is identical and these plots should thus look
identical to the paper's ones data-wise.
