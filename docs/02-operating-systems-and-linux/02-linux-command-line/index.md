# Linux command line

A compact reference for the chapter. Each section links the lesson that teaches it.

## Lessons

1. [Shell and terminal basics](01-shell-and-terminal-basics.md)
2. [Files and navigation](02-files-and-navigation.md)
3. [Users, groups and permissions](03-users-groups-and-permissions.md)
4. [Pipes, redirection and text tools](04-pipes-redirection-and-text-tools.md)
5. [Processes and signals](05-processes-and-signals.md)
6. [Packages with apt](06-packages-with-apt.md)
7. [Services, systemd and logs](07-services-systemd-and-logs.md)
8. [Environment variables and path](08-environment-variables-and-path.md)
9. [Shell scripting and cron](09-shell-scripting-and-cron.md)
10. [SSH and keys](10-ssh-and-keys.md)

## Key terms

| Term | Meaning |
|---|---|
| terminal, shell | the window; the program in it that reads lines (Bash) |
| argument, option | a word after the command; an argument starting with `-` |
| glob | a pattern like `*.txt` that the shell expands |
| exit code | 0 is success, non-zero is failure, stored in `$?` |
| absolute, relative path | starts with `/`; read from the working directory |
| stdin, stdout, stderr | streams 0, 1, 2 |
| PID, signal | process ID; a numbered message sent to a process |
| package, repository | a `.deb` archive; a server of packages with a signed index |
| unit, service | a thing systemd manages; a unit that runs a process |
| environment variable | a name and string passed to child processes |
| crontab | a user's table of scheduled jobs |
| public key, private key | the shareable half; the secret half of a key pair |

## Shell and files

Lessons: [shell and terminal basics](01-shell-and-terminal-basics.md), [files and navigation](02-files-and-navigation.md).

| Need | Command |
|---|---|
| where am I, go somewhere | `pwd`, `cd path`, `cd -`, `cd ~` |
| list all, long | `ls -la` |
| make folders | `mkdir -p a/b/c` |
| copy, move or rename, delete | `cp -r`, `mv`, `rm`, `rm -r` (permanent) |
| read a file | `cat`, `less`, `head -n`, `tail -n`, `tail -f` |
| find by name | `find . -name "*.py" -type f` |
| sizes | `du -sh dir`, `df -h` |
| learn a command | `man cmd`, `cmd --help`, `type cmd` |
| history | up arrow, `history`, Ctrl-R |

Quoting: double quotes expand `$var`, single quotes expand nothing, unquoted words split at spaces. WSL paths: `C:\` is `/mnt/c`; Linux files are at `\\wsl$\Ubuntu` from Windows.

## Permissions

Lesson: [users, groups and permissions](03-users-groups-and-permissions.md).

| Octal | Symbolic | Use |
|---|---|---|
| `755` | `rwxr-xr-x` | programs, shared folders |
| `644` | `rw-r--r--` | ordinary files |
| `600` | `rw-------` | private keys, secrets |
| `700` | `rwx------` | `~/.ssh` |

Commands: `chmod`, `chown owner:group`, `sudo`, `id`. The kernel uses the first matching class: owner, then group, then other.

## Redirection and text tools

Lesson: [pipes, redirection and text tools](04-pipes-redirection-and-text-tools.md).

| Syntax | Meaning |
|---|---|
| `>`, `>>` | stdout to file (replace, append) |
| `2>`, `2>&1` | stderr to file, stderr to where stdout goes |
| `\|` | stdout of one command into stdin of the next |
| `grep -rniv` | search folders, number lines, ignore case, invert |
| `sort -rn`, `uniq -c` | sort numerically, largest first; count adjacent repeats (sort first) |
| `wc -l`, `cut -d, -f2`, `tr a-z A-Z` | count lines, take a field, translate characters |
| `sed 's/a/b/g'`, `awk '{print $1}'` | replace, print a field |
| `xargs`, `tee` | lines into arguments; copy a stream to a file |

Top-N pattern: `awk '{print $1}' f | sort | uniq -c | sort -rn | head`.

## Processes and signals

Lesson: [processes and signals](05-processes-and-signals.md).

| Need | Command |
|---|---|
| list, live view | `ps aux`, `top`, `pgrep -f name` |
| background, list, resume | `cmd &`, `jobs`, `fg %1`, `bg %1`, Ctrl-Z |
| survive logout | `nohup cmd &`, or a service |
| polite, forced stop | `kill PID` (SIGTERM 15), `kill -9 PID` (SIGKILL) |

Exit code after a signal is 128 plus the signal number: 130 is Ctrl-C, 143 is SIGTERM, 137 is SIGKILL.

## Packages, services, logs

Lessons: [packages with apt](06-packages-with-apt.md), [services, systemd and logs](07-services-systemd-and-logs.md).

| Need | Command |
|---|---|
| refresh index, apply upgrades | `sudo apt update`, `sudo apt upgrade` |
| install, remove, purge | `sudo apt install x`, `remove x`, `purge x`, `autoremove` |
| inspect | `apt search`, `apt show`, `dpkg -L x`, `dpkg -S file` |
| service control | `systemctl status`, `start`, `stop`, `restart`, `enable --now` |
| after editing a unit | `sudo systemctl daemon-reload` |
| logs | `journalctl -u x -f --since "1 hour ago"` |

Unit file: `[Unit]` description and order, `[Service]` with `User=`, `ExecStart=` (full path) and `Restart=on-failure`, and `[Install]` with `WantedBy=multi-user.target`.

## Environment, scripts, cron

Lessons: [environment variables and path](08-environment-variables-and-path.md), [shell scripting and cron](09-shell-scripting-and-cron.md).

| Need | Syntax |
|---|---|
| set for children | `export NAME=value` |
| add to PATH | `export PATH="$HOME/bin:$PATH"` in `~/.bashrc`, then `source ~/.bashrc` |
| who wins | `type -a name`; the first match in `PATH` wins |
| safe script header | `#!/usr/bin/env bash` and `set -euo pipefail` |
| arguments | `$1`, `$#`, `"$@"` |
| cron fields | minute hour day-of-month month day-of-week command |

Cron examples: `*/5 * * * *` every 5 minutes, `0 2 * * *` daily at 02:00, `30 9 * * 1-5` weekdays at 09:30. Use full paths, `\%` for a literal percent, and `>> log 2>&1`.

## SSH

Lesson: [SSH and keys](10-ssh-and-keys.md).

| Need | Command |
|---|---|
| log in | `ssh user@host`, `ssh -p 2222 user@host` |
| make a key | `ssh-keygen -t ed25519 -C "you@example.com"` |
| install it | `ssh-copy-id user@host` |
| copy files | `scp f host:path`, `rsync -av dir/ host:dir/` |
| forward a port | `ssh -L 5433:localhost:5432 host` |
| clean an old host key | `ssh-keygen -R host` |

Modes: `~/.ssh` is `700`; the private key and `authorized_keys` are `600`. Share only the `.pub` file.
