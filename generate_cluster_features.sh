#!/bin/bash

files=$(ls *.clus)
#echo $files

> cluster_features

for file in $files
do
	cmd="python3 cluster_analysis.py $file --features --noplot >> cluster_features"
	echo "Executing $cmd"
	eval $cmd
done