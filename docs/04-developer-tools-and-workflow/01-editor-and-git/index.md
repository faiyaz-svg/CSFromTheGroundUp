# Editor and Git

A compact reference for the chapter. The lessons teach the ideas; this page is for looking things up.

1. [VS Code and IDEs](01-vs-code-and-ides.md)
2. [Git basics](02-git-basics.md)
3. [Branches, merging and conflicts](03-branches-merging-and-conflicts.md)
4. [GitHub, pull requests and code review](04-github-pull-requests-and-code-review.md)

## Key terms

| Term | Meaning |
|---|---|
| IDE | editor plus language-aware tools: completion, errors, refactoring, debugger, terminal |
| Language server | program that answers the editor's questions about your code, spoken over LSP |
| Working tree, index, repository | the files on disk, the draft of the next commit, the history |
| Commit | snapshot of the project with a message and a pointer to its parent |
| Branch, HEAD | movable pointer to a commit; the commit or branch you are on |
| Fast-forward, merge commit | pointer just moves; commit with two parents |
| Conflict | both sides changed the same lines; you choose the result |
| Remote, `origin/main` | named copy of the repo; local record of the remote's `main` |
| Pull request | request on GitHub to merge a branch, with review and checks |

## VS Code keys (Windows and Linux)

| Keys | Action |
|---|---|
| `Ctrl+Shift+P` | command palette |
| `Ctrl+P` | open file by name |
| `F12`, `Shift+F12` | definition, references |
| `F2`, `Ctrl+.` | rename, quick fix |
| `F9`, `F5`, `F10`, `F11` | breakpoint, run/continue, step over, step into |

## Git commands

| Command | Use |
|---|---|
| `git init -b main`, `git clone <url>` | start or copy a repo |
| `git status`, `git diff`, `git diff --staged` | see what changed and where |
| `git add <file>`, `git commit -m "msg"` | stage, then save a snapshot |
| `git log --oneline --graph --all --decorate` | history as a graph |
| `git switch -c <name>`, `git switch <name>` | create, change branch |
| `git merge <branch>`, `git merge --abort` | combine, give up |
| `git rebase <branch>` | replay your commits on top (local commits only) |
| `git stash`, `git stash pop` | shelve and restore uncommitted edits |
| `git fetch`, `git pull`, `git push -u origin <branch>` | sync with the remote |
| `git remote -v`, `git branch -vv` | remotes, tracking info |

## Undo guide

| Situation | Command | Safe after push? |
|---|---|---|
| Discard an unstaged edit | `git restore <file>` | edit is lost for good |
| Unstage | `git restore --staged <file>` | yes |
| Undo a shared commit | `git revert <hash>` | yes |
| Undo a local commit, keep changes | `git reset --soft HEAD~1` | no |
| Undo a local commit, drop changes | `git reset --hard HEAD~1` | no |
| Find a lost commit | `git reflog` | local only |

## Rules

- Run `git status` before every commit and read `git diff --staged`.
- One logical change per commit; subject in the imperative, about 50 characters.
- Rebase only commits nobody else has. Never force-push a shared branch; use `--force-with-lease` on your own.
- A secret that was committed is leaked: rotate it.
- Protect `main`: require a pull request, approvals and passing checks.
- SSH: private key stays on your machine, public key goes to GitHub. HTTPS: use a token, not your password.

## gh quick list

| Command | Use |
|---|---|
| `gh auth login` | log in |
| `gh repo clone owner/repo`, `gh repo fork --clone` | clone, fork |
| `gh pr create --fill`, `gh pr list`, `gh pr view` | open and read PRs |
| `gh pr checkout <n>`, `gh pr merge --squash` | review locally, merge |
