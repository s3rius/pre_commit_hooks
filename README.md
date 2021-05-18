# Collection of useful pre-commit hooks.

[![Coveralls](https://img.shields.io/coveralls/github/s3rius/pre_commit_hooks?style=for-the-badge)](https://coveralls.io/github/s3rius/pre_commit_hooks)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/pre_commit_hooks/Pre-commit%20check?style=for-the-badge)

This repo includes pre-commit-hooks that I couldn't find on the internet.
If you find it helpful too, please give a star to this repo.

Existing hooks:
* [Commit message prefix appender](#commit-message-prefix-appender)

## Commit message prefix appender

### Abstract
This hook appends JIRA task name at the beginning of the commit message just before you commit.

It detects that current branch is a JIRA ticket name and prepends it's name to the commit message.

Task name detecting is the following:
* Name starts with at least 2 **uppercase** latin letters;
* Letters followed by hyphen.
* hyphen followed by numbers.

E.G:
It will detect `TASK-123` or `AJAJ-312`.

### Installation
Add to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/s3rius/pre_commit_hooks
    hooks:
    -   id: commit_msg_prefix
        args:
            - "-f={}:"
```

And install `prepare-commit-msg` hooks like this.

```bash
pre-commit install --hook-type "prepare-commit-msg"
```

### Arguments
You can use the following parameters:
```
  -f FORMAT, --format FORMAT
                Commit prefix format. (default: {}:)
                The "{}" will be replaced with current branch name.

  --force       Force prefix addition. (default: False)
                Add prefix even if it already exists.
```
