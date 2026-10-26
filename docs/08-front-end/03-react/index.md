# React

Cheat sheet for the chapter. Lessons: [Components, props and JSX](01-components-props-and-jsx.md), [State and hooks](02-state-and-hooks.md), [Data fetching and forms](03-data-fetching-and-forms.md), [Frameworks and libraries landscape](04-frameworks-and-libraries-landscape.md), [Web performance](05-web-performance.md).

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| Component | Function that takes props and returns JSX; name starts with a capital | [1](01-components-props-and-jsx.md) |
| Props | Inputs from parent to child; read-only | [1](01-components-props-and-jsx.md) |
| Children | The content between a component's tags | [1](01-components-props-and-jsx.md) |
| State | Data a component remembers between renders | [2](02-state-and-hooks.md) |
| Render, commit | React calls components, then updates the DOM with the differences | [2](02-state-and-hooks.md) |
| Effect | Code run after commit to sync with something outside React | [2](02-state-and-hooks.md) |
| Race condition | Result depends on which request finishes first | [3](03-data-fetching-and-forms.md) |
| Controlled input | Field whose value lives in state | [3](03-data-fetching-and-forms.md) |
| SSR, SSG, CSR, islands | When and where HTML is built | [4](04-frameworks-and-libraries-landscape.md) |
| LCP, INP, CLS | Core Web Vitals: loading, responsiveness, stability | [5](05-web-performance.md) |

## JSX rules

1. One root element per return; use `<>...</>` when you have no wrapper.
2. Close every tag: `<img />`.
3. `className`, `htmlFor`, camelCase events (`onClick`).
4. `{ }` holds a JavaScript expression; `style={{ color: "red" }}` is braces around an object.
5. Lists: `map` with a stable `key` (an id, not the index).
6. Conditions: ternary or `&&`; write `count > 0 && ...` so `0` is not printed.

## Hooks

| Hook | Use | Remember |
|---|---|---|
| `useState(init)` | Remember a value | Returns `[value, setValue]`; the value is a snapshot per render |
| `useEffect(fn, deps)` | Sync with the outside world | Return a cleanup; list every value read |
| `useRef(init)` | Hold a DOM node or mutable value | Changing `.current` does not re-render |
| `useMemo(fn, deps)` | Cache a calculation | Optimization only; measure first |
| `useCallback(fn, deps)` | Cache a function | Same |
| `useContext(ctx)` | Read a value from a parent provider | Re-renders when the value changes |
| Custom hook | Share stateful logic | Name starts with `use` |

Rules of hooks: call at the top level, never in `if`, loops or nested functions; only in components or custom hooks.

## Immutable updates

| Goal | Code |
|---|---|
| Add | `setItems([...items, x])` |
| Remove | `setItems(items.filter(i => i.id !== id))` |
| Change one | `setItems(items.map(i => i.id === id ? { ...i, done: true } : i))` |
| Object field | `setUser({ ...user, name })` |
| From previous value | `setN(c => c + 1)` |

## Fetching pattern

```jsx
useEffect(() => {
  const ctl = new AbortController();
  fetch(url, { signal: ctl.signal }).then(/* check r.ok */);
  return () => ctl.abort();
}, [url]);
```

## Core Web Vitals (as of 2026, 75th percentile)

| Metric | Good | Source |
|---|---|---|
| LCP | 2.5 s or less | [web.dev](https://web.dev/articles/vitals) |
| INP | 200 ms or less | [web.dev](https://web.dev/articles/vitals) |
| CLS | 0.1 or less | [web.dev](https://web.dev/articles/vitals) |
