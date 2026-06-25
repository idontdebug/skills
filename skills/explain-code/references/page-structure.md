# Explainer page structure and components (written into `__CONTENT__`)

The page skeleton (top nav bar #1, dark toggle, export to PDF, Mermaid zoom/reset, table search/filter,
print optimization) all live in `assets/template.html`, with Tailwind and Mermaid already inlined. You
only write the HTML for **blocks 2–8** into `content.html` (the template's `__CONTENT__`). The nav bar
(#1) is filled by the template from `--title` / `--path`.

Style with the template's predefined Tailwind component classes (defined via `@apply`); just write the
short class names. You can also stack on any Tailwind utility classes as needed. **Follow the 1→8 order
strictly.**

The section headings below are placeholders. Write all visible text (headings, labels, captions) in
the user's language, one language only, with no emojis and no bilingual `中文 / English` double
headings. See "Write like an engineer, not an AI" in `SKILL.md`.

## JS hook conventions (must follow, or interactions break)
- **Zoomable diagram**: `<div class="diagram"><pre class="mermaid">…</pre></div>`. The script renders
  Mermaid and automatically adds a zoom/reset toolbar. Hand-written SVG also goes inside
  `<div class="diagram">`.
- **Rules matrix search/filter**: outer `<div data-rules>`, containing `<input data-rules-search>` and
  `<select data-rules-filter>` (option values are `all/high/med/low`); the table `<tbody>` has each row
  as `<tr data-risk="high|med|low|none">`. The script filters by text + risk level.
- **Accordion**: native `<details class="acc"><summary>…</summary><div class="acc-body">…</div></details>`,
  auto-expanded when printing.
- **Navigation**: each `<section id="...">` carries an `<h2 class="h-sec">`, and the top nav collects
  them automatically (the Hero uses `<h1>`, which is not added to the nav).

## Block templates (in order)

### 2. Hero + key metric cards
```html
<section id="hero" class="section">
  <div class="rounded-2xl border border-slate-200 dark:border-slate-700 bg-gradient-to-br from-brand-50 to-white dark:from-slate-800 dark:to-slate-900 p-7">
    <span class="chip mb-3"><b>Business logic explainer</b></span>
    <h1 class="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">XxxService.method — one-line locator</h1>
    <p class="lead mt-2 max-w-3xl">Who it's for, what problem it solves.</p>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
    <div class="metric"><div class="kpi-num">5</div><div class="kpi-label">Branches</div></div>
    <div class="metric"><div class="kpi-num">3</div><div class="kpi-label">Order states</div></div>
    <div class="metric"><div class="kpi-num">4</div><div class="kpi-label">Return codes</div></div>
    <div class="metric"><div class="kpi-num">3</div><div class="kpi-label">Known risks</div></div>
  </div>
</section>
```

### 3. Executive summary (high-level business overview)
```html
<section id="summary" class="section">
  <h2 class="h-sec"><span class="idx">01</span>Executive summary</h2>
  <div class="callout callout-note"><p class="lead">A 3–5 sentence high-level overview for a non-author reader: what this code does in business terms, the key branching dimension, and the single most important thing to watch out for.</p></div>
</section>
```

### 4. Core business flow (large diagram + control buttons + step list)
The zoom/reset buttons are added by the script automatically; no need to write them.
```html
<section id="flow" class="section">
  <h2 class="h-sec"><span class="idx">02</span>Core business flow</h2>
  <div class="diagram">
    <pre class="mermaid">
flowchart TD
  S["Entry"] --> Q1{"orderType == top-up?"}
  Q1 -- yes --> R1["Adjust balance account<br/>return 0001"]
  Q1 -- no --> C["Generic billing"]
    </pre>
    <div class="cap">Returns on match; colors correspond to the steps/cards below</div>
  </div>
  <ol class="steps mt-4">
    <li><b>Step one</b>: …</li>
    <li><b>Step two</b>: …</li>
  </ol>
</section>
```

For complex logic, follow the flowchart with a **sequence diagram** in its own `.diagram` block right
below it (`sequenceDiagram`), so the branch logic and the cross-layer call order both get shown. Stack
the diagrams vertically. Every diagram is a full-width block; never put two diagrams in a side-by-side
grid (it shrinks them and clips labels).

### 5. Detailed logic breakdown (accordion: each step has business meaning + technical note)
```html
<section id="detail" class="section">
  <h2 class="h-sec"><span class="idx">03</span>Detailed logic breakdown</h2>
  <details class="acc" open>
    <summary>① Top-up branch <span class="badge badge-info ml-1">return 0001</span></summary>
    <div class="acc-body">
      <p><b>Business meaning:</b> a top-up is not a purchase order; it only adjusts the "money" account and never touches the order table.</p>
      <p class="mt-2"><b>Technical note:</b> when <code>orderType == "top-up"</code> matches, set the <code>SettlementDetails</code> / <code>TradeRelationship</code> channel to <code>balance-recharge</code> and call <code>notifyForReCharge</code>.</p>
    </div>
  </details>
  <details class="acc">
    <summary>② Subscription branch <span class="badge badge-info ml-1">return 0002</span></summary>
    <div class="acc-body">…</div>
  </details>
</section>
```

### 6. Business rules matrix (searchable + risk filter; risk shown as colored badges)
```html
<section id="rules" class="section">
  <h2 class="h-sec"><span class="idx">04</span>Business rules matrix</h2>
  <div data-rules class="card !p-0 overflow-hidden">
    <div class="flex flex-wrap gap-2 p-3 border-b border-slate-200 dark:border-slate-700">
      <input data-rules-search type="search" placeholder="Search rules / conditions…" class="flex-1 min-w-[160px] rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 px-3 py-1.5 text-sm">
      <select data-rules-filter class="rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 px-3 py-1.5 text-sm">
        <option value="all">All risks</option><option value="high">High</option><option value="med">Medium</option><option value="low">Low</option>
      </select>
    </div>
    <div class="overflow-x-auto">
      <table class="tbl">
        <thead><tr><th>Rule</th><th>Condition</th><th>Result</th><th>Risk</th></tr></thead>
        <tbody>
          <tr data-risk="high"><td>Unknown type not persisted</td><td><code>type ∉ {standard, premium}</code></td><td>Claims success but does not update</td><td><span class="badge badge-high">High</span></td></tr>
          <tr data-risk="low"><td>Full subscription charge</td><td><code>orderType == "subscription"</code></td><td>PAID, received = billed</td><td><span class="badge badge-low">Low</span></td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
```

### 7. Risks and improvement suggestions (card grid, categorized by severity)
```html
<section id="risks" class="section">
  <h2 class="h-sec"><span class="idx">05</span>Risks and improvement suggestions</h2>
  <div class="grid md:grid-cols-2 gap-3">
    <div class="riskcard riskcard-high">
      <div class="flex items-center gap-2 mb-1.5"><span class="badge badge-high">High</span><span class="card-t">Unknown type silently not persisted</span></div>
      <p class="text-sm text-slate-600 dark:text-slate-300">The tail has only two <code>if</code>s for standard/premium and no <code>else</code>; other types mutate in memory but are never updated.</p>
      <p class="text-sm mt-2"><b>Suggestion:</b> add an <code>else</code> branch or assertion, and at least log a warning.</p>
    </div>
    <div class="riskcard riskcard-med">
      <div class="flex items-center gap-2 mb-1.5"><span class="badge badge-med">Medium</span><span class="card-t">Top-up branch does not null-check</span></div>
      <p class="text-sm text-slate-600 dark:text-slate-300">…</p>
    </div>
  </div>
</section>
```

### 8. Appendix (metadata)
```html
<section id="appendix" class="section">
  <h2 class="h-sec"><span class="idx">06</span>Appendix</h2>
  <div class="grid sm:grid-cols-3 gap-3 text-sm">
    <div class="card"><div class="card-t">Analysis target</div><code>src/.../OrderService.java#updateOrderWhenPaySuccess</code></div>
    <div class="card"><div class="card-t">Related files</div><ul class="mt-1 space-y-1"><li><code>OrderService.java:1085</code></li><li><code>OrderStatusEnum.java</code></li></ul></div>
    <div class="card"><div class="card-t">Generated</div>2026-06-25 · explain-code skill</div>
  </div>
</section>
```

## Component cheat sheet
- Callouts: `callout callout-note` (blue) / `callout callout-warn` (amber) / `callout callout-ok` (green); lead with `<span class="ctag">label</span>`.
- Badges: `badge badge-high|badge-med|badge-low|badge-info`.
- Cards: `card` + `card-t` (title); metric cards `metric` + `kpi-num` + `kpi-label`; risk cards `riskcard riskcard-high|med|low`.
- Step list: `<ol class="steps">`, highlight numbers with `<span class="val">6.00</span>`.
- Diagram caption: `<div class="cap">`. Side-by-side grid (cards/tables only, never diagrams): `grid md:grid-cols-2 gap-3`.

## How to draw diagrams
- Use `<pre class="mermaid">` for standard diagrams (`flowchart` / `sequenceDiagram` / `stateDiagram-v2` / `gantt`). **Always quote labels** with special characters: `A["order = paid"]`, otherwise `()=+:` will break parsing.
- For custom diagrams (such as a timeline coloring paid/free time segments), hand-write an inline `<svg>` inside `<div class="diagram">` — zero dependencies, reliable offline, and tailored to the content.
- Put every diagram inside `<div class="diagram">` so it gets the zoom/reset toolbar.
