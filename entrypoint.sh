#!/bin/sh -l

echo "Activate Github in last $1 days."
echo "The template getting checked is $2."
python /src/main.py --last_active $1 --template_name $2 --token $3
echo "::set-output name=repo_list::$(cat /src/repos.txt)"
