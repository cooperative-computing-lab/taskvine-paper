To run this experiment, 100 workers should be allocated, each with 4 cores.
Then, run the blast executable twice in succession. This can be done like so: `./blast & ./blast`
Once executed, there will be a directory named `blast_runtime_info`.
Whithin, there are two subdirectories, each named with the startime of each execution.
A transactions file can be found within each subdirectory `/blast_runtime_info/<STARTTIME>/vine-logs/transactions`. 
Once retrieved, each log can be ploted with the plot\_blast tool.
like so `./plot\_blast /blast_runtime_info/<STARTTIME>/vine-logs/transactions <OUTPUT.png>`
