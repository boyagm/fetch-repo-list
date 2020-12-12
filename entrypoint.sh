#!/bin/sh -l

echo "Activate Github in last $2 days."
echo "The template getting checked is $3."
echo "The orgnization name is $4."
repo_list=$(python /src/main.py --token $1 last_active $2 --template_name $3 --org_name $4)
echo "::set-output name=repo_list::$repo_list"
