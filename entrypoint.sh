#!/bin/sh -l

echo $1
echo $2
time=$(python /src/main.py --last_active $1 --template_name $2)
echo "::set-output name=time::$time"
