// Render only the spans Arithmatex marked as math, so a literal \$ in text
// (money amounts) is never picked up as a math delimiter.
document$.subscribe(({ body }) => {
  body.querySelectorAll(".arithmatex").forEach((el) => {
    renderMathInElement(el, {
      delimiters: [
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    })
  })
})
