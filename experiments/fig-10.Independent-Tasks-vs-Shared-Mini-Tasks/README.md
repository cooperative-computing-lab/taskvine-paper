First, curl the environment needed for the experiment: `curl https://ccl.cse.nd.edu/temp/package.tar.gz --output package.tar.gz`
To run this experiment, 50 workers should be allocated, each with 4 cores. Then, run the executables `./vine_example_ponchoMinitask` and `./vine_example_NoMiniTask`
Once executed, there will be directories named `vine_example_ponchoMINITASK_info` and `vine_example_ponchoMINITASK_info`.
Whithin each, there are subdirectories, named with the startime of each execution.
A transactions file can be found within each subdirectory `/vine_example_ponchoMINITASK_info/<STARTTIME>/vine-logs/transactions` and. `/vine_example_ponchoNOMINITASK_info/<STARTTIME>/vine-logs/transactions` 
Once retrieved, each log can be ploted with the plot\_poncho tool.
like so `./plot\_poncho /blasr_runtime_info/<STARTTIME>/vine-logs/transactions <OUTPUT.png>`
