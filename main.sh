#!/bin/bash

number=0

for i in ./info/*
do
    string="script$number"
    echo $i | nohup python3 ./scripts/main.py > ./output/$string.out &
    ((number++))
done

exit 0