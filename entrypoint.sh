#!/bin/sh -l

echo "Hello $1"
time=$(python --last $1)
echo "::set-output name=time::$time"