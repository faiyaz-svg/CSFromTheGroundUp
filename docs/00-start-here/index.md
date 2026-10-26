# How to use this book

This is a self-study CS and software development book for one kind of reader: a 4th-year computer science student who is about to start work. It covers how computers run code, Linux, programming, algorithms, networking, web front ends and back ends, databases, security, cloud, system design, AI tools and how software teams work.

## The idea behind it

You will write much of your code with AI tools, and those tools are fast and often wrong. What protects you is a solid general understanding: the concepts, the right vocabulary, a working mental model of how the pieces fit, and a list of what to check. This book is written for that. It does not try to teach every detail, because details can be looked up. Each lesson leaves you able to name things correctly, ask a precise question and judge whether the answer is right.

Start with the three guide pages in this folder:

1. [Setting up your machine](setting-up-your-machine.md): Windows 11 with WSL2, VS Code, Git, Python, Node.js, Docker and PostgreSQL.
2. [Learning tech with AI](learning-tech-with-ai.md): the learn, ask, verify, explain loop and the privacy rules.
3. [Reading docs and error messages](reading-docs-and-error-messages.md): how to read documentation, stack traces and common errors.

## Reading order

The folders are numbered in reading order. Each one starts with a short overview of what it covers and what to read first.

| Folder | What it covers |
|---|---|
| 01 How computers work | Bits, hardware, and how code becomes a running program |
| 02 Operating systems and Linux | What an OS does, and the Linux command line |
| 03 Programming fundamentals | Python, thinking like a programmer, object-oriented ideas |
| 04 Developer tools and workflow | Git, dependencies, testing, code quality, spreadsheets |
| 05 Discrete math for CS | Logic, proofs, counting, graphs, modular arithmetic |
| 06 Data structures and algorithms | Big O, structures, algorithms, LeetCode patterns |
| 07 Networking | How the internet works, HTTP, TLS, debugging tools |
| 08 Front end | HTML, CSS, JavaScript, TypeScript, React |
| 09 Back end | Servers, APIs, authentication |
| 10 Databases, SQL and Postgres | The relational model, querying, schema design, indexes |
| 11 Data engineering and data science | Pipelines, warehouses, statistics, machine learning |
| 12 Security | Web security and cryptography |
| 13 DevOps and cloud | Containers, CI/CD, AWS, operations |
| 14 Software and system design | Clean code, architecture, scalability, case studies |
| 15 AI and LLMs | How LLMs work, building with them, using AI coding tools |
| 16 The workplace | Teams, code review, interviews |

Folders 01 to 03 are the base for everything after them. Folder 04 gives you the tools (Git, testing, dependencies) that every later lab uses. Folders 05 and 06 matter most for interviews. Folders 07 to 10 are the core of day-to-day work. Every folder builds only on the folders before it, and the order inside each folder follows the dependencies. If you already know a folder well, read its cheat sheet and move on; short lessons make skipping easy. Folders 01 and 05 are the likeliest to skip if the university courses are recent.

## How a lesson is laid out

Every lesson is a 10 to 15 minute read and follows the same shape:

1. The idea: a concrete situation and the mental model.
2. Key terms: each term defined in plain words, once.
3. How it works: the mechanism, with short code you can run.
4. Worked examples: Example 1 is explained step by step and ends with a check.
5. Common mistakes: what goes wrong and how to fix it.
6. Working with AI: words to use in a prompt, prompts to try, and what to check in the answer.
7. A 4-question quiz, with collapsible answers.
8. A 10 to 20 minute lab, with a collapsible solution.

Try the quiz before you open the answers, and try the lab before you open the solution. Attempting first is what makes the answer stick.

## Features on the site

- SQL runner. SQL lessons have boxes that run queries in your browser against a sample database. Nothing is installed.
- Progress. The [progress page](../progress.md) lists every lesson. Your progress is saved in your own browser only, so it does not follow you to another browser or device.
- Cheat sheets. Each chapter has an `index.md` that collects its rules, commands and tables for quick review.
- Optional lessons. Lessons marked optional go beyond what most jobs need. Skip them on a first pass.

## The sibling math book

Some lessons use math: Big O, discrete probability, RSA. This book teaches the part it needs. For more depth, [Math From the Ground Up](https://faiyaz-svg.github.io/MathFromTheGroundUp/) starts at arithmetic and goes up to university math, proofs and probability. Use it as an optional reference, not a prerequisite.
