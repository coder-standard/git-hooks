# git-hooks for coders

* gitleaks precommit

# setup

1. install [python3](https://www.python.org/)
2. install [gitleaks](https://github.com/zricethezav/gitleaks)
3. install `git-hooks-tools`
    ```bash
   https://github.com/coder-standard/git-hooks.git
   cd git-hooks
   ./install-tools.sh
   ```
4. install hooks
   1. install hooks for local project
       ```bash
      cd ${root_of_project}
      install-git-hooks.sh
       ```
   2. install hooks for global - only effect on new cloned projects
       ```bash
       install-git-hooks.sh -g
      ```

# extend

## use local gitleaks config file

create .gitleaks.toml on root of project
