# Command cheat sheets

Linux, Git, Docker and psql commands in one place, plus the tools around them. Every command here appears in a lesson or a chapter cheat sheet, and the last column links the lesson that explains it. Placeholders are in capitals (`HOST`, `NAME`). Shell commands assume WSL2 Ubuntu unless a row says otherwise.

## Linux shell

| Command | What it does | Lesson |
|---|---|---|
| `pwd`, `cd path`, `cd -`, `cd ~` | Show the working directory, change it, go back, go home | [Files and navigation](../02-operating-systems-and-linux/02-linux-command-line/02-files-and-navigation.md) |
| `ls -la` | List all files, long format | [Files and navigation](../02-operating-systems-and-linux/02-linux-command-line/02-files-and-navigation.md) |
| `mkdir -p a/b/c` | Make a folder and its parents | [Files and navigation](../02-operating-systems-and-linux/02-linux-command-line/02-files-and-navigation.md) |
| `cp -r`, `mv`, `rm`, `rm -r` | Copy, move or rename, delete (permanent), delete a folder | [Files and navigation](../02-operating-systems-and-linux/02-linux-command-line/02-files-and-navigation.md) |
| `cat`, `less`, `head -n`, `tail -n`, `tail -f` | Read a file, page through it, first or last lines, follow new lines | [Files and navigation](../02-operating-systems-and-linux/02-linux-command-line/02-files-and-navigation.md) |
| `find . -name "*.py" -type f` | Find files by name | [Files and navigation](../02-operating-systems-and-linux/02-linux-command-line/02-files-and-navigation.md) |
| `du -sh dir`, `df -h` | Size of a folder, free space on disks | [Files and navigation](../02-operating-systems-and-linux/02-linux-command-line/02-files-and-navigation.md) |
| `man cmd`, `cmd --help`, `type cmd` | Read the manual, show usage, show what a name resolves to | [Shell and terminal basics](../02-operating-systems-and-linux/02-linux-command-line/01-shell-and-terminal-basics.md) |
| `chmod`, `chown owner:group`, `sudo`, `id` | Change permissions, change owner, run as root, show your user and groups | [Users, groups and permissions](../02-operating-systems-and-linux/02-linux-command-line/03-users-groups-and-permissions.md) |
| `>`, `>>`, `2>`, `2>&1` | Redirect stdout (replace, append), stderr, stderr to where stdout goes | [Pipes, redirection and text tools](../02-operating-systems-and-linux/02-linux-command-line/04-pipes-redirection-and-text-tools.md) |
| `grep -rniv` | Search folders, number lines, ignore case, invert the match | [Pipes, redirection and text tools](../02-operating-systems-and-linux/02-linux-command-line/04-pipes-redirection-and-text-tools.md) |
| `sort -rn`, `uniq -c`, `wc -l` | Sort numerically largest first, count adjacent repeats (sort first), count lines | [Pipes, redirection and text tools](../02-operating-systems-and-linux/02-linux-command-line/04-pipes-redirection-and-text-tools.md) |
| `cut -d, -f2`, `tr a-z A-Z`, `sed 's/a/b/g'`, `awk '{print $1}'` | Take a field, translate characters, replace text, print a field | [Pipes, redirection and text tools](../02-operating-systems-and-linux/02-linux-command-line/04-pipes-redirection-and-text-tools.md) |
| `xargs`, `tee` | Turn lines into arguments, copy a stream to a file | [Pipes, redirection and text tools](../02-operating-systems-and-linux/02-linux-command-line/04-pipes-redirection-and-text-tools.md) |
| `ps aux`, `top`, `pgrep -f name` | List processes, live view, find a PID by name | [Processes and signals](../02-operating-systems-and-linux/02-linux-command-line/05-processes-and-signals.md) |
| `cmd &`, `jobs`, `fg %1`, `bg %1` | Run in the background, list jobs, bring one forward or send it back | [Processes and signals](../02-operating-systems-and-linux/02-linux-command-line/05-processes-and-signals.md) |
| `nohup cmd &` | Keep a command running after you log out | [Processes and signals](../02-operating-systems-and-linux/02-linux-command-line/05-processes-and-signals.md) |
| `kill PID`, `kill -9 PID` | Ask a process to stop (SIGTERM), force it (SIGKILL) | [Processes and signals](../02-operating-systems-and-linux/02-linux-command-line/05-processes-and-signals.md) |
| `sudo apt update`, `sudo apt upgrade` | Refresh the package index, apply upgrades | [Packages with apt](../02-operating-systems-and-linux/02-linux-command-line/06-packages-with-apt.md) |
| `sudo apt install x`, `remove x`, `purge x`, `autoremove` | Install, remove, remove with config, clean unused dependencies | [Packages with apt](../02-operating-systems-and-linux/02-linux-command-line/06-packages-with-apt.md) |
| `apt search`, `apt show`, `dpkg -L x`, `dpkg -S file` | Search, inspect, list a package's files, find the owner of a file | [Packages with apt](../02-operating-systems-and-linux/02-linux-command-line/06-packages-with-apt.md) |
| `systemctl status`, `start`, `stop`, `restart`, `enable --now` | Control a service | [Services, systemd and logs](../02-operating-systems-and-linux/02-linux-command-line/07-services-systemd-and-logs.md) |
| `sudo systemctl daemon-reload` | Re-read unit files after editing one | [Services, systemd and logs](../02-operating-systems-and-linux/02-linux-command-line/07-services-systemd-and-logs.md) |
| `journalctl -u x -f --since "1 hour ago"` | Read and follow a service's logs | [Services, systemd and logs](../02-operating-systems-and-linux/02-linux-command-line/07-services-systemd-and-logs.md) |
| `export NAME=value` | Set an environment variable for child processes | [Environment variables and path](../02-operating-systems-and-linux/02-linux-command-line/08-environment-variables-and-path.md) |
| `export PATH="$HOME/bin:$PATH"`, `source ~/.bashrc` | Add a folder to `PATH`, reload the shell config | [Environment variables and path](../02-operating-systems-and-linux/02-linux-command-line/08-environment-variables-and-path.md) |
| `type -a name` | Show every match on `PATH`; the first one wins | [Environment variables and path](../02-operating-systems-and-linux/02-linux-command-line/08-environment-variables-and-path.md) |
| `set -euo pipefail` | Safe script header, after `#!/usr/bin/env bash` | [Shell scripting and cron](../02-operating-systems-and-linux/02-linux-command-line/09-shell-scripting-and-cron.md) |
| `$1`, `$#`, `"$@"` | Script arguments: first, count, all | [Shell scripting and cron](../02-operating-systems-and-linux/02-linux-command-line/09-shell-scripting-and-cron.md) |
| `*/5 * * * *`, `0 2 * * *`, `30 9 * * 1-5` | Cron schedules: every 5 minutes, daily at 02:00, weekdays at 09:30 | [Shell scripting and cron](../02-operating-systems-and-linux/02-linux-command-line/09-shell-scripting-and-cron.md) |
| `ssh user@host`, `ssh -p 2222 user@host` | Log in to a server | [SSH and keys](../02-operating-systems-and-linux/02-linux-command-line/10-ssh-and-keys.md) |
| `ssh-keygen -t ed25519 -C "you@example.com"` | Make a key pair | [SSH and keys](../02-operating-systems-and-linux/02-linux-command-line/10-ssh-and-keys.md) |
| `ssh-copy-id user@host` | Install your public key on a server | [SSH and keys](../02-operating-systems-and-linux/02-linux-command-line/10-ssh-and-keys.md) |
| `scp f host:path`, `rsync -av dir/ host:dir/` | Copy files over SSH | [SSH and keys](../02-operating-systems-and-linux/02-linux-command-line/10-ssh-and-keys.md) |
| `ssh -L 5433:localhost:5432 host` | Forward a local port to the server | [SSH and keys](../02-operating-systems-and-linux/02-linux-command-line/10-ssh-and-keys.md) |
| `ssh-keygen -R host` | Remove an old host key | [SSH and keys](../02-operating-systems-and-linux/02-linux-command-line/10-ssh-and-keys.md) |

## Git and GitHub

| Command | What it does | Lesson |
|---|---|---|
| `git init -b main`, `git clone URL` | Start a repo, copy one | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git status`, `git diff`, `git diff --staged` | See what changed and where | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git add FILE`, `git commit -m "msg"` | Stage a file, save a snapshot | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git log --oneline --graph --all --decorate` | History as a graph | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git restore FILE`, `git restore --staged FILE` | Discard an unstaged edit (lost for good), unstage a file | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git revert HASH` | Undo a shared commit with a new commit | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git reset --soft HEAD~1`, `git reset --hard HEAD~1` | Undo a local commit, keeping or dropping its changes | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git reflog` | Find a lost commit (local only) | [Git basics](../04-developer-tools-and-workflow/01-editor-and-git/02-git-basics.md) |
| `git switch -c NAME`, `git switch NAME` | Create a branch, change branch | [Branches, merging and conflicts](../04-developer-tools-and-workflow/01-editor-and-git/03-branches-merging-and-conflicts.md) |
| `git merge BRANCH`, `git merge --abort` | Combine a branch, give up a merge | [Branches, merging and conflicts](../04-developer-tools-and-workflow/01-editor-and-git/03-branches-merging-and-conflicts.md) |
| `git rebase BRANCH` | Replay your commits on top (local commits only) | [Branches, merging and conflicts](../04-developer-tools-and-workflow/01-editor-and-git/03-branches-merging-and-conflicts.md) |
| `git stash`, `git stash pop` | Shelve and restore uncommitted edits | [Branches, merging and conflicts](../04-developer-tools-and-workflow/01-editor-and-git/03-branches-merging-and-conflicts.md) |
| `git fetch`, `git pull`, `git push -u origin BRANCH` | Sync with the remote | [GitHub, pull requests and code review](../04-developer-tools-and-workflow/01-editor-and-git/04-github-pull-requests-and-code-review.md) |
| `git remote -v`, `git branch -vv` | List remotes, show tracking info | [GitHub, pull requests and code review](../04-developer-tools-and-workflow/01-editor-and-git/04-github-pull-requests-and-code-review.md) |
| `gh auth login` | Log in to GitHub from the terminal | [GitHub, pull requests and code review](../04-developer-tools-and-workflow/01-editor-and-git/04-github-pull-requests-and-code-review.md) |
| `gh repo clone owner/repo`, `gh repo fork --clone` | Clone, fork | [GitHub, pull requests and code review](../04-developer-tools-and-workflow/01-editor-and-git/04-github-pull-requests-and-code-review.md) |
| `gh pr create --fill`, `gh pr list`, `gh pr view` | Open and read pull requests | [GitHub, pull requests and code review](../04-developer-tools-and-workflow/01-editor-and-git/04-github-pull-requests-and-code-review.md) |
| `gh pr checkout N`, `gh pr merge --squash` | Review locally, merge | [GitHub, pull requests and code review](../04-developer-tools-and-workflow/01-editor-and-git/04-github-pull-requests-and-code-review.md) |

## Docker and Compose

| Command | What it does | Lesson |
|---|---|---|
| `docker run --rm -it IMAGE CMD` | Run a command in a new container, delete it on exit | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker run -d --name N -p 8080:80 IMAGE` | Run in the background, publish host port 8080 to container port 80 | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker run -m 64m IMAGE` | Limit memory | [VMs vs containers](../13-devops-and-cloud/01-containers/01-vms-vs-containers.md) |
| `docker ps`, `docker ps -a` | List running containers, all containers | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker logs -f N` | Follow a container's output | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker exec -it N sh` | Open a shell in a running container | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker stop N`, `docker rm N` | Stop, remove a container | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker build -t name:tag .` | Build an image from the Dockerfile in this folder | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker build --platform linux/amd64 .` | Build for a specific architecture | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker images`, `docker rmi IMAGE` | List, remove images | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker system prune` | Remove stopped containers, unused networks and dangling images (asks first) | [Docker images and Dockerfiles](../13-devops-and-cloud/01-containers/02-docker-images-and-dockerfiles.md) |
| `docker run -v NAME:/path IMAGE` | Mount a named volume (use `-v "$PWD":/path` for a bind mount) | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker volume ls` | List volumes | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker compose up -d --build` | Build and start all services | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker compose ps` | Service status | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker compose logs -f SERVICE` | Follow a service's logs | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker compose exec SERVICE CMD` | Run a command in a service | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker compose down` | Remove containers and network, keep volumes | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker compose down -v` | Also delete volumes (the data is gone) | [Volumes, networks and Compose](../13-devops-and-cloud/01-containers/03-volumes-networks-and-compose.md) |
| `docker login [REGISTRY]` | Authenticate to a registry | [Registries and Kubernetes basics](../13-devops-and-cloud/01-containers/04-registries-and-kubernetes-basics.md) |
| `docker tag SRC DEST`, `docker push`, `docker pull` | Add a name to an image, upload, download | [Registries and Kubernetes basics](../13-devops-and-cloud/01-containers/04-registries-and-kubernetes-basics.md) |

## psql and Postgres tools

Meta-commands start with a backslash and take no semicolon.

| Command | What it does | Lesson |
|---|---|---|
| `psql -h localhost -p 5432 -U app -d shop` | Connect with options | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `psql "postgres://app:secret@localhost:5432/shop"` | Connect with a connection string | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\?` | Help on meta-commands | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\l` | List databases | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\c dbname` | Connect to another database | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\dn`, `\dt`, `\d table` | List schemas, list tables, describe a table | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\x` | Toggle expanded output | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\timing` | Toggle statement timing | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\i file.sql` | Run a SQL file | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\conninfo` | Show the current connection | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `\q` | Quit | [Postgres and psql](../10-databases-sql-and-postgres/01-database-basics/03-postgres-and-psql.md) |
| `EXPLAIN SELECT ...`, `EXPLAIN (ANALYZE, BUFFERS) SELECT ...` | Show the plan, or run the query and add real times and page reads | [EXPLAIN and query plans](../10-databases-sql-and-postgres/04-postgres-in-depth/02-explain-and-query-plans.md) |
| `pg_dump --format=custom --file=shop.dump shop` | Logical backup of one database | [Postgres in depth](../10-databases-sql-and-postgres/04-postgres-in-depth/index.md) |
| `pg_restore --dbname=shop_copy --clean --if-exists shop.dump` | Restore a custom-format dump | [Postgres in depth](../10-databases-sql-and-postgres/04-postgres-in-depth/index.md) |

## npm, pip and venv

| Command | What it does | Lesson |
|---|---|---|
| `npm install pkg`, `npm install --save-dev pkg` | Add a package, add a dev tool | [Package managers and dependencies](../04-developer-tools-and-workflow/02-project-plumbing/01-package-managers-and-dependencies.md) |
| `npm ci` | Rebuild exactly from the lockfile | [Package managers and dependencies](../04-developer-tools-and-workflow/02-project-plumbing/01-package-managers-and-dependencies.md) |
| `npm ls --all`, `npx tool` | Show the dependency tree, run a tool | [Package managers and dependencies](../04-developer-tools-and-workflow/02-project-plumbing/01-package-managers-and-dependencies.md) |
| `python -m venv .venv` (Linux: `python3 -m venv .venv`) | Create a virtual environment | [Modules, packages, pip and venv](../03-programming-fundamentals/01-python-basics/08-modules-packages-pip-and-venv.md) |
| `.venv\Scripts\Activate.ps1` (Linux: `source .venv/bin/activate`) | Activate it | [Modules, packages, pip and venv](../03-programming-fundamentals/01-python-basics/08-modules-packages-pip-and-venv.md) |
| `python -m pip install NAME` | Install a package | [Modules, packages, pip and venv](../03-programming-fundamentals/01-python-basics/08-modules-packages-pip-and-venv.md) |
| `python -m pip freeze > requirements.txt` | Save installed versions | [Modules, packages, pip and venv](../03-programming-fundamentals/01-python-basics/08-modules-packages-pip-and-venv.md) |
| `python -m pip install -r requirements.txt` | Recreate the environment | [Modules, packages, pip and venv](../03-programming-fundamentals/01-python-basics/08-modules-packages-pip-and-venv.md) |
| `uv add pkg`, `uv add --dev pkg`, `uv sync`, `uv tree`, `uv run tool` | The same jobs with uv | [Package managers and dependencies](../04-developer-tools-and-workflow/02-project-plumbing/01-package-managers-and-dependencies.md) |

## curl and network tools

The [networking cheat sheet](../07-networking/01-how-the-internet-works/index.md) has the Windows equivalents side by side.

| Command | What it does | Lesson |
|---|---|---|
| `curl -v URL` | Show the full exchange | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `curl -sI URL` | Headers only | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `curl -X POST URL -H "Content-Type: application/json" -d '{"a":1}'` | Send JSON | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `curl -s -o /dev/null -w "dns %{time_namelookup} tls %{time_appconnect} ttfb %{time_starttransfer}\n" URL` | Timing breakdown | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `nslookup NAME`, `dig NAME` | DNS lookup | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `ping -c 4 HOST` (Windows `-n 4`) | Check reachability and round trip time | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `traceroute HOST` (Windows `tracert`) | Show the path | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `ss -tlnp` (Windows `netstat -an`) | Listening ports and their programs | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |
| `openssl s_client -connect HOST:443 -servername HOST` | Show the certificate chain | [Network debugging tools](../07-networking/02-web-protocols/07-network-debugging-tools.md) |

## kubectl

| Command | What it does | Lesson |
|---|---|---|
| `kubectl apply -f file.yaml` | Create or update objects | [Registries and Kubernetes basics](../13-devops-and-cloud/01-containers/04-registries-and-kubernetes-basics.md) |
| `kubectl get pods` | List pods | [Registries and Kubernetes basics](../13-devops-and-cloud/01-containers/04-registries-and-kubernetes-basics.md) |
| `kubectl describe pod NAME` | Details and events | [Registries and Kubernetes basics](../13-devops-and-cloud/01-containers/04-registries-and-kubernetes-basics.md) |
| `kubectl logs NAME` | Pod output | [Registries and Kubernetes basics](../13-devops-and-cloud/01-containers/04-registries-and-kubernetes-basics.md) |
| `kubectl rollout status deployment/NAME` | Wait for a rollout | [Registries and Kubernetes basics](../13-devops-and-cloud/01-containers/04-registries-and-kubernetes-basics.md) |

## AWS CLI

Checked against the [AWS CLI v2 reference](https://docs.aws.amazon.com/cli/latest/reference/), not against a live account. Set `export AWS_PROFILE=lab` first and check the Region.

| Command | What it does | Lesson |
|---|---|---|
| `aws sts get-caller-identity` | Show who you are | [AWS account, IAM and billing](../13-devops-and-cloud/03-aws/02-aws-account-iam-and-billing.md) |
| `aws ec2 run-instances ...`, `aws ec2 terminate-instances --instance-ids ID` | Launch, terminate an instance | [EC2](../13-devops-and-cloud/03-aws/03-ec2.md) |
| `aws ec2 authorize-security-group-ingress --group-id SG --protocol tcp --port 443 --cidr 0.0.0.0/0` | Open a port | [VPCs and security groups](../13-devops-and-cloud/03-aws/06-vpcs-and-security-groups.md) |
| `aws ec2 create-vpc`, `create-subnet`, `create-internet-gateway`, `create-route-table`, `create-route` | Build the VPC pieces | [VPCs and security groups](../13-devops-and-cloud/03-aws/06-vpcs-and-security-groups.md) |
| `aws s3 cp FILE s3://BUCKET/KEY`, `aws s3 ls s3://BUCKET/` | Copy to S3, list a bucket | [S3](../13-devops-and-cloud/03-aws/04-s3.md) |
| `aws rds create-db-instance ... --no-publicly-accessible --vpc-security-group-ids SG` | Create a private database | [RDS managed Postgres](../13-devops-and-cloud/03-aws/05-rds-managed-postgres.md) |
| `aws rds delete-db-instance --db-instance-identifier ID --skip-final-snapshot --delete-automated-backups` | Delete a database | [RDS managed Postgres](../13-devops-and-cloud/03-aws/05-rds-managed-postgres.md) |
| `aws lambda create-function --function-name N --runtime python3.14 --handler lambda_function.lambda_handler --role ARN --zip-file fileb://lambda.zip` | Deploy a function | [Lambda and serverless](../13-devops-and-cloud/03-aws/07-lambda-and-serverless.md) |
| `aws lambda invoke --function-name N --cli-binary-format raw-in-base64-out --payload JSON out.json` | Invoke a function | [Lambda and serverless](../13-devops-and-cloud/03-aws/07-lambda-and-serverless.md) |
| `aws lambda delete-function --function-name N` | Delete a function | [Lambda and serverless](../13-devops-and-cloud/03-aws/07-lambda-and-serverless.md) |
| `aws logs tail /aws/lambda/N --since 10m` | Read a function's logs | [Lambda and serverless](../13-devops-and-cloud/03-aws/07-lambda-and-serverless.md) |
| `sudo nginx -t`, `sudo systemctl reload nginx` | On the server: test the nginx config, apply it | [Deploying an app to EC2](../13-devops-and-cloud/03-aws/08-deploying-an-app-to-ec2.md) |
| `sudo certbot --nginx -d HOST`, `sudo certbot renew --dry-run` | On the server: get a certificate, test renewal | [Deploying an app to EC2](../13-devops-and-cloud/03-aws/08-deploying-an-app-to-ec2.md) |
