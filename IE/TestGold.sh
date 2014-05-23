#!/bin/bash

if [ $# != ]; then
	echo "usage xx.sh model input output index"
	exit
fi

model=$1
in=$2
out=$3
idx=$4
./crf_test -m $model < $in | /home/sutd/Ji/Scripts/IE/CRF2Rel.py $idx > $out


