#!/bin/bash

if [ $# -lt 2 ]; then
	echo "Usage: Need at least 2 parameters. 1:rpm-dir, 2:keep-number"
	echo "Example: ./cut.sh rpmlists 6"
	exit 1
fi	

count=1
for BVersion in `ls $1 |sort -r`
do
	if [ $count -gt $2 ]; then
		path=$1"/"$BVersion"/"
		echo "remove: "$path
		rm -rf $path
	else
		echo "keep: "$BVersion
	fi
	let "count++"
done
