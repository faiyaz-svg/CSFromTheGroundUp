// Make the checkboxes on the progress page clickable and remember them in
// this browser (localStorage). Each device keeps its own list.
const MF_PROGRESS_KEY = "mftgu-progress-v1"

function mfLoadProgress() {
  try {
    return JSON.parse(localStorage.getItem(MF_PROGRESS_KEY)) || {}
  } catch (e) {
    return {}
  }
}

function mfSaveProgress(state) {
  try {
    localStorage.setItem(MF_PROGRESS_KEY, JSON.stringify(state))
  } catch (e) {
    // Storage blocked (private mode): ticks last until the page closes.
  }
}

document$.subscribe(() => {
  const article = document.querySelector("article.md-content__inner")
  if (!article || !location.pathname.replace(/\/$/, "").endsWith("/progress")) return

  const state = mfLoadProgress()
  const items = article.querySelectorAll("li.task-list-item")
  let total = 0
  let done = 0

  items.forEach((li) => {
    const box = li.querySelector("input[type=checkbox]")
    const link = li.querySelector("a")
    if (!box || !link) return
    const key = new URL(link.href, location.href).pathname.replace(/^.*?\/CSFromTheGroundUp\//, "")
    total += 1
    box.disabled = false
    box.classList.add("mf-progress-box")
    if (key in state) box.checked = state[key]
    if (box.checked) done += 1
    box.addEventListener("change", () => {
      state[key] = box.checked
      mfSaveProgress(state)
      updateCount()
    })
  })

  const count = document.createElement("p")
  count.className = "mf-progress-count"
  const h1 = article.querySelector("h1")
  if (h1) h1.after(count)

  function updateCount() {
    const checked = article.querySelectorAll("input.mf-progress-box:checked").length
    count.textContent = `Finished in this browser: ${checked} of ${total} written lessons.`
  }
  updateCount()
})
