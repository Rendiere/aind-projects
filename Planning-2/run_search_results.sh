#!/bin/zsh

for p in 1 2 3
do
	for s in 1 2 3 4 5 6 7 8 9 10
	do
		out="results/raw/p_${p}_s_${s}.txt"
		touch $out
		echo "Doing search with p = ${p} and s = ${s}"
		echo "python run_search.py -p ${p} -s ${s} > $out"
		python run_search.py -p $p -s $s > $out
	done
done