# Site design

The site should feel like W3Schools: flat, plain, quick to scan, with the content doing the work. It should not look like a generic AI-generated site. It shares its look with the sibling math book. The styles live in `docs/stylesheets/site.css`; the scripts that change the page are `docs/javascripts/prevnext.js`, `docs/javascripts/progress.js` and `docs/javascripts/sqlrunner.js`.

## Layout

- A white header with the site title, the light/dark toggle, search and the GitHub link.
- A dark bar of subject tabs under the header (`#282a35`, white uppercase labels). The current tab has a light gray background with dark text. Tab labels are short (Hardware, Linux, Python, SQL, Cloud) so they fit on one line on a laptop.
- A light gray left sidebar (`#ebedee`) listing the chapters and lessons of the current tab. The current lesson is white with a green left border.
- The page title is large and light (weight 400). Section headings are plain and smaller.
- Under every page title there is an outlined "Previous" button on the left and a green "Next" button on the right (`#04aa6d`). The same pair repeats at the bottom of the page.
- The home page is a table of contents, like the first page of a book.

## Boxes

| Box | Look | Markdown |
|---|---|---|
| Worked example | Gray background, 5px corners | `<div class="example" markdown>` |
| Note | Pale yellow, no icon | `<div class="note" markdown>` |
| Warning | Pale red with a red left border, no icon | `<div class="warning" markdown>` |
| Working with AI | Pale blue-grey with a slate-blue left border, no icon. Never purple or indigo | `<div class="ai" markdown>` |
| Lab | White with a thin border and a green left border, a little thicker than a solution box | `<div class="lab" markdown>` |
| Solution | White, thin border, green left border, collapsible | `<details class="solution" markdown>` |
| In code | Same as a solution | `<details class="code" markdown>` |
| SQL runner | A `sql` code block made editable, with Run and Reset buttons and a results table. Flat, gray panel, green Run button | `<div class="sql-runner" data-db="shop" markdown>` |

## Colour

One dark colour (the tab bar and footer), one accent (green), and gray neutrals. Links are dark green and underlined. Inline code is dark red on light gray. The AI box uses a pale blue-grey (a cool gray with a hint of blue, like `#e8eef3`) and nothing in the violet range. Dark mode uses the same layout with dark grays and a slightly lighter green; no neon and no glow.

## Figures

Plots and diagrams that Mermaid can't draw are SVG files drawn with matplotlib. Each lesson that needs them has a script, `tools/figures/<folder>/<lesson-slug>.py`, which imports `tools/figures/figstyle.py` for the colours and fonts and writes to `docs/assets/figures/<folder>/<lesson-slug>-<name>.svg`. Re-run the script after changing it and commit the script with the SVG.

- Embed with a relative image link and alt text that says what the figure shows: `![Latency of L1 cache, RAM and SSD on a log scale](../../assets/figures/01-how-computers-work/memory-hierarchy-latency.svg)`.
- Label points, lines and boxes inside the figure, next to what they name. Keep the legend off the data.
- Use the palette in `figstyle.py` (green first, then blue, red, orange). No titles inside the figure; the text around it says what it is.
- Mermaid stays the tool for flowcharts, sequence diagrams, trees, graphs and state machines.

## Things to avoid

These are common signs of AI-generated web design. Don't add any of them.

- Gradients of any kind, glow or aurora backgrounds, glass blur effects, neon colours on dark backgrounds.
- Purple, indigo or violet anywhere (the default colour of many generators). This includes the AI box.
- Emoji used as icons, bullets or headings. Use the theme's built-in icons sparingly, or none.
- A centered "hero" section with a pill badge, a big tagline and three feature cards with icons, followed by a call-to-action button.
- The Inter or Geist fonts. The site uses the system font stack, like W3Schools (Segoe UI on Windows, the system font on phones).
- Drop shadows, heavily rounded corners (more than 5px), and cards nested inside cards.
- Marketing language in any site text: "unlock", "elevate", "master", "supercharge", "your journey", "level up".
- Giving every element the same visual weight. The title leads, then headings, then body text.

## Checking a change

Run `zensical serve`, then look at a lesson page at desktop width (about 1400px) and phone width (about 390px), in light and dark mode. Check that math and diagrams render, solutions open and close, the SQL runner runs and resets, the tabs fit, and the Previous and Next buttons appear.
