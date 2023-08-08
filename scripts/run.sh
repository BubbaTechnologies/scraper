#!/bin/bash

DATE=$(date "+%Y-%m-%d-%H")
read GROUP

#Loads enviorment 
bash ./scripts/login.sh
source ./.venv/bin/activate

for file in ./info/group$GROUP/*
do
    fileName=$(basename $file)
    fileNameWithoutExtension="${fileName%.*}"
    outputDirectory="./output/$fileNameWithoutExtension"
    if [ ! -d "$directoutputDirectoryory" ]; then
        mkdir -p "$outputDirectory"
    fi
    echo $i | nohup python3 ./scripts/main.py > $outputDirectory/$DATE.out
done

exit 0