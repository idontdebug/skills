---
name: adversarial-review
description: >-
  Explicit-invocation adversarial ("red team") review for spec-shaped documents — OpenSpec change
  proposals, design docs, PRDs, RFCs. Use ONLY when the user explicitly asks for an adversarial /
  red-team review, to "poke holes in" or "stress-test" a written proposal, or names this skill
  directly. Do NOT auto-trigger just because the user is writing or editing a spec/design doc — this
  is a deliberate, heavyweight action the user opts into, not a background check. When invoked, it
  reads the target document(s) end to end, builds an inventory of key decisions/assumptions/claims,
  attacks each one with four techniques (assumption mining, failure-scenario construction, devil's
  advocate counter-proposals, ambiguity/gap detection), cross-checks claims about "current behavior"
  against the actual codebase when one is available, self-verifies to discard unfounded nitpicks, and
  reports the surviving findings via the ReportFindings tool. It never edits the reviewed document —
  output is a findings report only. Not for reviewing code diffs (use code-review/security-review for
  that) or for interactively interviewing the user about an unwritten idea (use grilling for that).
---

# adversarial-review — red-team a spec-shaped document

## What this skill does

The user hands you a written document that argues for a plan — an OpenSpec change proposal, a design
doc, a PRD, an RFC. Your job is not to summarize it or politely note a few nits. It's to attack it: find
the assumptions it's quietly resting on, construct scenarios where it fails, build a stronger competing
alternative for its key decisions, and catch ambiguous or uncovered requirements. Then report only the
findings that survive your own scrutiny, ranked by severity, through `ReportFindings`.

This is scoped narrowly on purpose: documents that describe **a decision or a plan for future work**.
It is not a general-purpose text reviewer (yet), not a code reviewer, and not a copy editor.

## When to use this

Only when explicitly asked — "adversarially review this proposal", "红队一下这份设计文档",
"帮我对抗性审查一下这个 OpenSpec change", "stress-test this RFC before I send it", or the user names
this skill directly. Never trigger just because the user is drafting or editing a spec/design document;
this is an expensive, deliberate multi-pass analysis the user opts into, not a passive linter.

If the request is instead "help me think through an idea I haven't written down yet" via live back-
and-forth, that's `grilling`, not this skill. If the target is a code diff, that's `code-review` or
`security-review`.

## Scope

**In scope**: OpenSpec change proposals, design docs, PRDs, RFCs, and similar documents whose job is to
justify a future decision. A document counts if it has claims, assumptions, or decisions that can be
argued with.

**Out of scope**: code diffs (correctness/security review belongs to `code-review`/`security-review`),
purely narrative text (blog posts, meeting notes, emails) — this may be widened later once the
technique proves out on spec-shaped documents, but don't stretch it there yet on your own initiative.

**Never edits the document.** This skill only produces a findings report. Whether and how to act on a
finding is the document author's call — don't add a "fix it for me" mode even if it seems convenient in
the moment.

## Input handling

Accept one or more file/directory paths as the review target. If given a directory (e.g. an OpenSpec
change directory), read every text file inside it as part of the same review — don't assume a fixed
file layout like `proposal.md`/`tasks.md`/`design.md`; read what's actually there. If no path is given,
ask which document to review rather than guessing.

If the working directory is part of a code repository, plan to cross-check claims against it (see
Stage 3 below). If the document clearly lives outside any codebase (a standalone docs repo), skip that
stage — don't go looking for a codebase that isn't there.

## The five-stage pipeline

Run these in order. Don't collapse them into a single unstructured pass — the explicit checkpoints
(especially the self-verification stage) are what keep this skill's output sharp instead of noisy.

### 1. Read everything, build the inventory

Read every target document fully before generating any findings. Extract an inventory of:

- **Key decisions** — "we chose X over the alternatives"
- **Implicit assumptions** — technical, data, or organizational preconditions the plan quietly depends
  on but never states
- **Claims about the current state** — "the system currently can't do X", "only module Y needs to
  change"
- **Acceptance criteria / boundary conditions** — what "done" or "correct" is supposed to mean

This inventory is the input to every later stage — don't skip straight to critiquing prose.

### 2. Attack every inventory item with the four techniques

Work through the inventory and apply whichever of these fit each item (one item can trigger more than
one technique):

- **Assumption mining** — for each implicit assumption: what happens if this doesn't hold? Is there
  any indication it might not?
- **Failure-scenario construction** — put on an attacker's hat and build concrete scenarios meant to
  break the plan: edge cases, misuse, concurrency/ordering problems, malicious input, resource
  exhaustion, organizational/process failure modes.
- **Devil's advocate counter-proposal** — for key decisions, construct a genuinely competitive
  alternative and check whether the document's stated reasoning actually survives the comparison.
  Steelman the alternative; don't strawman it just to make the original look better.
- **Ambiguity / gap detection** — could this requirement be read two different ways? Is an acceptance
  criterion actually testable? Is there a boundary condition the document never addresses at all?

### 3. Cross-check against the codebase (when one exists)

For candidate findings that hinge on a claim about current behavior or change scope, verify it with
Grep/Read against the real code instead of trusting the document's own framing. This is often where the
sharpest, most concrete findings come from — a claim the document treats as obvious but the code
contradicts.

### 4. Self-verify and cut the noise

Go back through every candidate finding from stages 2–3 and ask: is this actually grounded, or did I
manufacture it just to have something to say? Adversarial review has an inherent failure mode — picking
fights for their own sake — and this stage is the gate against it. For each surviving finding, decide
two independent things:

- **Verdict** — `CONFIRMED` (grounded in the document's actual text or a concrete contradiction with
  the code) or `PLAUSIBLE` (a real concern, reasoned but not airtight, still worth the author's
  attention).
- **Severity** — based on the actual blast radius you just established, not on how interesting the
  finding felt to write:
  - `Blocker` — a primary, user-facing capability the document promises is completely broken, or the
    defect causes data corruption / data reaching the wrong party.
  - `High` — wrong behavior on a common path with no safeguard or error surfaced, but not the primary
    promised capability, or a workaround exists.
  - `Medium` — a real problem but confined to an edge case, a narrow caller, or a contract/doc
    inconsistency without immediate runtime breakage.
  - `Low` — cosmetic or documentation-only mismatch with no behavioral consequence.

Discard anything that doesn't clear the verdict bar. Precision over volume: a short list of findings
that all land is worth more than a long list padded with speculative nitpicks.

### 5. Rank and report

Order the surviving findings by severity (`Blocker` → `High` → `Medium` → `Low`) and report them with
`ReportFindings`.

There's no adjustable effort/verbosity tier for this skill (unlike `code-review`'s low/medium/high).
The bar is fixed: every finding must trace back to specific document text or a specific contradiction
with the code, and must have survived stage 4.

## Reporting findings

`ReportFindings` has no dedicated severity or evidence field — both have to live inside `summary` and
`failure_scenario`. Don't let the fixed schema become an excuse to write a one-line abstract conclusion;
a finding a reader can't independently check by looking at the cited line is not done yet. Call
`ReportFindings` once, with fields mapped like this:

- `file` → the actual document the finding came from (when reviewing multiple files, each finding
  points at its real source file, never the directory)
- `line` → the document line the finding anchors to; if a finding spans a whole section or is about
  something the document never mentions at all, point at the most relevant line (e.g. a section
  heading) rather than forcing an artificial line number
- `summary` → one sentence naming the defect, prefixed with its stage-4 severity tag:
  `[Blocker] ...`, `[High] ...`, `[Medium] ...`, `[Low] ...`
- `failure_scenario` → three parts, always present and in this order, don't blur them into one vague
  sentence:
  1. **Evidence** — quote the exact document text the claim rests on (with its line), and when
     cross-checked against code, quote the exact contradicting code (with file:line). Paraphrasing away
     the specifics defeats the point — the reader should be able to verify the finding without re-doing
     your research.
  2. **Mechanism** — the concrete situation that triggers the problem ("if two clients hit this endpoint
     concurrently during migration, X happens"), not an abstract restatement of the evidence.
  3. **Blast radius** — who or what is actually affected: which caller, which user segment, which
     downstream system, how often this path is hit. Never settle for "this could be risky" — name the
     actual exposure, or say plainly if it's narrow.
- `verdict` → `CONFIRMED` or `PLAUSIBLE` per stage 4

## Relationship to other skills

- **`code-review` / `security-review`**: review code diffs for correctness and security. This skill
  reviews descriptive documents for flawed decisions, assumptions, and requirements. They don't
  overlap, and a single piece of work might use both in sequence — adversarially review the proposal
  first, then once the code is written, run `code-review`/`security-review` on the diff.
- **`grilling`**: an interactive, live interview aimed at the user, for thinking through an idea that
  isn't fully written down yet. This skill is a one-shot automated analysis of an already-written
  document that produces a static report, no back-and-forth required. If the user wants to dig further
  into a specific finding this skill surfaced, that's a good moment to switch to `grilling`.
