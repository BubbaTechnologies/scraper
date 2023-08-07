#!/bin/bash

DATE=$(date -d '2 hours ago' "+%Y-%m-%d-%H")
read GROUP

for i in ./info/group$GROUP/*
do
    fileName=$(basename i)
    fileNameWithoutExtension="${fileName%.*}"
    #TODO: Check if output directory exists
    echo $i | nohup python3 ./scripts/main.py > ./output/$fileNameWithoutExtension/$DATE.out
done

exit 0