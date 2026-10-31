# UI and UX design

Cheat sheet for the chapter. Lessons: [UI vocabulary and components](01-ui-vocabulary-and-components.md), [Visual design basics](02-visual-design-basics.md), [Design systems and Figma](03-design-systems-and-figma.md), [UX research and usability](04-ux-research-and-usability.md).

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| UI, UX | What the user sees and touches, and the whole experience of a task | [1](01-ui-vocabulary-and-components.md) |
| Visual hierarchy | The order the eye reads a page, set by size, weight, colour and position | [1](01-ui-vocabulary-and-components.md) |
| Affordance, signifier | What an element allows, and the visible clue that says so | [1](01-ui-vocabulary-and-components.md) |
| Primary, secondary, destructive action | The main action, an alternative, and one that deletes or overwrites | [1](01-ui-vocabulary-and-components.md) |
| CTA | The button or link that asks for the next step | [1](01-ui-vocabulary-and-components.md) |
| Breakpoint | Viewport width where the layout changes | [1](01-ui-vocabulary-and-components.md) |
| Type scale, spacing scale | Fixed lists of sizes and gaps (base 4 or 8 px) | [2](02-visual-design-basics.md) |
| Colour roles | Primary, neutral, semantic (success, warning, danger, info) | [2](02-visual-design-basics.md) |
| Contrast ratio | Brightness comparison of two colours, from 1 to 21 | [2](02-visual-design-basics.md) |
| Gestalt: proximity, similarity | Close items look related, alike items look like one kind | [2](02-visual-design-basics.md) |
| Design system | Shared components, values and rules, kept in sync between design and code | [3](03-design-systems-and-figma.md) |
| Design token | A named design value; primitive (raw) or semantic (role) | [3](03-design-systems-and-figma.md) |
| Frame, auto layout, component, variant, variable, Dev Mode | Figma containers, flexbox-like layout, reusable parts and their versions, token storage, developer view | [3](03-design-systems-and-figma.md) |
| Persona, journey map | A research-based user profile, and a user's steps with feelings and pain points | [4](04-ux-research-and-usability.md) |
| Low and high fidelity | Sketch or grey wireframe versus a realistic clickable prototype | [4](04-ux-research-and-usability.md) |
| Heuristic evaluation | Expert review against a rule list, with no users | [4](04-ux-research-and-usability.md) |

## Which component?

| Need | Use |
|---|---|
| Do something here / go somewhere | Button / link |
| Must decide before continuing | Modal dialog (`<dialog>`, `showModal()`) |
| Details or editing beside a list | Drawer (bottom sheet on phones) |
| Small interactive panel at a control | Popover |
| Short, non-essential label | Tooltip (never the only place for information) |
| Brief confirmation after an action | Toast, with `role="status"` |
| Pick one of a few / of many | Select / combobox |
| List of actions | Menu |
| Switch views of the same thing | Tabs |
| Long list: find a position / endless feed | Pagination / infinite scroll |
| Waiting, layout known / unknown / percent known | Skeleton / spinner / progress bar |

Every data screen has four states: loading, empty, error, success.

## Numbers

| Rule | Value | Source |
|---|---|---|
| Contrast, normal text (AA) | 4.5:1 | WCAG 2.2 SC 1.4.3 |
| Contrast, large text (AA) | 3:1 (18 pt, or 14 pt bold) | SC 1.4.3 |
| Contrast, UI components (AA) | 3:1 | SC 1.4.11 |
| Minimum target size (AA) | 24 by 24 CSS px | SC 2.5.8 |
| Body text size, line height | 16 px, about 1.5 | convention |
| Line length | 45 to 80 characters (80 max, Level AAA) | SC 1.4.8 |
| Spacing base | 4 or 8 px | convention |
| Users per usability round | about 5 (finds about 85%) | NN/g |

WCAG 2.2 is a W3C Recommendation (12 December 2024), as of 2026.

## Nielsen's 10 heuristics

1. Visibility of system status
2. Match between the system and the real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation

## Contrast in Python

```python
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(h):
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)
```

## Figma to CSS

| Figma | CSS |
|---|---|
| Auto layout, horizontal or vertical | `display: flex` with `flex-direction: row` or `column` |
| Gap, padding | `gap`, `padding` |
| Hug contents | `width: fit-content` |
| Fill container | `flex: 1` (main axis), `align-self: stretch` (cross axis) |
| Variant property | a prop |
| Variable and mode | a CSS custom property and a theme selector such as `[data-theme="dark"]` |

## Form rules

1. Visible label above each field; a placeholder is only a hint.
2. Right input `type` and `autocomplete`.
3. Validate on blur or submit, not on every keystroke.
4. Error in text, next to the field, saying what is wrong and how to fix it; keep the input; focus the first error.
5. Link with `aria-describedby` and set `aria-invalid="true"`.
6. Name buttons by their action ("Create account"), not "OK" or "Submit".
