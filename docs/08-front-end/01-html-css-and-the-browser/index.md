# HTML, CSS and the browser

Cheat sheet for the chapter. Lessons: [How browsers render pages](01-how-browsers-render-pages.md), [HTML](02-html.md), [CSS and the box model](03-css-and-the-box-model.md), [Layout with flexbox, grid and responsive design](04-layout-flexbox-grid-and-responsive.md), [Accessibility](05-accessibility.md).

## Rendering pipeline

Network, parse HTML to DOM, parse CSS to CSSOM, render tree, layout, paint, composite. See [How browsers render pages](01-how-browsers-render-pages.md).

| Script tag | Parsing | Runs |
|---|---|---|
| `<script src>` | blocked | at once, in order |
| `<script defer src>` | not blocked | after parsing, in order |
| `<script async src>` | not blocked | when downloaded, any order |

| Change | Reruns |
|---|---|
| `width`, `margin`, adding elements | layout, paint, composite |
| `color`, `background-color` | paint, composite |
| `transform`, `opacity` | composite |

## HTML

- Skeleton: `<!doctype html>`, `<html lang="en">`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, `<title>`.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`. One `<h1>`, no skipped heading levels.
- Images: `alt` text for meaning, `alt=""` for decoration, `width` and `height` to reserve space.
- Forms: `<label for>` plus `id`; `name` is the key sent; `required`, `type`, `min`, `max`, `pattern`. Browser validation is a convenience, and the server checks again.

## CSS

| Selector | Example | Specificity (ids, classes, types) |
|---|---|---|
| type | `p` | (0,0,1) |
| class, attribute, pseudo-class | `.note`, `a:hover` | (0,1,0) |
| id | `#main` | (1,0,0) |

Cascade order: importance and origin, then specificity, then source order. Inline styles beat selectors.

Box size with `width: 200px; padding: 20px; border: 5px`: `content-box` is 250 px wide, `border-box` is 200 px wide. Start projects with `* { box-sizing: border-box; }`.

| Unit | Relative to |
|---|---|
| `px` | a CSS pixel |
| `rem` | root font size (16px by default) |
| `em` | this element's font size |
| `%` | the parent |
| `vw`, `vh` | 1% of the viewport |

Variables: `:root { --accent: #0b5cad; }` then `color: var(--accent);`.

## Layout

| Need | Use |
|---|---|
| Items in one row or column | `display: flex`, `justify-content` (main axis), `align-items` (cross axis), `gap`, `flex-wrap` |
| Rows and columns together | `display: grid`, `grid-template-columns: 1fr 2fr`, `repeat(auto-fit, minmax(200px, 1fr))` |
| Different layout on wide screens | `@media (min-width: 48rem) { ... }`, written mobile first |

## Accessibility

- POUR: Perceivable, Operable, Understandable, Robust. Target WCAG 2.2 Level AA.
- Contrast on AA: 4.5:1 normal text, 3:1 large text and UI components.
- Order of work: semantic HTML, labels and alt text, contrast, keyboard and focus, ARIA only when HTML cannot say it.
- Test with Lighthouse or axe, then the keyboard, then a screen reader (NVDA, VoiceOver).
- AODA: public websites of designated public sector organizations and of organizations with 50 or more employees, WCAG 2.0 AA ([ontario.ca](https://www.ontario.ca/page/how-make-websites-accessible)).
