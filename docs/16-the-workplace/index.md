# The workplace

How software teams work, how to communicate in code review and design docs, and how to prepare for hiring.

Before this folder: Developer tools and workflow.

The lessons and chapter cheat sheets for this folder are written in reading order.

<!-- lessons:start -->
## Lessons

1. [How software teams work](01-how-software-teams-work.md)
2. [Agile, Scrum and Kanban](02-agile-scrum-and-kanban.md)
3. [Tickets, estimates and planning](03-tickets-estimates-and-planning.md)
4. [Code review etiquette](04-code-review-etiquette.md)
5. [Design docs and writing](05-design-docs-and-writing.md)
6. [Working in a legacy codebase](06-working-in-a-legacy-codebase.md)
7. [Open source and licences](07-open-source-and-licences.md)
8. [Resume and portfolio](08-resume-and-portfolio.md)
9. [Technical interviews](09-technical-interviews.md)
10. [Behavioural interviews](10-behavioural-interviews.md)

<!-- lessons:end -->

## Cheat sheet

Roles and flow: [How software teams work](01-how-software-teams-work.md)

| Role | Owns |
|---|---|
| Software engineer | Building and maintaining code |
| Tech lead | Technical direction for a team |
| Engineering manager | People, growth, delivery |
| Product manager | What to build and in what order |
| Designer | User experience and interface |
| QA | Finding what breaks |
| SRE / DevOps | Deploying and running production |
| Data roles | Measuring what happened |

Flow: idea, prioritize, design, build, code review, CI, staging, production, monitor. A good help request: goal, symptom, what you tried, your guess, one question.

Agile and Scrum: [Agile, Scrum and Kanban](02-agile-scrum-and-kanban.md)

| Scrum | Items |
|---|---|
| Accountabilities | Product Owner, Scrum Master, Developers |
| Events | Sprint, Sprint Planning, Daily Scrum (15 min), Sprint Review, Sprint Retrospective |
| Artifacts and commitments | Product Backlog (Product Goal), Sprint Backlog (Sprint Goal), Increment (Definition of Done) |

A Sprint is one month or less. A Kanban WIP limit caps items per column so work finishes before more starts.

Tickets and estimates: [Tickets, estimates and planning](03-tickets-estimates-and-planning.md)

- A ticket has a problem, 2 to 5 testable acceptance criteria, scope with out of scope, and context.
- Story points are relative size, not hours. Give estimates as a range with a reason.
- Three-point estimate: $(	ext{best} + 4 	imes 	ext{likely} + 	ext{worst}) / 6$.
- Split work into pieces of one or two days. Use a spike to learn before estimating.

Code review: [Code review etiquette](04-code-review-etiquette.md)

- Author: small PR, self-review, description (why, what, tested, focus), tests, reply to every comment.
- Reviewer: description first, questions not orders, label `blocking:`, `question:`, `nit:`, `suggestion:`.
- AI-written code: check it solves the ticket, tests can fail, names exist, nothing sensitive.

Design docs: [Design docs and writing](05-design-docs-and-writing.md)

Sections: context, goals and non-goals, options (including do nothing), decision, risks and open questions, rollout. An ADR is a five-line record of one decision. Conclusion first, short paragraphs, name the decision you need.

Legacy code: [Working in a legacy codebase](06-working-in-a-legacy-codebase.md)

Find the entry point, trace one request, reproduce, write a characterization test, change one thing, open a small PR. Useful commands: `git grep`, `git blame path`, `git log --follow -p path`.

Open source and licences: [Open source and licences](07-open-source-and-licences.md)

| Licence | Family | Ask |
|---|---|---|
| MIT | Permissive | Keep notice |
| Apache-2.0 | Permissive | Keep notices, patent grant |
| GPL-3.0 | Strong copyleft | Share source of distributed derivatives |
| AGPL-3.0 | Network copyleft | Also for use over a network |

No licence means no permission. Sources: [choosealicense.com](https://choosealicense.com/), [spdx.org/licenses](https://spdx.org/licenses/). This is not legal advice.

Resume: [Resume and portfolio](08-resume-and-portfolio.md)

One page, single column, impact bullets (verb, what, technology, result), no photo or date of birth, tailor to the posting, pinned repositories with README, licence and no secrets.

Technical interviews: [Technical interviews](09-technical-interviews.md)

Steps: restate, ask, example, brute force, improve, agree, code, test (dry run and edge cases), complexity. When stuck, say what you know and ask. Follow each stage's AI-use rules.

Behavioural interviews: [Behavioural interviews](10-behavioural-interviews.md)

STAR is Situation, Task, Action (longest), Result. Keep a bank of six to eight stories of about two minutes. Ask questions back. For an offer: ask for it in writing, compare total compensation, cite public sources if you negotiate.
