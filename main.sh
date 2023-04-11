#!/bin/bash

number=0

for i in ./info/*
do
    string="script$number"
    echo $i | nohup python3 ./scripts/main.py > ./output/$string.txt &
    ((number++))
done

exit 0