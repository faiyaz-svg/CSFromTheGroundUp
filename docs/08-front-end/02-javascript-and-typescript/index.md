# JavaScript and TypeScript

Cheat sheet for the chapter. Snippets were run on Node 24.15; TypeScript is 7.0 and Vite is 8.3 (as of 2026).

## Lessons

1. [JavaScript for Python programmers](01-javascript-for-python-programmers.md)
2. [The DOM and events](02-the-dom-and-events.md)
3. [Async JavaScript and the event loop](03-async-javascript-and-the-event-loop.md)
4. [TypeScript](04-typescript.md)
5. [npm, bundlers and Vite](05-npm-bundlers-and-vite.md)

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| Coercion | Automatic type conversion by `==` and `+` | [1](01-javascript-for-python-programmers.md) |
| Truthy, falsy | Falsy: `false`, `0`, `""`, `null`, `undefined`, `NaN`, `0n`; all else truthy, including `[]` and `{}` | [1](01-javascript-for-python-programmers.md) |
| Destructuring, spread | Unpack into variables; copy items or properties into a new array or object | [1](01-javascript-for-python-programmers.md) |
| DOM | The browser's tree of objects for a page | [2](02-the-dom-and-events.md) |
| Bubbling, delegation | Events travel up to ancestors; one parent listener handles many children | [2](02-the-dom-and-events.md) |
| Event loop | Runs one task, then all microtasks, then the next task | [3](03-async-javascript-and-the-event-loop.md) |
| Promise | A value that is pending, then fulfilled or rejected | [3](03-async-javascript-and-the-event-loop.md) |
| Narrowing | The checker refines a union type inside an `if` or `switch` | [4](04-typescript.md) |
| Type erasure | Types are removed before the program runs | [4](04-typescript.md) |
| Bundler, tree shaking | Combine modules from an entry file; drop unused exports | [5](05-npm-bundlers-and-vite.md) |
| HMR | Swap a changed module into the running page | [5](05-npm-bundlers-and-vite.md) |

## Python and JavaScript syntax

| Python | JavaScript |
|---|---|
| `x = 1` | `let x = 1` or `const x = 1` |
| `None` | `null` (set to nothing), `undefined` (never set) |
| `==` | `===` (value, no coercion) |
| `and`, `or`, `not` | `&&`, `\|\|`, `!` |
| `x if c else y` | `c ? x : y` |
| `a or b` (falsy default) | `a \|\| b`; use `a ?? b` for null or undefined only |
| `d.get("k")` | `obj.k` or `obj?.k` |
| `len(xs)` | `xs.length` |
| `[f(x) for x in xs if c(x)]` | `xs.filter(c).map(f)` |
| `functools.reduce(f, xs, 0)` | `xs.reduce(f, 0)` |
| `for x in xs:` | `for (const x of xs) { }` |
| `for k, v in d.items():` | `for (const [k, v] of Object.entries(obj)) { }` |
| `a, *rest = xs` | `const [a, ...rest] = xs` |
| `{**d, "k": 1}` | `{ ...obj, k: 1 }` |
| `f"{x}"` | `` `${x}` `` |
| `lambda x: x * 2` | `x => x * 2` |
| `def f(x=1):` | `function f(x = 1) { }` |
| `try / except / finally` | `try { } catch (e) { } finally { }` |
| `from m import f` | `import { f } from "./m.js"` |
| `x // y` | `Math.floor(x / y)` |
| `print(x)` | `console.log(x)` |
| `xs.sort()` | `xs.sort((a, b) => a - b)` for numbers; the default compares strings |

## DOM and events

```javascript
const el = document.querySelector("#id");       // first match or null
const all = document.querySelectorAll("li");     // all matches
el.textContent = "text";                         // safe; innerHTML parses HTML
el.classList.add("a"); el.classList.toggle("b"); // style by classes
el.addEventListener("click", (event) => {
  event.target;          // where it started
  event.currentTarget;   // where this listener is attached
  event.preventDefault();// cancel default (form submit, link)
});
```

## Async

```javascript
const res = await fetch(url);                 // rejects only on network failure
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const data = await res.json();
const [a, b] = await Promise.all([f(), g()]); // parallel; rejects on first failure
```

Order: synchronous code, then all microtasks (promise callbacks, after `await`), then the next task (timers, events).

## TypeScript

| Syntax | Meaning |
|---|---|
| `let x: number` | Annotation |
| `interface U { id: number; email?: string }` | Object shape, optional field |
| `type Id = number \| string` | Alias, union |
| `function f<T>(xs: T[]): T \| undefined` | Generic |
| `unknown`, `any` | Must narrow before use; checking off |
| `npx tsc --noEmit` | Type check only |
| `node file.ts` | Runs with types stripped, no check; no `enum` |

## npm and Vite

| Command | What it does |
|---|---|
| `npm create vite@latest app -- --template vanilla-ts` | Scaffold a project |
| `npm install`, `npm ci` | Install from `package.json`; install exactly from the lock file |
| `npm install -D pkg` | Add a dev dependency |
| `npm run dev`, `build`, `preview` | Dev server with HMR; bundle to `dist/`; serve `dist/` |
