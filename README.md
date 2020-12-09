# fetch-repo-list action
Fetch a list of repo with given filters in the org or user.

Usage example:
```
    - name: Find all workable repo
      id: get_repo_list
      uses: SFLScientific/fetch-repo-list
      with:
        last_active: [N_DAYS]
        template: [TEMPLATE_NAME]
        token: [READ_ACCESS_TOKEN]
```

- `N_DAYS` is a time filter to only select repos that are activate in last N days.
- `TEMPLATE_NAME` is the name of the template repo to filter on, for example `bo-sfl/personal-template`. 
- `READ_ACCESS_TOKEN` it the Github token to read repo information.

The final output it passed to the `steps.[STEP_ID].outputs.repo_list`, in the above example, the `STEP_ID` is `get_repo_list`