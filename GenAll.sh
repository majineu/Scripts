#!/bin/bash
FILES=*.pos
for f in $FILES
do
	echo $f
	./Generalize.py  < $f > $f.gen
done

