# Software engineering process

A cheat sheet for the chapter. Each section links to the lesson that teaches it.

## Requirements and user stories ([lesson](01-requirements-and-user-stories.md))

- Stakeholder: anyone affected by the software or able to affect it.
- Functional requirement: what the system does. Non-functional requirement: how well (performance, security, availability, accessibility), and only useful with a number.
- User story: "As a `<role>`, I want `<goal>`, so that `<benefit>`."
- Acceptance criteria in Gherkin: Given (state), When (one action), Then (observable result). Each Then should become one assertion.
- A use case is a longer form: one actor, one goal, a main flow and alternative flows.

| INVEST | Test |
|---|---|
| Independent | Can be built in any order |
| Negotiable | States the need, not the design |
| Valuable | A user or customer sees a benefit |
| Estimable | The team can size it |
| Small | Fits in days |
| Testable | You can say when it is done |

| Availability (30-day month) | Downtime allowed |
|---|---|
| 99% | 432 min |
| 99.9% | 43.2 min |
| 99.99% | 4.3 min |

Six clarifying questions: who is the user and what are they trying to do, what exactly should happen (with example values), how many or how fast, what happens on failure, what is out of scope, how will we know it is done.

A spec for an AI tool: context, story, scenarios (including failures), NFRs with numbers, out of scope, then tests before code.

## UML ([lesson](02-uml-class-and-sequence-diagrams.md))

| Question | Diagram | Mermaid |
|---|---|---|
| What exists and how is it related? | Class | `classDiagram` |
| Who calls whom, in what order? | Sequence | `sequenceDiagram` |
| What states can one thing be in? | State | `stateDiagram-v2` |
| What are the steps and decisions? | Activity | `flowchart` |

```text
A --> B       association
A o-- B       aggregation (part lives on its own)
A *-- B       composition (part dies with the whole)
A <|-- B      inheritance (B is an A)
A <|.. B      realization (B implements interface A)
A ..> B       dependency (brief use)
```

- Multiplicity: `1`, `0..1`, `0..*`, `1..*`. Visibility: `+` public, `-` private, `#` protected.
- Sequence arrows: `->>` call, `-->>` return, `-)` asynchronous send. Fragments: `alt`/`else`, `loop`.
- Mermaid: no semicolons in labels.
- Draw the 5 to 10 classes that matter, then compare every arrow with the code.

## SDLC models ([lesson](03-sdlc-models.md))

| Model | Idea | Fits | Weakness |
|---|---|---|---|
| Waterfall | Phases run once, in order | Fixed, well-understood requirements | Problems found late |
| V-model | Each design phase paired with a test level | Regulated and safety-critical work | Heavy documentation, slow to change |
| Iterative and incremental | Repeat in thin releasable slices | Requirements that emerge | Needs discipline on architecture |
| Spiral | Each loop starts with the biggest risk | Large technical unknowns | Overhead on small projects |
| Agile | Four manifesto values, short feedback loops | Unclear needs, available users | Misread as "no plan or documents" |
| DevOps and continuous delivery | Automated build, test, release, monitor loop | Web products with good tests | Needs automation and monitoring |

- V-model pairs: requirements with acceptance tests, system design with system tests, architecture with integration tests, module design with unit tests.
- Verification: built it right. Validation: built the right thing.
- Agile ceremonies are taught in [Agile, Scrum and Kanban](../../16-the-workplace/02-agile-scrum-and-kanban.md).
- Choose by three questions: how known are the requirements, what does a bug cost, how often can you release.
