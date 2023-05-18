#!/bin/bash

read GROUP
number=0

for i in ./info/group$GROUP/*
do
    string="script$number"
    echo $i | nohup python3 ./scripts/main.py > ./output/$string.out &
    ((number++))
done

exit 0