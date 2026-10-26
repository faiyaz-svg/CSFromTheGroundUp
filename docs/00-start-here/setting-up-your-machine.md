# Setting up your machine

After this you have one development environment on Windows 11 that every lab in the book uses: Ubuntu under WSL2, VS Code, Git with an SSH key, Python, Node.js, Docker and PostgreSQL.

You do this once, and it takes an hour or two, mostly waiting for downloads. If a step fails, paste the exact error into an AI assistant along with your Windows version and the command you ran (see [Reading docs and error messages](reading-docs-and-error-messages.md)).

## The idea

Most servers run Linux, so the labs use Linux tools. **WSL2** (Windows Subsystem for Linux, version 2) runs a real Linux kernel inside a lightweight virtual machine on Windows, so you get Ubuntu without dual-booting. Your editor and browser stay on Windows; your code, terminals and tools live in Ubuntu.

Two shells matter, and mixing them up causes most setup problems.

| Where | Prompt looks like | Use it for |
|---|---|---|
| PowerShell (Windows) | `PS C:\Users\you>` | Installing WSL, `wsl` management commands, Docker Desktop and VS Code installers |
| Ubuntu (WSL) | `you@machine:~$` | Everything else: Git, Python, Node.js, `psql`, running your code |

Every command below says which one it runs in. If the book says nothing, use Ubuntu.

Files go in the Linux home directory (`~`, for example `~/projects`), not under `/mnt/c/...`. Microsoft's guidance is to store files on the same operating system as the tools that use them, and Linux tools are much slower on the Windows drive ([WSL environment guide](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)). To see your Linux files from Windows, run `explorer.exe .` inside the folder.

## Step 1: WSL2 and Ubuntu

In PowerShell opened as administrator (right-click, Run as administrator):

```powershell
wsl --install
```

This enables the needed Windows features, installs the Linux kernel, sets WSL 2 as the default and installs Ubuntu. Restart when asked, then open Ubuntu from the Start menu. It asks for a Linux username and password. The password does not show as you type; that is normal, and the account can run `sudo`. Source: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

Check that the distribution runs as version 2 (PowerShell):

```powershell
wsl -l -v
```

Then update Ubuntu's packages (Ubuntu). Windows does not do this for you.

```bash
sudo apt update && sudo apt upgrade
```

## Step 2: Windows Terminal and VS Code

Microsoft recommends Windows Terminal for WSL, because it opens PowerShell and Ubuntu in tabs. Install it from the Microsoft Store if it is not already there.

Install VS Code on Windows (not inside Ubuntu) from [code.visualstudio.com](https://code.visualstudio.com/docs/remote/wsl), and keep "Add to PATH" ticked. Then install the **WSL** extension (`ms-vscode-remote.remote-wsl`). In Ubuntu:

```bash
mkdir -p ~/projects/hello
cd ~/projects/hello
code .
```

The first run downloads a small server component into Ubuntu. When the window opens, the bottom-left corner shows a WSL indicator: the editor is on Windows, but files, terminals and debugging run in Ubuntu. If `code` is not found, restart the terminal.

## Step 3: Git and an SSH key

Git is usually pre-installed. Install or update it and set your identity (Ubuntu). The email should match the one on your GitHub account.

```bash
sudo apt install git
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

An **SSH key** is a pair of files: a private key that stays on your machine and a public key you give to GitHub. GitHub then accepts your pushes without a password. Create one with the Ed25519 algorithm, following [GitHub's guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent):

```bash
ssh-keygen -t ed25519 -C "you@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Accept the default file location and choose a passphrase. Never share the file without the `.pub` ending; that is the private key.

Now give GitHub the public key, either in the browser ([adding a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account), paste the output of `cat ~/.ssh/id_ed25519.pub`) or with the GitHub CLI. If you install `gh` (see [its install page](https://cli.github.com/)), `gh auth login` with the SSH protocol looks for an existing key to upload ([manual](https://cli.github.com/manual/gh_auth_login)). Test the connection:

```bash
ssh -T git@github.com
```

```text
Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

The first time, SSH asks you to confirm GitHub's fingerprint; compare it with the [published fingerprints](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/githubs-ssh-key-fingerprints) before typing `yes` ([testing your connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)). The command exits with code 1 even on success, which is expected. Git Credential Manager, mentioned in Microsoft's guide, only handles HTTPS remotes, so you can skip it when you use SSH.

## Step 4: Python

Ubuntu includes `python3`. Create a virtual environment per project, so packages for one project do not collide with another (Ubuntu):

```bash
cd ~/projects/hello
python3 -m venv .venv
source .venv/bin/activate
python --version
```

If `venv` fails and suggests installing a package, run `sudo apt install python3-venv` as the error says. Usage is from the [venv documentation](https://docs.python.org/3/library/venv.html).

## Step 5: Node.js with nvm

**nvm** (Node Version Manager) installs Node.js into your home directory and lets you switch versions. As of 2026 its latest release is v0.40.8 ([nvm README](https://github.com/nvm-sh/nvm)). Check the README for a newer version number before you copy the URL.

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
```

Close and reopen the terminal, then confirm that `command -v nvm` prints `nvm`, and install the current long-term support (LTS) release:

```bash
command -v nvm
nvm install --lts
```

As of 2026, [nodejs.org lists](https://nodejs.org/en/about/previous-releases) Node.js 24 as an LTS line. Use LTS releases for anything you deploy.

## Step 6: Docker Desktop

**Docker** runs applications in containers, which the DevOps chapter explains. Install Docker Desktop on Windows from [Docker's install page](https://docs.docker.com/desktop/setup/install/windows-install/). On the configuration page, choose "Use WSL 2 instead of Hyper-V". It needs WSL 2.1.5 or later (check with `wsl --version` in PowerShell), and it does not start by itself after the first install.

Then open Docker Desktop, go to Settings, Resources, WSL Integration, and switch on Ubuntu ([WSL backend guide](https://docs.docker.com/desktop/features/wsl/)). Test it from Ubuntu:

```bash
docker run hello-world
```

Docker's docs say the container prints a confirmation message and exits. A line such as `Hello from Docker!` near the top means it works.

Watch out: Docker's licence says commercial use of Docker Desktop in companies with more than 250 employees or more than 10 million USD in annual revenue needs a paid subscription ([source](https://docs.docker.com/get-started/introduction/get-docker-desktop/)). Check with your employer's policy before installing it on a work laptop.

## Step 7: PostgreSQL

Install the server and client inside Ubuntu, not on Windows ([Microsoft's database guide](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database)):

```bash
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres psql
```

The last command opens a `psql` prompt that looks like `postgres=#`. Type `\q` to leave. Check it with `sudo service postgresql status`, and start it again with the `start` command whenever it is not running (for example after a reboot). Ubuntu's package carries Ubuntu's choice of PostgreSQL version. If a lesson needs a specific version, the [PostgreSQL Ubuntu page](https://www.postgresql.org/download/linux/ubuntu/) shows how to add the project's own apt repository (it lists version 18 as an example).

## Check everything

Run these in Ubuntu. Each should print a version, not "command not found". The numbers below are examples; yours will differ.

```bash
git --version
ssh -T git@github.com
python3 --version
node --version
npm --version
docker --version
docker run hello-world
psql --version
code --version
```

```text
git version 2.x.y
Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
Python 3.x.y
v24.x.y
x.y.z
Docker version 2x.x.x, build abcdef
Hello from Docker!
psql (PostgreSQL) 1x.x
x.y.z
```

AWS setup comes later, in its own lesson on [AWS accounts, IAM and billing](../13-devops-and-cloud/03-aws/02-aws-account-iam-and-billing.md), because it involves billing and security choices that need explaining first.

## Working with AI

<div class="ai" markdown>

### Working with AI

Words to use: WSL2, distribution, package manager (`apt`), PATH, virtual environment, SSH key, daemon or service. They tell an assistant exactly which layer is broken.

Prompts to try:

- "I'm on Windows 11 with WSL2 Ubuntu. Running `docker run hello-world` in Ubuntu prints `Cannot connect to the Docker daemon`. Docker Desktop is open. What should I check, in order?"
- "`nvm: command not found` after installing nvm in Ubuntu on WSL. Here is the end of my `~/.bashrc`: (paste). What is missing?"

What to check:

- Which shell a command is for. An answer that gives `choco install` or `.exe` installers for a task in Ubuntu is aimed at the wrong place.
- Invented or outdated install URLs and version numbers. Compare with the official page before you run a `curl ... | bash` line.
- Advice to put project files under `/mnt/c`, or to install Docker Engine inside Ubuntu next to Docker Desktop. Docker's docs say to remove the second to avoid conflicts.
- Never paste your private key (`id_ed25519` without `.pub`) or a password into a prompt.

</div>
