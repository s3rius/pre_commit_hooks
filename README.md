# Collection of useful pre-commit hooks.

[![Coveralls](https://img.shields.io/coveralls/github/s3rius/pre_commit_hooks?style=for-the-badge)](https://coveralls.io/github/s3rius/pre_commit_hooks)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/pre_commit_hooks/Pre-commit%20check?style=for-the-badge)

This repo includes pre-commit-hooks that I couldn't find on the internet.
If you find it helpful too, please give a star to this repo.

Existing hooks:
* [Commit message prefix appender](#commit-message-prefix-appender)
* [TODOS linked to a Jira ticket](#todos-linked-to-a-jira-ticket)

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

## TODOS linked to a Jira ticket

### Abstract
This hook won't allow you to commit if you have todo linked to
currently active branch.

TODO is linked if it has the following format:
```
TODO TASK-123:
```

E.G.
If you work on a branch JTICKET-123 and you have
comment like this somwhere in your codebase:
```python
a = 3  # TODO JTICKET-123: change to 4
```
This hook will raise an error.


### Installation

Add to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/s3rius/pre_commit_hooks
    hooks:
    -   id: linked_todos
        args:
            - FIXME
            - FOR_TEST
```


### Arguments
You can use the following parameters:
```
positional arguments:
  formats          List of different formats for special comments. E.G FIXME. (default: [])

optional arguments:
  -h, --help       show this help message and exit
  --disable-todos  Disable todo detection. (default: False)
```

```
# note

Positional arguments are provided as is.

args:
    - '--disable-todos'
    - ONE
    - TWO
    - THREE

parameters 'ONE', 'TWO' and 'THREE' are positional.
```
