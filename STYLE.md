# Writing style

These rules apply to every page in `docs/`. The reader is a capable adult (a 4th-year university CS student with an economics minor) who is preparing for the workforce and wants a solid general understanding of computers and software development. Don't talk down to them, and don't assume they already know the background.

The thesis of the book: with AI coding tools you need a good general understanding (concepts, vocabulary, mental models, what to check) more than every detail. Each page should leave the reader able to name things correctly, ask a precise question, and judge whether an answer is right.

The goal of each page is that the reader can do something new by the end of it, and understands why it works.

## Voice

- Talk to the reader as "you" in instructions ("Open a terminal and run..."). Use "we" when working through something together ("We want to find the slow query").
- Explanations are plain and direct. Definitions are stated precisely, in the standard wording a documentation page or university course would use, so the reader also learns to read real docs.
- Active voice, present tense, plain verbs: "run", not "execute"; "use", not "utilize".
- Be modest. Don't praise the material and don't hype tools, languages or AI.
- Use Canadian spelling: colour, centre, behaviour, practise (the verb) and practice (the noun). Keep the original spelling in names, titles and code ("color" in CSS stays "color").

## How to explain

1. Start with something concrete: a real situation or a small example, then a diagram if one helps, then plain words, then the formal definition. Keep the concrete part short.
2. The first time a term, command or symbol appears, say what it means in words.
3. Start from what the reader already knows, and say where an analogy stops working.
4. Give a procedure as numbered steps, then refer to the step numbers in the examples.
5. Explain Example 1 fully. A second example gets less commentary.
6. End every worked example with a check: run it, print it, or compare with what you predicted.
7. Name a common mistake at the step where it happens, not only in a separate list.
8. State each definition twice, once formally and once in plain words or with an example.
9. Never write "clearly", "obviously", "it is easy to see", "simply", "just" (as in "just run") or "trivially". Show the step instead.
10. Keep one idea per paragraph, in 2 to 5 sentences.
11. Aim for about 20 words per sentence on average, never more than about 40, and vary the length. A page of identical short sentences reads like a machine wrote it.
12. Put labels next to what they label: inside the diagram or beside the code line, not "see the figure above".
13. Leave out decoration. No fun facts, history asides or images that don't teach the idea.
14. One term per concept. If the book says "process", it doesn't also say "task" for the same thing, except once when introducing the term.
15. Say what to check. Where a tool or an AI can produce a wrong answer, name the specific way it goes wrong.

## Code and commands

- Every fenced block names its language: `python`, `javascript`, `typescript`, `sql`, `bash`, `powershell`, `text`, `json`, `yaml`, `dockerfile`, `html`, `css`. Use `text` for output, logs and anything that is not code.
- Shell commands carry no `$` or `>` prompt, so they copy cleanly. Their output goes in a separate `text` block under the command.
- Mark where a command runs when it matters: "In WSL (Ubuntu):" or "In PowerShell:". Labs assume WSL2 Ubuntu on Windows 11 unless the lesson says otherwise.
- Never invent a flag, option, function or API. Check with `--help`, `man`, or the official docs before writing it.
- Run every snippet before the page is committed. SQL blocks also go through `node tools/check_sql.mjs`.
- Keep snippets short: show the idea, not a full app. Prefer 3 to 15 lines. Name the file in a sentence before the block, not in a comment.
- Inline code (backticks) for commands, file names, function names, flags and values. Don't bold them.
- In prose, a shell variable such as `$HOME` always goes in backticks, so it isn't read as math.

## Facts that change

Versions, prices, free-tier rules, limits, default settings and ports in use change over time. Each lesson that uses one:

- takes it from the official docs at writing time (never from memory),
- states the year ("as of 2026"),
- links the source at the point of use.

This covers AWS free-tier limits, Docker and Python versions, LLM model names and context sizes, tax or fee figures in the workplace lessons, and similar items. If a number is not needed to learn the idea, leave it out.

## Math in sentences

KaTeX stays for the places where math is the subject: Big O, discrete math, probability, RSA. Everywhere else, use code or plain words.

- Put words between separate formulas. Not "Consider $S_q$, $q < p$" but "Consider $S_q$, where $q < p$".
- Don't start a sentence with a symbol. Not "$n$ is even" but "The number $n$ is even".
- In prose, write "for every", "there exists" and "implies" as words. The symbols appear only in the logic lessons, where the symbols are the subject.
- The sentence before a displayed formula is either complete or ends with a colon.
- One letter keeps one meaning within a lesson ($n$ is the input size everywhere in the algorithms chapter).
- Never write "any" when you mean "each" or "every".

## Markdown that works on the site and in VS Code

The same files are read in VS Code's preview and built into the website (Zensical with KaTeX and Mermaid). These rules keep both working.

### Math markup

- Inline math: `$n^2$`. No space just inside the dollar signs.
- Display math: `$$` on its own line, with a blank line before and after the block, and no blank lines inside it.
- Multi-line work: `$$\begin{aligned} ... \end{aligned}$$`.
- Never use `\(...\)` or `\[...\]` in the source.
- Don't put a letter or digit right after a closing `$`: write `$n$-th`, not `$n$th`.
- Inside a table, write absolute value as `\lvert x \rvert` and "divides" as `\mid`, because a plain `|` ends the table cell.
- Minus signs belong inside math: write `$-3$`, never a hyphen on its own.
- Escape the dollar sign in money amounts: `\$12.50`. An unescaped `$` can turn the text after it into math.

### Boxes

Use HTML containers with the `markdown` attribute. Leave a blank line after the opening tag and a blank line before the closing tag, or the content inside won't be processed.

Worked example (gray box), note (pale yellow), warning (pale red), Working with AI (pale blue-grey) and lab (outlined green):

```html
<div class="example" markdown>

### Example 1: reading a stack trace

...

</div>

<div class="note" markdown>

...

</div>

<div class="warning" markdown>

...

</div>

<div class="ai" markdown>

### Working with AI

...

</div>

<div class="lab" markdown>

### Lab: title

...

</div>
```

Collapsible solution, and collapsible code:

```html
<details class="solution" markdown>
<summary>Answer</summary>

...

</details>

<details class="code" markdown>
<summary>In code</summary>

...

</details>
```

Don't use `!!!`, `???` or `===` blocks. They need indented content, which VS Code shows as a raw code block. The SQL runner box is described in `LESSON_TEMPLATE.md`.

### Links, headings and diagrams

- Link between pages with relative paths to the `.md` file: `[hash tables](../03-data-structures/04-hash-tables.md)`.
- Keep code and punctuation out of headings that other pages link to, so the anchor stays stable.
- Mermaid code blocks for flowcharts, sequence diagrams, trees, graphs and state machines. Generated SVG files (from `tools/figures/`) for plots and anything Mermaid can't draw.

## Patterns to avoid

These are signs of AI-generated text, collected from Wikipedia's "Signs of AI writing" page (including its 2026 updates) and from studies of words that language models overuse (Kobak et al. 2024; Juzek and Ward 2025; Liang et al. 2024). One or two of them can appear by chance in human writing; the problem is when they pile up. Treat them as hard rules here anyway, because the whole book is drafted with AI help and would otherwise drift toward them.

### Words: never use

delve, tapestry, testament, pivotal, underscore (as a verb), intricate, intricacies, meticulous, meticulously, showcase, garner, bolster, interplay, vibrant, multifaceted, realm, groundbreaking, renowned, nestled, seamless, seamlessly, commendable, noteworthy, invaluable, transformative, unparalleled, unveil, harness (as a verb), elucidate, burgeoning, foster, leverage (in any sense), quietly, deep dive, boasts, "key role", "key factor", "key takeaway", "key insight", "key concept".

Technical senses are allowed:

- "agent harness" and "test harness" (nouns, with that exact meaning),
- "primary key", "foreign key", "API key", "encryption key", "SSH key",
- "robust" only in a technical sense (robust statistics), never as praise,
- the underscore character, steady state, critical section, spanning tree, "the inequality holds".

### Words: use rarely

crucial, vital, essential, comprehensive, notably, additionally, moreover, furthermore, consequently, ultimately, enhance, valuable, insights, practical, remarkable, nuanced, significant (outside statistics), robust (outside the technical sense above), powerful, modern, cutting-edge, best practice (name the practice and the reason instead). Prefer a plain word: "needed", "also", "so", "big".

### Phrases and patterns: never use

- "serves as", "stands as", "functions as" where "is" works. Write "A hash table is a map from keys to values", not "A hash table serves as...".
- Inflated importance: "plays a crucial role", "is a testament to", "is a cornerstone of", "sets the stage for", "marks a shift".
- A trailing "-ing" clause that adds vague commentary: "..., highlighting the importance of indexes", "..., underscoring...", "..., showcasing...".
- Disclaimers: "It's important to note that", "It's worth noting", "It is worth mentioning". State the warning directly instead: "Watch out: ...".
- Summary endings: a closing paragraph starting "In summary", "In conclusion", "To sum up" or "Overall,". Pages end with the lab and "Where this shows up", not a recap.
- Chatbot lines: "Great question", "Certainly!", "Let's dive in", "Let's unpack this", "I hope this helps", "Let me know". Plain "Let's check the output" is fine.
- Vague attribution: "developers agree", "experts say", "it is widely believed". Name the source or drop the claim.
- Negative parallelism: "not only X but also Y", "it's not X, it's Y", "no X, no Y, just Z". The one exception is correcting a specific mistake: "`==` compares values, not identity".
- False ranges: "from X to Y" where X and Y are not two ends of one scale ("from bits to the cloud"). Real ranges are fine: "from 0 to 255", "from client to server".
- Groups of three used for rhythm ("fast, simple, and scalable"). A real list of three things is fine.
- Hedging about sources: "while details are limited", "based on available information".
- Hype about AI or tools: "revolutionize", "game-changing", "supercharge", "10x", "magic". Say what the tool does and what it gets wrong.

### Punctuation and characters

- Em dashes (—) almost never: at most one per 500 words, and never with spaces around them. Studies cited on Wikipedia found Claude uses em dashes more than professional writers do, so this takes active effort. Use a comma, a colon, parentheses or a new sentence instead.
- En dashes (–) only in numeric ranges ("pages 10–12"), or write "10 to 12".
- Straight quotes and apostrophes only (`"` and `'`). Curly ones also break code and math like `f'(x)`.
- No emoji, and no unicode bullets (•). Use Markdown `-` lists.
- Few exclamation marks in prose. (In code, `!` is an operator and is fine.)

### Formatting

- Headings are in sentence case: "How it works", not "How It Works". Proper nouns keep their capitals. Allowed in headings: PostgreSQL, Postgres, SQL, NoSQL, Linux, Ubuntu, WSL, Windows, macOS, Git, GitHub, GitHub Actions, AWS, EC2, S3, IAM, RDS, VPC, Lambda, Docker, Kubernetes, Terraform, Python, JavaScript, TypeScript, Node.js, React, Vite, Express, FastAPI, Django, Redis, GraphQL, REST, HTTP, HTTPS, TCP, UDP, IP, TLS, DNS, SSH, JSON, YAML, CSV, HTML, CSS, DOM, API, JWT, OAuth, CORS, CSRF, XSS, OWASP, PIPEDA, RSA, ACID, MVCC, ETL, ELT, dbt, MCP, LLM, RAG, GPU, CPU, VS Code, Claude Code, Excel, LeetCode, Unicode, ASCII, Big O. Add a name here when a lesson needs one, instead of lowercasing it.
- A term is bold once, where it is defined, and nowhere else. Don't use bold for emphasis.
- Don't write bullet lists where every item starts with a bold label and a colon. Use a sentence, a table or a real subheading.
- Each page has one H1 (the title). Don't skip heading levels (H2 straight to H4).
- Don't put `---` lines between sections.
- Use a list for real steps or real collections of items. If prose reads fine, use prose.
- Use tables for real tables of values (latency numbers, status codes, ports, command options). A two-row table that should be a sentence should be a sentence.

### Don't over-correct

Wikipedia now also flags the opposite extreme: text that never uses a dash or a semicolon, uses only commas and periods, and keeps every sentence between 8 and 20 words. Write like a person explaining at a whiteboard: plain "is" and "has" sentences, a colon or semicolon or parentheses where they fit, an occasional "usually" or "often", and sentences of different lengths.

## The "Working with AI" box

Every lesson has one (`<div class="ai" markdown>`). It is part of the lesson, not an advert for AI.

- Words to use: the 3 to 6 terms from this lesson that make a prompt precise ("primary key", "idempotent", "race condition").
- Prompts to try: 2 or 3 concrete prompts a developer would really send, written with the lesson's vocabulary and with the context an AI needs (language, version, error text, what you already tried). Don't write vague prompts like "explain databases".
- What to check: a list of specific failure modes in the answer, such as "invented flags", "an index on the wrong column", "SQL built by string concatenation", "a deprecated API", "code that ignores the empty case". Each item is something the reader can verify, and says how.
- No hype. Don't claim that AI "understands" or "knows". Say it produces plausible text that must be checked.

## Self-check before a page is committed

1. Search the file for `—`, `“`, `”`, `‘`, `’`, emoji, and every word in "never use".
2. Search for "serves as", "stands as", "important to note", "worth noting", "In summary", "In conclusion", "Overall,", "not only", "Let's dive", "simply", "just run".
3. Check headings for Title Case (outside the allowlist) and lists for bold "Label:" items.
4. Check that every code fence names a language, no shell command has a `$` prompt, and output sits in its own `text` block.
5. Run every code block. Run every SQL block and SQL solution with `node tools/check_sql.mjs`. Run every Linux or Docker command in WSL, or flag it as unchecked.
6. Check that each changing fact has a source link and "as of 2026".
7. Recompute every number and table value (Python is fine).
8. Read the page once from top to bottom for rhythm. If several sentences in a row have the same length and shape, rewrite some of them.
