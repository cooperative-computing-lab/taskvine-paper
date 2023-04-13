To test out the bgd workflow, you can run the run one worker with a smaller number of tasks, for example 20.
Start the bgd manager program, run ```./vine_run_bgd.py --tasks 20```
It will begin by creating the Library file and environment, which may take some time. The workflow will not begin running until this is complete.
Start a single worker by running ```vine_worker -M coprocess```
The worker will receive the Library and run all 20 tasks. Once this is complete, the manager will output the set of weights with the least error.
The log file for this run will be present in vine-run-info/most-recent/vine-logs/transactions

To recreate the run presented in the paper, 200 workers should be allocated with the following settings:
2 cores, 3000 MB of memory, 5000 MB of disk, and a 900 second timeout. The factory.conf file contains the vine_factory configration file to create these workers.
Then start the manager program by running ```./vine_run_bgd.py --params 100 --iterations 200000 --error 0.0000001 --rate 0.000005 --tasks 2000```
The log	file for this run will be present in vine-run-info/most-recent/vine-logs/transactions

The log file for the run presented in the paper is in the paper_results subdirectory

To plot the log files, run ```./plot_bgd --mode tasks path_to_log_file``` to recreate the task view seen in fig 13c, and ```./plot_bgd --mode workers path_to_log_file``` to recreate the worker view seen in fig 13f
