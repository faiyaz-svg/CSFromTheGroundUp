# Dates and times

Cheat sheet for the chapter. Each lesson teaches the idea; this page collects the terms and rules.

## Lessons

1. [How computers keep time](01-how-computers-keep-time.md): Unix time, UTC, wall and monotonic clocks, NTP, leap seconds, 2038.
2. [Time zones and daylight saving](02-time-zones-and-daylight-saving.md): IANA zones, DST gaps and overlaps, what to store.
3. [Dates in Python and JavaScript](03-dates-in-python-and-javascript.md): ISO 8601, naive vs aware, `Date` traps, Temporal, injected clocks.

## Key terms

| Term | Meaning |
|---|---|
| Unix time / epoch | Seconds since 1970-01-01 00:00:00 UTC |
| UTC | Reference time, the same everywhere |
| Wall clock | The current date and time, can jump |
| Monotonic clock | Only moves forward, for durations |
| NTP / clock drift | Protocol that corrects the clock / slow gain or loss between corrections |
| Leap second | Second added to UTC, last one 31 December 2016 |
| 2038 problem | Signed 32-bit `time_t` overflows at 03:14:07 UTC, 19 January 2038 |
| UTC offset | Difference from UTC now, such as `-05:00` |
| IANA zone | Region name with its offset history, such as `America/Toronto` |
| Gap / overlap | Local times that never happen / that happen twice |
| `fold` | Python flag: 0 first occurrence, 1 second |
| Naive / aware | Datetime without / with a zone or offset |
| ISO 8601 / RFC 3339 | Standard date text / strict internet profile with `Z` or offset |
| Temporal | New JavaScript date API, not Baseline as of 2026 |
| Injected clock | A clock object passed in so tests can fix the time |

## Syntax

| Task | Python | JavaScript |
|---|---|---|
| Now (instant) | `datetime.now(timezone.utc)` | `new Date()`, `Date.now()` (ms) |
| Elapsed time | `time.monotonic()` | `performance.now()` |
| Parse RFC 3339 | `datetime.fromisoformat(s)` | `new Date(s)` |
| To text | `dt.isoformat()` | `d.toISOString()` |
| Convert zone | `dt.astimezone(ZoneInfo("America/Toronto"))` | `Intl.DateTimeFormat` with `timeZone` |
| Zone data | `pip install tzdata` (needed on Windows) | built into the runtime |

## Rules

- Measure durations with a monotonic clock, never the wall clock.
- Store past instants as UTC. Store future local events as local time plus an IANA zone name.
- Convert to a zone only when displaying. Never store offsets or `EST`-style abbreviations for a user.
- Use RFC 3339 strings with `Z` or an offset in JSON. A date-only string means a calendar day.
- Use `timedelta(days=1)` for "same time tomorrow" and hours for elapsed time.
- Keep datetimes aware. Never mix naive and aware values.
- Pass a clock into code that needs the time, so tests can fix it.
- JavaScript months start at 0, and `Date` is mutable.

## Toronto 2026

| Change | Date | Offset after |
|---|---|---|
| Spring forward (02:00 to 03:00) | Sunday 8 March | UTC-4 (EDT) |
| Fall back (02:00 to 01:00) | Sunday 1 November | UTC-5 (EST) |
