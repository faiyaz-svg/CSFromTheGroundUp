// Run the SQL examples in the lessons against the sample databases.
//
//   node tools/check_sql.mjs                 check every docs/**/*.md
//   node tools/check_sql.mjs path/to/a.md    check only the given files
//
// A ```sql block is checked when it is
//   - inside <div class="sql-runner" data-db="X">,
//   - inside <details ... data-db="X">, or inside the <details id="..."> that a
//     runner points to with data-solution="...", or
//   - right after an HTML comment <!-- db: X -->.
// Put <!-- sql: expect-error --> before a block that is supposed to fail.
// Each block runs on a freshly seeded copy of database X (docs/assets/sql/X.sql).
// Exit code is 1 if any block fails unexpectedly.

import { readFileSync, readdirSync, statSync } from "node:fs"
import { join, dirname, relative, resolve } from "node:path"
import { fileURLToPath } from "node:url"
import { PGlite } from "@electric-sql/pglite"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..")
const SQL_DIR = join(ROOT, "docs", "assets", "sql")
const MAX_ROWS = 8
const MAX_CELL = 28

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name)
    if (statSync(p).isDirectory()) walk(p, out)
    else if (name.endsWith(".md")) out.push(p)
  }
  return out
}

// ---- find blocks -----------------------------------------------------------

const FENCE_OPEN = /^(\s*)(`{3,}|~{3,})\s*(?:sql|postgres|postgresql|pgsql)\b/i
const TAG_OPEN = /<(div|details)\b([^>]*)>/gi
const TAG_CLOSE = /<\/(div|details)\s*>/gi

function attr(tag, name) {
  const m = new RegExp(`\\b${name}\\s*=\\s*"([^"]*)"`).exec(tag)
  return m ? m[1] : null
}

function findBlocks(file) {
  const lines = readFileSync(file, "utf8").split(/\r?\n/)

  // Pass 1: which details id belongs to which database (via data-solution).
  const solutionDb = {}
  for (const line of lines) {
    for (const m of line.matchAll(TAG_OPEN)) {
      const sol = attr(m[2], "data-solution")
      const db = attr(m[2], "data-db")
      if (sol && db) solutionDb[sol] = db
    }
  }

  const blocks = []
  const stack = [] // open div/details tags: { db }
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const open = FENCE_OPEN.exec(line)
    if (open) {
      const indent = open[1].length
      const fence = open[2]
      const body = []
      let j = i + 1
      while (j < lines.length && !new RegExp(`^\\s*${fence[0]}{${fence.length},}\\s*$`).test(lines[j])) {
        body.push(lines[j].slice(0, indent).trim() === "" ? lines[j].slice(indent) : lines[j].trimStart())
        j++
      }
      // comments directly above the fence (or above the div/details that wraps it)
      let db = null
      let expectError = false
      for (let k = i - 1; k >= 0; k--) {
        const t = lines[k].trim()
        if (t === "" || /^<(div|details|summary)[^>]*>/i.test(t)) continue
        const c = /^<!--\s*(.*?)\s*-->$/.exec(t)
        if (!c) break
        const dm = /^db:\s*(\w+)$/.exec(c[1])
        if (dm) db = dm[1]
        if (/^sql:\s*expect-error$/.test(c[1])) expectError = true
      }
      if (!db) {
        for (let k = stack.length - 1; k >= 0; k--) {
          if (stack[k].db) { db = stack[k].db; break }
        }
      }
      if (db) blocks.push({ file, line: i + 1, db, expectError, sql: body.join("\n") })
      i = j
      continue
    }
    // track tags (only outside fences)
    const events = []
    for (const m of line.matchAll(TAG_OPEN)) {
      const tag = m[2]
      let db = attr(tag, "data-db")
      const id = attr(tag, "id")
      if (!db && id && solutionDb[id]) db = solutionDb[id]
      events.push({ pos: m.index, type: "open", db })
    }
    for (const m of line.matchAll(TAG_CLOSE)) events.push({ pos: m.index, type: "close" })
    events.sort((a, b) => a.pos - b.pos)
    for (const e of events) {
      if (e.type === "open") stack.push({ db: e.db })
      else stack.pop()
    }
  }
  return blocks
}

// ---- databases ------------------------------------------------------------

const snapshots = {}

async function freshDb(name) {
  if (!(name in snapshots)) {
    let seed
    try {
      seed = readFileSync(join(SQL_DIR, `${name}.sql`), "utf8")
    } catch {
      throw new Error(`no seed file docs/assets/sql/${name}.sql`)
    }
    const base = new PGlite()
    await base.exec(seed)
    try {
      snapshots[name] = { dump: await base.dumpDataDir("none"), seed }
    } catch {
      snapshots[name] = { dump: null, seed }
    }
    await base.close()
  }
  const snap = snapshots[name]
  if (snap.dump) return new PGlite({ loadDataDir: snap.dump })
  const db = new PGlite()
  await db.exec(snap.seed)
  return db
}

// ---- output ---------------------------------------------------------------

function fmt(v) {
  if (v === null || v === undefined) return "NULL"
  if (v instanceof Date) return v.toISOString().replace(/T00:00:00\.000Z$/, "").replace(/\.000Z$/, "").replace("T", " ")
  if (typeof v === "object") return JSON.stringify(v, (k, x) => (typeof x === "bigint" ? String(x) : x))
  return String(v)
}

function table(fields, rows) {
  const cols = fields.map((f) => f.name)
  const cut = (s) => (s.length > MAX_CELL ? s.slice(0, MAX_CELL - 1) + "~" : s)
  const shown = rows.slice(0, MAX_ROWS).map((r) => cols.map((c) => cut(fmt(r[c]))))
  const widths = cols.map((c, i) => Math.max(c.length, ...shown.map((r) => r[i].length)))
  const line = (cells) => "  " + cells.map((c, i) => c.padEnd(widths[i])).join(" | ").trimEnd()
  const out = [line(cols), "  " + widths.map((w) => "-".repeat(w)).join("-+-")]
  for (const r of shown) out.push(line(r))
  out.push(`  (${rows.length} row${rows.length === 1 ? "" : "s"}${rows.length > MAX_ROWS ? `, first ${MAX_ROWS} shown` : ""})`)
  return out.join("\n")
}

// ---- main -----------------------------------------------------------------

const args = process.argv.slice(2)
const files = args.length ? args.map((a) => resolve(a)) : walk(join(ROOT, "docs"))
const blocks = files.flatMap(findBlocks)

let failures = 0
for (const b of blocks) {
  const where = `${relative(process.cwd(), b.file)}:${b.line}  [${b.db}]${b.expectError ? " expect-error" : ""}`
  let db
  try {
    db = await freshDb(b.db)
    const results = await db.exec(b.sql)
    const withRows = results.filter((r) => r.fields && r.fields.length > 0)
    const last = withRows[withRows.length - 1]
    if (b.expectError) {
      failures++
      console.log(`FAIL ${where}\n  expected an error but the block ran`)
    } else {
      console.log(`ok   ${where}`)
      console.log(last ? table(last.fields, last.rows) : "  (no rows returned)")
    }
  } catch (e) {
    if (b.expectError) {
      console.log(`ok   ${where}\n  error as expected: ${String(e.message).split("\n")[0]}`)
    } else {
      failures++
      console.log(`FAIL ${where}\n  ${String(e.message).split("\n")[0]}`)
    }
  } finally {
    if (db) await db.close()
  }
}

console.log(`\n${blocks.length} block${blocks.length === 1 ? "" : "s"} checked, ${failures} failed.`)
process.exit(failures ? 1 : 0)
