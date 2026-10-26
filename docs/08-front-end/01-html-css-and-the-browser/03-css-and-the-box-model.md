# CSS and the box model

After this you can predict which CSS rule wins, work out the real size of a box, and use units, colours and variables without surprises.

Before this: [HTML](02-html.md).

## The idea

You write `color: red` on a paragraph and nothing happens. Somewhere else a rule says `color: blue`, and it wins. CSS stands for Cascading Style Sheets, and "cascading" is the answer: when several rules apply to one element, the browser has a fixed procedure for choosing. The other half of CSS is that every element is drawn as a rectangular box with layers around its content.

```text
+------------------------------------------+
|  margin (outside, transparent)           |
|  +------------------------------------+  |
|  |  border                            |  |
|  |  +------------------------------+  |  |
|  |  |  padding (inside, has        |  |  |
|  |  |  the element's background)   |  |  |
|  |  |  +------------------------+  |  |  |
|  |  |  |  content               |  |  |  |
|  |  |  |  (text, image)         |  |  |  |
|  |  |  +------------------------+  |  |  |
|  |  +------------------------------+  |  |
|  +------------------------------------+  |
+------------------------------------------+
```

## Key terms

A **selector** says which elements a rule applies to: `p` (type), `.note` (class), `#main` (id), `a:hover` (pseudo-class), `nav a` (descendant). A **declaration** is `property: value;`, and a **rule** is a selector with a block of declarations.

The **cascade** is the procedure that picks one value when several rules set the same property. **Specificity** is a score for how targeted a selector is. **Inheritance** passes some properties (such as `color` and `font-family`) from parent to child when the child sets none.

The **box model** says an element's size is content plus **padding**, **border** and **margin**. With `box-sizing: content-box` (the default), `width` sets the content only. With `box-sizing: border-box`, `width` includes padding and border.

A **CSS variable** (custom property) is a named value, such as `--accent: #0b5cad;`, read with `var(--accent)`.

## How it works

The cascade compares competing declarations in this order ([MDN: cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction)):

1. Importance and origin. A declaration marked `!important` beats a normal one, and the author's styles beat the browser defaults.
2. Specificity. The score is three counts, compared left to right: ids, then classes, attributes and pseudo-classes, then type selectors. So `#a` beats any number of classes, and `.a.b` beats `.a`.
3. Source order. If everything is equal, the later rule wins.

Inline `style=""` attributes beat any selector, which is why they are hard to override. Avoid `!important` in your own code; it starts an arms race.

```python
import re

def specificity(selector):
    ids = len(re.findall(r"#[\w-]+", selector))
    classes = len(re.findall(r"\.[\w-]+|\[[^\]]+\]|:(?!:)[\w-]+", selector))
    tags = len(re.findall(r"(?:^|[\s>+~])[a-zA-Z][\w-]*", selector))
    return (ids, classes, tags)

for s in ["p", ".note", "p.note", "#main .note p", "nav a:hover"]:
    print(f"{s:15} {specificity(s)}")
```

```text
p               (0, 0, 1)
.note           (0, 1, 0)
p.note          (0, 1, 1)
#main .note p   (1, 1, 1)
nav a:hover     (0, 1, 2)
```

This simplified counter ignores things like `:not()` and pseudo-elements, but it shows the idea: Python compares tuples left to right, as CSS does.

Box size is arithmetic. For `width: 200px; padding: 20px; border: 5px solid`, each side adds, so:

```python
width, padding, border = 200, 20, 5
print("content-box total:", width + 2*padding + 2*border)
print("border-box content:", width - 2*padding - 2*border)
```

```text
content-box total: 250
border-box content: 150
```

Most projects start with `*, *::before, *::after { box-sizing: border-box; }`, so a `width: 50%` box with padding stays 50% wide. Vertical margins of adjacent blocks also collapse into the larger one, not their sum ([MDN: margin collapsing](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Box_model/Mastering_margin_collapsing)).

Units:

| Unit | Meaning | Use for |
|---|---|---|
| `px` | one CSS pixel (not always one screen dot) | borders, small fixed gaps |
| `rem` | multiple of the root font size (16px by default) | font sizes, spacing, so they follow the user's setting |
| `em` | multiple of this element's font size | spacing that scales with its own text |
| `%` | share of the parent (for `width`) | fluid widths |
| `vw`, `vh` | 1% of the viewport width or height | full-screen sections |

Colours can be names, hex (`#0b5cad`), `rgb(11 92 173)` or `hsl(210 88% 36%)`. Hex and `rgb()` are the same colour in two notations; `hsl()` is easier to adjust by hand because lightness is one number.

Variables are declared on `:root` (the `<html>` element) and inherited everywhere:

```css
:root { --accent: #0b5cad; --gap: 1rem; }
a { color: var(--accent); }
.card { padding: var(--gap); }
```

Change `--accent` in one place and every use updates, including at runtime from JavaScript.

## Worked examples

<div class="example" markdown>

### Example 1: which colour wins

```html
<p id="intro" class="note">Hello</p>
```

```css
p { color: black; }
.note { color: green; }
#intro { color: blue; }
p.note { color: red; }
```

1. Score each selector: `p` is (0,0,1), `.note` is (0,1,0), `#intro` is (1,0,0), `p.note` is (0,1,1).
2. Compare left to right. `#intro` has an id and the others have none, so it wins.
3. The text is blue, even though `p.note` comes later in the file. Source order only breaks a tie.

Check: open DevTools, Elements panel, select the paragraph. The Styles pane lists every rule, and the losing declarations are struck through.

</div>

## Common mistakes

<div class="warning" markdown>

Watch out: forgetting that the default is `content-box`. A `width: 100%` box with padding becomes wider than its parent and scrolls sideways. Set `box-sizing: border-box`.

Watch out: using `px` for font sizes. Users who raise their browser's default text size get no change. Use `rem`.

Watch out: fighting specificity with `!important` or longer and longer selectors. Keep selectors short (one class) and fix the order instead.

</div>

## Working with AI

<div class="ai" markdown>

Words to use: specificity, cascade, inheritance, box-sizing, rem, custom property, computed style.

Prompts to try:

- "My `.button` background stays grey. Here are the matching rules from the DevTools Styles pane: [paste]. Which one wins by specificity and what is the smallest fix that avoids `!important`?"
- "Convert these pixel font sizes and margins to `rem` with a 16px base and put the colours in CSS variables on `:root`."

What to check:

- `!important` added as the fix. Ask for the specificity explanation instead.
- Selectors that depend on page structure (`div > div > ul li a`). They break as soon as the HTML changes.
- Mixed units in one calculation. Select the element and read the Computed tab in DevTools for the final pixel values.

</div>

## Quiz

1\. A `div` has `width: 300px; padding: 10px; border: 2px solid; box-sizing: content-box`. How wide is it on screen?

<details class="solution" markdown>
<summary>Answer</summary>

$300 + 2 \times 10 + 2 \times 2 = 324$ px. With `border-box` it would be 300 px.

</details>

2\. Which wins for a `<p class="a b">`: `.a.b { color: red }` or `.a { color: blue }`, written later?

<details class="solution" markdown>
<summary>Answer</summary>

Red. `.a.b` scores (0,2,0) and `.a` scores (0,1,0). Specificity is checked before source order.

</details>

3\. You set `border: 1px solid red` on a `<div>`. Do the paragraphs inside get a red border? And if you set `color: red` on the `div`?

<details class="solution" markdown>
<summary>Answer</summary>

No border: `border` is not inherited. The text turns red because `color` is inherited.

</details>

4\. A heading is `font-size: 2rem` and the root font size is 16px. The user changes their browser default to 20px. How big is the heading?

<details class="solution" markdown>
<summary>Answer</summary>

$2 \times 20 = 40$ px, up from 32 px. That is the reason to use `rem`.

</details>

## Lab

<div class="lab" markdown>

### Lab: measure a box

Goal: confirm the box arithmetic in DevTools. Time: about 15 minutes. Runs in: any browser.

1. Save the code below as `box.html` and open it.
2. Right-click the grey box, choose Inspect, and open the Computed tab. The box-model diagram shows the content size. Predict it first (answer: 200 px wide, 250 px total).
3. Remove the comment markers around `box-sizing: border-box;` and reload. Check that the box is now 200 px in total and the content is 150 px.
4. Change `--accent` in `:root` and watch the border colour change.
5. Cleanup: delete the file.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Box model</title>
  <style>
    :root { --accent: #0b5cad; }
    .box {
      width: 200px;
      padding: 20px;
      border: 5px solid var(--accent);
      background: #eee;
      /* box-sizing: border-box; */
    }
  </style>
</head>
<body>
  <div class="box">Content</div>
</body>
</html>
```

Expected result: 250 px wide with the default, 200 px wide after `border-box`.

<details class="solution" markdown>
<summary>Solution</summary>

Content-box: $200 + 40 + 10 = 250$ px, so the Computed tab shows 200 px for the content width. Border-box: the content is $200 - 40 - 10 = 150$ px and the outer width is 200 px. The height is set by the text, so it changes with the font.

</details>

</div>

## Where this shows up

- Arranging boxes in rows and grids is next, in [layout with flexbox, grid and responsive design](04-layout-flexbox-grid-and-responsive.md).
- Component libraries and utility classes are covered in the [frameworks and libraries landscape](../03-react/04-frameworks-and-libraries-landscape.md).
