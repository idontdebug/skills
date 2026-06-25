---
name: explain-code
description: >-
  Command-invoked, on-demand code explainer. **Invoke ONLY when the user explicitly asks for this
  skill** — i.e. they run the `/explain-code` command or say something like "use the explain-code
  skill to walk me through…". **Do NOT auto-trigger.** Even when the user says "explain this code",
  "I can't follow this logic", "walk me through this method", "explain this function", or "how does
  X work", do NOT invoke this skill on your own — just answer normally; only this skill's explicit
  invocation should run it. When invoked, it explains a piece of code's *business logic* by
  generating a polished, self-contained HTML explainer page (Tailwind-styled, light/dark, single
  offline file) built from concrete worked examples and visual diagrams (flowcharts, sequence/state
  diagrams, timelines, decision tables) rather than a line-by-line prose restatement.
---

# explain-code — generate a "see the diagram + see the example" explainer for code business logic

## What this skill does

The user points you at a piece of code (a location or a snippet). Your job is not to translate the
syntax line by line, but to make clear what it does **in business terms** and why, then deliver that
explanation as a **self-contained HTML page** — written to a file and opened in the browser. The two
most effective techniques are:

1. **Concrete worked examples** — pick a set of real inputs, run them through the code step by step,
   show how the intermediate values change, and arrive at the output. This is the fastest way to make
   logic "click".
2. **Diagrams** — visualize control flow, call relationships, state transitions, time intervals, and
   rule combinations. One good diagram beats three paragraphs.

The page is rendered from the bundled template (professional and modern, light-first with dark toggle,
top nav + export to PDF + zoomable diagrams, mobile- and print-friendly), suitable for internal tech
docs and stakeholder briefings. The reader is a developer who wants a *mental model*, not API docs.

## Core principle: explain the business, don't restate syntax

Translating syntax line by line is low value. Translate "machine language" into "business language".

- ❌ Bad: "Here `if (startTime.isBefore(periodStart))` checks whether the start time is before the
  period start, then `add`s an object to the list."
- ✅ Good: "If the resource was **already active before the subscription took effect**, then the gap
  between 'activation' and 'subscription start' isn't covered by the subscription, so it must be
  billed separately at the standard rate. That's why this line carves out that interval and queues it
  up to be priced later."

Translate magic values into meaning (`feePayFlag = "T"` → no payment required; `status = "1"` →
already paid), and spell out the business concepts behind the variable names.

## Write like an engineer, not an AI

The page should read like a senior engineer explaining the code to a colleague at a whiteboard, not
like generated marketing copy. Readers dismiss the whole thing the moment it "smells like AI". Avoid
these tells:

- **No emojis in the page content** (💡, 🛠️, ✅, 🚀, …). The template's UI chrome is the only place
  small icons belong; the body never uses them.
- **One language per page, no double-barreled bilingual headings.** Write `详细逻辑拆解`, not
  `详细逻辑拆解 / Detailed Logic Breakdown`, and never splice English words into an otherwise-Chinese
  heading (`详细 logic 分解`). Match the user's language and stay in it.
- **No invented buzzwords or dramatic jargon.** Don't coin terms like "需求漏斗穿透", "系统性崩溃",
  "黄金门禁", or "语意震荡". Name things the way the codebase and a normal engineer would; if a concept
  has no established name, describe it plainly instead of branding it.
- **Don't over-gloss.** Keep code identifiers verbatim, but don't stamp a parenthetical translation
  after every phrase (`触发条件 (Condition)`, `计算结果 (Result)`). Gloss a term at most once, and only
  when it genuinely helps.
- **Drop the hype and the exclamation marks.** No "彻底重构", "趋于完善", or "1.2x！". State what
  happens plainly and let the facts carry the weight.
- **Cut the filler.** No "值得注意的是", "综上所述", "总而言之", and no repeated "改进建议：" stamp on
  every card. Lead with the substance.
- **Vary the rhythm.** Relentless, perfectly parallel bullet lists read as machine-generated. Mix
  short sentences with the occasional longer one, the way people actually write.

Quick contrast:

- ❌ AI-flavored: "**群聚惩罚 (Clustering Multiplier)** 触发！同一章节的关联缺陷形成系统性崩溃,乘以
  1.2 倍惩罚系数。"
- ✅ Natural: "同一章节里冒出多个同类问题时,扣分会乘以 1.2。成片的问题通常说明这块设计整体没想清楚,
  而不是几个孤立的小疏漏。"

This applies to the prose you write. Code identifiers, enum values, and real data stay exactly as they
appear in the code.

## Workflow

1. **Locate and read the target**: resolve a `file:line`, a function name, a file path, or a pasted
   snippet, and read it fully. When the pointer is ambiguous, use Grep/Glob to find the best-matching
   location, and briefly confirm if needed.
2. **Follow dependencies for context (important, but stop in time)**: don't explain in a vacuum. To
   explain *this* code you usually have to hop around — the meaning of the **entities/fields** it reads
   and writes (amounts and timestamps are often stored as strings), what the **services/repositories/
   helpers it calls** actually do (step into them, don't guess from the method name), the business
   semantics behind **enums/constants**, and where the **data comes from**. Many backends are layered
   `Controller → Service → Repository/DAO → SQL/ORM mapping`; when the logic is "data-shaped" (queries,
   filtering, mapping), follow it down to the real SQL / mapping files (in ORM projects, read the
   corresponding mapping/query definitions) rather than guessing at the service layer. **Stop once you
   can tell the complete business story** — don't read the entire call tree.
3. **Distil the business intent**: before writing, state in a sentence or two "who this code is for and
   what real-world problem it solves". Label any inferred intent as inference.
4. **Choose diagrams**: pick the right diagram for the "shape" of the logic (see the table below).
5. **Generate the HTML explainer page**: assemble the body in the 8-block structure, build the page
   with the assembly script, and open it (see "Generating the HTML explainer page").
6. **Give a short summary in chat + the page path**: so the user gets the gist without switching
   windows, and can find/save the page.

## Which diagram: match the shape of the code

| Code shape | Recommended diagram | Why |
| --- | --- | --- |
| Many if/else branches, guard clauses, nested conditions | **flowchart** | Flattens nested conditions into walkable paths |
| Cross-service / cross-layer calls, messages, callbacks, external side effects | **sequence diagram** | Shows who calls whom, ordering, round trips, and side effects |
| Entities with a status field and a lifecycle (order status, approval flow) | **state diagram** | How states transition and what triggers each transition |
| Enum branches, rule tables, parameter combinations ("what to do in each case") | **decision table / table** | Lists all cases and their handling so none are missed |
| Time-window / period-based computation (cross-day billing, validity segmentation) | **timeline** (hand-written inline `<svg>` with colored intervals) | Draws out the intervals so overlaps/gaps are obvious |
| Amount accumulation / interval differences / formulas (due − paid = outstanding) | **formula flow / mini flowchart** (highlight numbers with `.val`) | Drawing the formula beats describing it in prose |
| Comparing two cases (A vs B) | **stacked diagrams** (one above the other) or a comparison table | Compare them stacked or in a table; never place two diagrams side by side |
| Data transformed across layers (DTO → Entity → VO, SQL → object) | **data-flow diagram / mapping table** | How fields map and where they transform |

A single piece of code may need more than one diagram (a flowchart for the branches, then a timeline
for the time computation in one branch). But **don't draw for the sake of drawing** — simple code only
needs one small diagram or one example.

**Layout rules for diagrams:**

- **Complex logic gets both a flowchart and a sequence diagram.** When the code is complex enough to
  deserve a flowchart, add a sequence diagram as well. The flowchart shows the branching; the sequence
  diagram shows the cross-layer / cross-service calls, their ordering, and the side effects. They
  answer different questions, so a complex method needs both, not one or the other.
- **Never lay diagrams out side by side.** Each diagram is its own full-width block, stacked top to
  bottom. Cards and comparison tables may sit in a side-by-side grid; diagrams never do, because
  shrinking a diagram into half a row clips labels and makes it unreadable.

## Generating the HTML explainer page

The page skeleton lives in `assets/template.html`: **top nav bar, dark-mode toggle, export to PDF,
Mermaid zoom/reset, rules-table search/filter, mobile and print optimizations** are all built in, and
**Tailwind and Mermaid are inlined** (self-contained, offline, **never reference any online CDN** —
the target environment often has no internet or is firewalled, and a CDN dependency would break
styles/diagrams or even hang the page). You only write the body content.

**Read `references/page-structure.md` before you start** — it gives the per-block HTML templates for
blocks 2–8, the component classes, and the JS hook conventions the interactions rely on (zoomable
diagrams, rules-table search/filter, accordions, etc.). The page **must follow these 8 parts in
order**:

1. Top nav bar (provided by the template, filled from `--title` / `--path`)
2. Hero + key metric cards
3. Executive summary (high-level business overview)
4. Core business flow (large Mermaid diagram + control buttons + step list)
5. Detailed logic breakdown (accordion; each step has business meaning + technical note)
6. Business rules matrix (searchable + risk-filterable table; risk shown as colored badges)
7. Risks and improvement suggestions (card grid, categorized by severity)
8. Appendix (analysis target, related files, timestamp, and other metadata)

**Assembly flow**: write the HTML for blocks 2–8 into `content.html`, then run the script (it injects
the title/path and inlines Tailwind + Mermaid, producing an offline single file):

```
python "<this skill dir>/scripts/build_explainer.py" \
  --title "SubscriptionService.calculateProratedCharge — mid-cycle plan change" \
  --path  "src/billing/SubscriptionService.java#calculateProratedCharge" \
  --content content.html \
  --out "<temp dir>/explain-<target-name>-<timestamp>.html"
```

Write the output to the system temp directory (to avoid polluting the user's repo) and tell the user
the path so they can save it. Open it: Windows `start "" "<file>"`; macOS `open "<file>"`; Linux
`xdg-open "<file>"`.

**Diagrams first (core requirement)**: default to expressing things as diagrams; text is only a
supplement. Before each paragraph, ask "**can this be a diagram?**" — if yes, draw it (which logic maps
to which diagram is in the "Which diagram" table above). Don't describe flows/branches/relationships
with big blocks of text or long `<ul>` lists; turn them into diagrams, colored cards, or accordions. A
complex method should usually have **more than one diagram** (a core flowchart plus a state diagram/
timeline/sequence diagram are often all needed). Keep colors consistent: whatever color a branch uses
in the flowchart, use the same color for the matching card/badge so the reader can map them at a glance.
The one red line: every diagram must genuinely aid understanding — don't pad with fake "charts" that
wrap two or three rows of data.

**How to draw diagrams**: use `<pre class="mermaid">` for standard diagrams
(`flowchart`/`sequenceDiagram`/`stateDiagram-v2`/`gantt`); **always quote labels** that contain special
characters — `A["order = paid"]` — otherwise `()=+:` will break parsing; for custom diagrams (such as a
timeline coloring paid/free time segments) hand-write an inline `<svg>` inside `<div class="diagram">`.
Put every diagram inside `<div class="diagram">` so it gets the zoom/reset toolbar.

**Degradation**:
- If `assets/tailwind.js` / `assets/mermaid.min.js` / the script is unavailable: still produce the page
  in the 8-block structure as best you can; when Mermaid is missing, switch diagrams to hand-written
  inline `<svg>`.
- If the environment simply isn't suited to generating/opening HTML (no browser/headless, or the user
  explicitly wants it in chat): degrade to a direct Markdown explanation in chat, with diagrams as
  ```mermaid``` code blocks or ASCII — the content and principles stay the same.

## How to walk through a good example

Examples are the soul of this skill:

- **Pick representative real inputs**: values close to real scenarios (real-looking IDs, timestamps,
  amounts, statuses), not `foo`/`123`.
- **Flag missing external rules**: if the computation depends on rules/rates outside the code (e.g. a
  unit price stored in a database), either look up the real value or **clearly mark it as an example
  value assumed for explanation** — don't let the reader think it's a real system rule.
- **Show state changes step by step**: use a step list `<ol class="steps">` to show the values of key
  variables/fields at each step (highlight numbers with `<span class="val">`), so the reader can follow
  along "in their head".
- **Main path + one boundary case**: walk the normal path first, then pick one interesting boundary
  (empty collection, crossing a threshold, misaligned start/end, etc.) — boundaries are often the
  reason the code is complex.

Example: for "proration across a subscription cycle" you can draw a timeline marking activation,
subscription start, subscription end, and deactivation, color the "billed vs free" segments, then use a
set of concrete dates to compute and sum each segment's amount.

## Accuracy and honesty (the bottom line for explanation tasks)

A wrong explanation is worse than no explanation.

- Ground every conclusion in **real code**, saying only what you've read; don't hallucinate branches or
  fields that don't exist.
- Distinguish "what the code does" from "the business intent I'm inferring" — label the latter as
  inference.
- For any number the code doesn't define (rates, thresholds), clearly mark it as an assumed example
  value.
- When unsure, say so and point to the file/config to check, rather than inventing a tidy story.

## Calibrating depth and language

- **Match depth to complexity**: a small utility function → one example may be enough (the page can be
  short; some blocks can be trimmed); a hundred-line branching method → worth a flowchart + timeline +
  walkthrough + the full 8 blocks. Read the user's intent too: do they want a "quick gist" or to
  "fully understand every branch"?
- **Follow the user's language**: Chinese if they write Chinese, English if they write English. Default
  to the language used by the project's comments/terminology, and **keep code identifiers verbatim**
  (variable names, method names, and magic values are not translated).
