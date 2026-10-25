// In-browser SQL runner (PGlite = Postgres compiled to WebAssembly).
//
// Markup (see tools/check_sql.mjs for the same rules):
//   <div class="sql-runner" data-db="shop" data-solution="sol-1" markdown>
//   ```sql
//   SELECT ...
//   ```
//   </div>
//   <details class="solution" id="sol-1" markdown> ... first sql block is the solution ... </details>
//
// PGlite is only downloaded when someone presses Run (about 15 MB, cached by the browser).
(function () {
  "use strict"

  // Keep this version in step with package.json (the version tools/check_sql.mjs uses).
  var PGLITE_VERSION = "0.5.8"
  var PGLITE_URL = "https://cdn.jsdelivr.net/npm/@electric-sql/pglite@" + PGLITE_VERSION + "/dist/index.js"
  var MAX_SHOWN = 500

  // Site root, taken from this script's own URL (pages are nested; the site lives in a subfolder).
  var SCRIPT_SRC = (document.currentScript && document.currentScript.src) || ""
  var SITE_ROOT = SCRIPT_SRC.replace(/javascripts\/sqlrunner\.js.*$/, "")

  var pgliteModule = null // the imported module, loaded once per tab
  var dbs = {} // db name -> { promise, queue }, rebuilt on every page

  function loadModule() {
    if (!pgliteModule) pgliteModule = import(PGLITE_URL)
    return pgliteModule
  }

  function seedText(name) {
    return fetch(SITE_ROOT + "assets/sql/" + name + ".sql").then(function (r) {
      if (!r.ok) throw new Error("Could not load the " + name + " database (" + r.status + ").")
      return r.text()
    })
  }

  function openDb(name) {
    return Promise.all([loadModule(), seedText(name)]).then(function (parts) {
      return parts[0].PGlite.create().then(function (pg) {
        return pg.exec(parts[1]).then(function () {
          return pg
        })
      })
    })
  }

  function getDb(name) {
    var entry = dbs[name]
    if (!entry) {
      entry = dbs[name] = { promise: null, queue: Promise.resolve() }
      entry.promise = openDb(name).catch(function (e) {
        delete dbs[name] // let the next Run try again
        throw e
      })
    }
    return entry
  }

  // Run fn(pg) after earlier work on the same db has finished.
  function withDb(name, fn) {
    var entry = getDb(name)
    var job = entry.queue.then(function () {
      return entry.promise.then(fn)
    })
    entry.queue = job.catch(function () {})
    return job
  }

  function resetDb(name) {
    return withDb(name, function (pg) {
      return seedText(name).then(function (seed) {
        return pg.exec("DROP SCHEMA public CASCADE; CREATE SCHEMA public;").then(function () {
          return pg.exec(seed)
        })
      })
    })
  }

  function closeAll() {
    Object.keys(dbs).forEach(function (name) {
      var entry = dbs[name]
      entry.promise.then(function (pg) { return pg.close() }).catch(function () {})
    })
    dbs = {}
  }

  // ---- results ----------------------------------------------------------

  var NUMERIC_TYPES = { 20: 1, 21: 1, 23: 1, 700: 1, 701: 1, 1700: 1 }

  function formatValue(v, typeId) {
    if (v === null || v === undefined) return null
    if (v instanceof Date) {
      var iso = v.toISOString()
      if (typeId === 1082) return iso.slice(0, 10)
      return iso.slice(0, 19).replace("T", " ")
    }
    if (typeof v === "object") {
      return JSON.stringify(v, function (k, x) { return typeof x === "bigint" ? String(x) : x })
    }
    return String(v)
  }

  // Of the statements in a run, the result of the last one that returns rows.
  function pickResult(results) {
    var last = null
    for (var i = 0; i < results.length; i++) {
      if (results[i].fields && results[i].fields.length > 0) last = results[i]
    }
    return last
  }

  function renderTable(res) {
    var wrap = document.createElement("div")
    wrap.className = "sqlr-table-wrap"
    var table = document.createElement("table")
    table.className = "sqlr-table"
    var thead = table.createTHead().insertRow()
    var numeric = []
    res.fields.forEach(function (f) {
      var th = document.createElement("th")
      th.textContent = f.name
      thead.appendChild(th)
      numeric.push(!!NUMERIC_TYPES[f.dataTypeID])
    })
    var tbody = table.createTBody()
    res.rows.slice(0, MAX_SHOWN).forEach(function (row) {
      var tr = tbody.insertRow()
      res.fields.forEach(function (f, i) {
        var td = tr.insertCell()
        var text = formatValue(row[f.name], f.dataTypeID)
        if (text === null) {
          td.textContent = "NULL"
          td.className = "sqlr-null"
        } else {
          td.textContent = text
          if (numeric[i]) td.className = "sqlr-num"
        }
      })
    })
    wrap.appendChild(table)
    return wrap
  }

  function plural(n, word) {
    return n + " " + word + (n === 1 ? "" : "s")
  }

  function showResults(out, results) {
    out.className = "sqlr-out"
    out.textContent = ""
    var res = pickResult(results)
    var note = document.createElement("p")
    note.className = "sqlr-note"
    if (res) {
      out.appendChild(renderTable(res))
      var n = res.rows.length
      note.textContent = plural(n, "row") + (n > MAX_SHOWN ? " (first " + MAX_SHOWN + " shown)" : "")
    } else {
      var lastRes = results[results.length - 1]
      var affected = lastRes && lastRes.affectedRows
      note.textContent = affected ? "Done. " + plural(affected, "row") + " affected." : "Done. The statement returned no rows."
    }
    out.appendChild(note)
  }

  function showError(out, message) {
    out.className = "sqlr-out sqlr-out--error"
    out.textContent = ""
    var p = document.createElement("p")
    p.className = "sqlr-error"
    p.textContent = message
    out.appendChild(p)
  }

  function showMessage(out, text, cls) {
    out.className = "sqlr-out" + (cls ? " " + cls : "")
    out.textContent = ""
    var p = document.createElement("p")
    p.className = "sqlr-note"
    p.textContent = text
    out.appendChild(p)
  }

  // ---- checking a solution ----------------------------------------------

  function normalizeCell(v, f) {
    var s = formatValue(v, f.dataTypeID)
    if (s === null) return "\u0000NULL"
    if (NUMERIC_TYPES[f.dataTypeID] && s !== "" && !isNaN(Number(s))) {
      return String(Number(Number(s).toPrecision(12)))
    }
    return s
  }

  function sameResult(a, b, ordered) {
    if (!a || !b) return !a && !b
    var namesA = a.fields.map(function (f) { return f.name })
    var namesB = b.fields.map(function (f) { return f.name })
    if (namesA.join("\u0001") !== namesB.join("\u0001")) return false
    if (a.rows.length !== b.rows.length) return false
    function rowsOf(r) {
      var list = r.rows.map(function (row) {
        return JSON.stringify(r.fields.map(function (f) { return normalizeCell(row[f.name], f) }))
      })
      return ordered ? list : list.sort()
    }
    var ra = rowsOf(a)
    var rb = rowsOf(b)
    for (var i = 0; i < ra.length; i++) if (ra[i] !== rb[i]) return false
    return true
  }

  function solutionSql(id) {
    var el = id && document.getElementById(id)
    if (!el) return null
    var code = el.querySelector(".language-sql code") || el.querySelector("pre code")
    return code ? code.textContent.trim() : null
  }

  // ---- one runner -------------------------------------------------------

  function setup(box) {
    if (box.getAttribute("data-sqlr") === "ready") return
    var dbName = box.getAttribute("data-db")
    var code = box.querySelector("pre code")
    if (!dbName || !code) return
    box.setAttribute("data-sqlr", "ready")

    var original = code.textContent.replace(/\s+$/, "")
    var solutionId = box.getAttribute("data-solution")

    var shown = code.closest(".highlight") || code.closest("pre")
    shown.hidden = true

    var ui = document.createElement("div")
    ui.className = "sqlr"

    var label = document.createElement("div")
    label.className = "sqlr-label"
    label.textContent = "SQL editor (" + dbName + " database)"

    var editor = document.createElement("textarea")
    editor.className = "sqlr-editor"
    editor.value = original
    editor.spellcheck = false
    editor.setAttribute("autocapitalize", "off")
    editor.setAttribute("autocomplete", "off")
    editor.setAttribute("aria-label", "SQL to run on the " + dbName + " database")

    function fit() {
      var lines = editor.value.split("\n").length
      editor.rows = Math.max(4, Math.min(lines + 1, 22))
    }
    fit()
    editor.addEventListener("input", fit)

    var bar = document.createElement("div")
    bar.className = "sqlr-bar"

    function button(text, cls, title) {
      var b = document.createElement("button")
      b.type = "button"
      b.className = "sqlr-btn " + cls
      b.textContent = text
      if (title) b.title = title
      return b
    }
    var runBtn = button("Run", "sqlr-run", "Run (Ctrl+Enter)")
    var resetBtn = button("Reset", "sqlr-reset", "Restore the original SQL and reload the data")
    var checkBtn = solutionId ? button("Check", "sqlr-check", "Compare with the expected result") : null
    bar.appendChild(runBtn)
    if (checkBtn) bar.appendChild(checkBtn)
    bar.appendChild(resetBtn)
    var hint = document.createElement("span")
    hint.className = "sqlr-hint"
    hint.textContent = "Ctrl+Enter runs"
    bar.appendChild(hint)

    var out = document.createElement("div")
    out.className = "sqlr-out sqlr-out--empty"
    out.setAttribute("role", "region")
    out.setAttribute("aria-live", "polite")
    out.setAttribute("aria-label", "Result")

    ui.appendChild(label)
    ui.appendChild(editor)
    ui.appendChild(bar)
    ui.appendChild(out)
    box.appendChild(ui)

    var busy = false
    function setBusy(on) {
      busy = on
      runBtn.disabled = resetBtn.disabled = on
      if (checkBtn) checkBtn.disabled = on
    }

    function loadingMessage() {
      var first = !dbs[dbName]
      showMessage(out, first ? "Loading the database (the first run downloads about 15 MB)..." : "Running...", "sqlr-out--busy")
    }

    function execSql(sql) {
      return withDb(dbName, function (pg) { return pg.exec(sql) })
    }

    function run() {
      if (busy) return
      setBusy(true)
      loadingMessage()
      execSql(editor.value)
        .then(function (results) { showResults(out, results) })
        .catch(function (e) { showError(out, e && e.message ? e.message : String(e)) })
        .then(function () { setBusy(false) })
    }

    function check() {
      if (busy) return
      var sol = solutionSql(solutionId)
      if (!sol) {
        showError(out, "This exercise has no solution to compare with.")
        return
      }
      setBusy(true)
      loadingMessage()
      var ordered = /\border\s+by\b/i.test(sol)
      execSql(editor.value)
        .then(function (mine) {
          return execSql(sol).then(function (expected) {
            var a = pickResult(mine)
            var b = pickResult(expected)
            showResults(out, mine)
            var verdict = document.createElement("p")
            var ok = sameResult(a, b, ordered)
            verdict.className = "sqlr-verdict " + (ok ? "sqlr-verdict--ok" : "sqlr-verdict--no")
            verdict.textContent = ok ? "Matches the expected result" : "Differs from the expected result"
            out.insertBefore(verdict, out.firstChild)
          })
        })
        .catch(function (e) { showError(out, e && e.message ? e.message : String(e)) })
        .then(function () { setBusy(false) })
    }

    function reset() {
      if (busy) return
      editor.value = original
      fit()
      setBusy(true)
      var loaded = !!dbs[dbName]
      if (!loaded) {
        // Nothing to re-seed yet: the first Run will load a fresh copy.
        out.className = "sqlr-out sqlr-out--empty"
        out.textContent = ""
        setBusy(false)
        return
      }
      showMessage(out, "Reloading the database...", "sqlr-out--busy")
      resetDb(dbName)
        .then(function () {
          out.className = "sqlr-out sqlr-out--empty"
          out.textContent = ""
        })
        .catch(function (e) { showError(out, e && e.message ? e.message : String(e)) })
        .then(function () { setBusy(false) })
    }

    runBtn.addEventListener("click", run)
    resetBtn.addEventListener("click", reset)
    if (checkBtn) checkBtn.addEventListener("click", check)
    editor.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault()
        run()
      }
    })
  }

  var lastPath = null

  function init() {
    // A new page: the old page's databases are no longer needed.
    if (location.pathname !== lastPath) {
      closeAll()
      lastPath = location.pathname
    }
    var boxes = document.querySelectorAll("div.sql-runner[data-db]")
    for (var i = 0; i < boxes.length; i++) setup(boxes[i])
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(init) // Material instant navigation: runs on every page view
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init)
  } else {
    init()
  }
})()
