#!/bin/bash

files=$(ls *.clus)
#echo $files
init_samp=0
> cluster_features

for file in $files
do
	cmd="python3 cluster_analysis.py $file --features --noplot > feat_tmp"
	copy="cat feat_tmp >> cluster_features"
	echo "Executing $cmd"
	eval $cmd
	eval $copy
	n_samp=$(cat feat_tmp | wc -l)
	echo "Total samples: $n_samp"
	end_samp=$((init_samp+n_samp-1))
	echo "features $init_samp to $end_samp"
	init_samp=$((end_samp+1))
done

rm feat_tmp
