# AI-assisted development

Cheat sheet for the chapter. Lessons: [Claude Code](01-claude-code.md), [The plan, build, test, review workflow](02-plan-build-test-review-workflow.md), [Reviewing AI code](03-reviewing-ai-code.md), [AI security risks](04-ai-security-risks.md), [AI coding tools landscape](05-ai-coding-tools-landscape.md) (optional).

## Key terms

| Term | Meaning |
|---|---|
| Harness | The program around the model that provides tools, asks permission and feeds results back |
| Agentic coding tool | A tool that reads, edits and runs code in a loop, such as Claude Code |
| Permission mode | Setting for what runs without asking: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` |
| `CLAUDE.md` | Project instructions loaded every session; advice, not enforcement |
| Hook | Shell command run at a fixed point; exit code 2 on `PreToolUse` blocks the call |
| Subagent | Helper with its own context window that returns a summary |
| MCP server | External tool or data source connected over the Model Context Protocol |
| Spec, plan, contract | What to build, the proposed steps, the tests that define correct |
| Worktree | Second working directory with its own branch, one repository |
| Vacuous test | Test that passes whether or not the code is right |
| Hallucinated API or package | A made-up function, option or library name |
| Prompt injection | Text that overrides a model's instructions; indirect when hidden in content it reads |
| Excessive agency | More tools or permissions than the task needs |
| Slopsquatting | Registering a package name that models tend to invent |
| Least privilege, sandbox | Grant only what is needed, and limit what the process can reach |
| Assistant, agent, app builder | Suggests, acts in your repo, generates a whole app |

## Commands

| Task | Command |
|---|---|
| Install (PowerShell) | `irm https://claude.ai/install.ps1 \| iex` |
| Install (macOS, Linux, WSL) | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Check the install | `claude --version` |
| Start in plan mode | `claude --permission-mode plan` |
| Cycle permission modes | Shift+Tab |
| Start in a worktree | `claude --worktree feature-auth` |
| Add a remote MCP server | `claude mcp add --transport http <name> <url>` |
| Generate a starter `CLAUDE.md` | `/init` |
| Reset, summarize, restore | `/clear`, `/compact`, `/rewind` |
| Inspect | `/context`, `/permissions`, `/hooks`, `/mcp`, `/status` |
| Review | `/code-review`, `/security-review` |
| Plain Git worktree | `git worktree add ../name -b branch`, `git worktree list`, `git worktree remove ../name` |

## Files

| File | Scope |
|---|---|
| `CLAUDE.md` or `.claude/CLAUDE.md` | Project instructions, committed |
| `~/.claude/settings.json` | Your settings, all projects |
| `.claude/settings.json` | Shared project settings, committed |
| `.claude/settings.local.json` | Your settings for one project |
| `.claude/agents/`, `~/.claude/agents/` | Subagent definitions |
| `.mcp.json` | Project MCP servers |

## Review checklist

Does it do what was asked, edge cases, error handling, security (injection, secrets, auth), real APIs and packages, tests that fail when the code is wrong, smallest change that works, licence.

## OWASP LLM top 10 (2025)

LLM01 prompt injection, LLM02 sensitive information disclosure, LLM03 supply chain, LLM04 data and model poisoning, LLM05 improper output handling, LLM06 excessive agency, LLM07 system prompt leakage, LLM08 vector and embedding weaknesses, LLM09 misinformation, LLM10 unbounded consumption ([genai.owasp.org](https://genai.owasp.org/llm-top-10/)).

## Rules

- Scope a task: files, behaviour, how it is checked.
- Plan first when the change is more than one sentence of diff.
- Small steps, one commit each, tests run by you.
- After two failed corrections, `/clear` and restate the task.
- Use a hook or `deny` rule for anything that must never happen; `CLAUDE.md` is advice.
- Read every command before approving it; never use `bypassPermissions` outside a disposable VM or container.
- Verify every suggested package exists and is maintained before installing it.
- Keep secrets and customer data out of prompts; follow your employer's AI policy.
