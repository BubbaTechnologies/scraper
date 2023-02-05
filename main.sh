#! /bin/bash

for i in ./info/*
do
    echo $i | python3 main.py &
done