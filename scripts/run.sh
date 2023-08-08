#!/bin/bash

DIRECTORY="/home/mgroholski/scraper"

DATE=$(date "+%Y-%m-%d-%H")
read GROUP

#Loads enviorment 
bash $DIRECTORY/scripts/login.sh
source $DIRECTORY/.venv/bin/activate

for file in $DIRECTORY/info/group$GROUP/*
do
    fileName=$(basename $file)
    fileNameWithoutExtension="${fileName%.*}"
    outputDirectory="$DIRECTORY/output/$fileNameWithoutExtension"
    if [ ! -d "$directoutputDirectoryory" ]; then
        mkdir -p "$outputDirectory"
    fi
    echo $i | nohup python3 $DIRECTORY/scripts/main.py > $outputDirectory/$DATE.out &
done

exit 0