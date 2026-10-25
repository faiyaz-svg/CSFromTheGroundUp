// Put "Previous" and "Next" buttons under the page title and at the end of
// the page, using the links the theme already puts in its footer.
document$.subscribe(() => {
  const article = document.querySelector("article.md-content__inner")
  if (!article || article.querySelector(".mf-prevnext")) return

  const prev = document.querySelector("a.md-footer__link--prev")
  const next = document.querySelector("a.md-footer__link--next")
  if (!prev && !next) return

  const makeBar = (extraClass) => {
    const bar = document.createElement("nav")
    bar.className = "mf-prevnext " + extraClass
    bar.setAttribute("aria-label", "Previous and next page")
    if (prev) {
      const a = document.createElement("a")
      a.className = "mf-prev"
      a.href = prev.href
      a.textContent = "‹ Previous"
      a.title = prev.getAttribute("aria-label") || ""
      bar.appendChild(a)
    }
    if (next) {
      const a = document.createElement("a")
      a.className = "mf-next"
      a.href = next.href
      a.textContent = "Next ›"
      a.title = next.getAttribute("aria-label") || ""
      bar.appendChild(a)
    }
    return bar
  }

  const h1 = article.querySelector("h1")
  if (h1) h1.after(makeBar("mf-prevnext--top"))
  article.appendChild(makeBar("mf-prevnext--bottom"))
})
