# Software design

A cheat sheet for the chapter. Each section links to the lesson that teaches it.

## Clean code ([lesson](01-clean-code.md))

- Name for meaning: a verb for a function, a noun for a value.
- One job per function, nameable without "and".
- Named constants instead of magic numbers.
- Guard clauses instead of deep nesting.
- Comments say why, not what.
- Wait for the third repeat before merging similar code (DRY vs premature abstraction).
- Refactoring is only safe if behaviour is unchanged: compare outputs before and after.

## SOLID in one line each ([lesson](02-solid-principles.md))

| Letter | Principle | One-liner | Smell it fixes |
|---|---|---|---|
| S | Single Responsibility | One reason to change per class. | A class that computes, formats and saves. |
| O | Open/Closed | Add behaviour by adding code, not editing old code. | An `if/elif` chain edited for every new case. |
| L | Liskov Substitution | A subclass works wherever its parent does. | A subclass that raises where the parent did not. |
| I | Interface Segregation | Small interfaces, no unused methods. | Stub methods that raise `NotImplementedError`. |
| D | Dependency Inversion | Depend on an abstraction, pass it in. | A class that builds its own database or mailer. |

SOLID is overkill for small scripts, prototypes, and interfaces with one implementation and no test double.

## Pattern table ([lesson](03-design-patterns.md))

| Problem | Pattern | Example |
|---|---|---|
| Choose between algorithms at runtime | Strategy | Shipping cost classes with a common `cost()` |
| React to an event without the source knowing who listens | Observer | `EventEmitter`, order placed triggers email and stock update |
| Your code expects one interface, a library offers another | Adapter | Wrapping a gateway that takes cents |
| Callers should not name concrete classes | Factory | `make_exporter("csv")` |
| Business code is full of storage details | Repository | `repo.get(id)`, in-memory version for tests |
| Add behaviour around a function or object | Decorator | `@timed`, `@functools.cache` |
| A class builds its own dependencies | Dependency injection | `Signup(mailer)` |

Anti-patterns: god object (one class does everything), singleton overuse (hidden global state), a pattern with no problem behind it.

## Layers and MVC ([lesson](04-layered-architecture-and-mvc.md))

| Layer | Holds | Does not hold |
|---|---|---|
| Presentation | Routes, parsing, shape and type validation, status codes | SQL, business rules |
| Business | Rules and workflows | HTTP or database details |
| Data | Repositories, SQL, ORM | Rules, HTTP |

- Requests go down and results come up; each layer calls only the one below.
- MVC: the controller takes input, the model holds data and rules, the view renders the output.
- Django's "view" is the MVC controller and its "template" is the MVC view. Express has no built-in structure.
- Hexagonal: business logic in the centre, everything else plugs in through ports and adapters.

## Monolith or microservices ([lesson](05-monoliths-and-microservices.md))

- Start with a modular monolith: clear modules, small public interfaces.
- Splitting costs network calls (latency, partial failure), distributed data (no shared transaction), and per-service deployment and observability.
- Availability of a required chain of $n$ services at $a$ each is $a^n$.
- Split when scaling needs, team ownership or technical needs differ. Draw boundaries along business capabilities.
- Warning signs: a shared database, or services deployed together (a distributed monolith).
- Strangler fig: a router sends one path at a time to the new service until the old code is unused.
- Conway's law: systems mirror the communication structure of the teams that build them.

## Coupling, cohesion and refactoring ([lesson](06-coupling-cohesion-and-refactoring.md))

- Aim for low coupling between parts and high cohesion inside each part.
- Signs of tight coupling: far-away breakage, import cycles, cannot test alone, must deploy together.
- Refactor loop: tests pass, one small change, run tests, commit.
- No tests: write characterization tests first.
- Refactorings: extract function, rename, introduce parameter object, replace conditional with polymorphism.
- Technical debt: describe the symptom, the cost, and a bounded fix.
