# fetch-repo-list action
Fetch a list of repo with given filters in the org or user.

Usage example:
```
    - name: Find all workable repo
      id: repo_list
      uses: SFLScientific/fetch-repo-list@1.0.1
      with:
        last_active: [N_DAYS]
        template: [TEMLATE_NAME]
        token: [READ_ACCESS_TOKEN]
```

- `N_DAYS` is a time filter to only select repos that are activate in last N days.
- `TEMLATE_NAME` is the name of the template repo to filter on, for example `bo-sfl/personal-template`. 
- `READ_ACCESS_TOKEN` it the Github token to read repo information.