# experiment-manager

experiment-manager is a command line tool for bash to grid search experiments. 

Currently it supports experiments that can be launched through a bash command where all parameters are passed as command line flags. Givne a JSON configuration file, experiment-manager launches all experiments on a given number of jobs. Each job runs a certain number of experiments sequentially. 
