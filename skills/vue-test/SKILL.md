---
name: vue-storybook-tests
description: >
  Set up Storybook + the Vitest addon in a Vue 3 (Vite) project and write
  component "stories" with play-function assertions so UI behavior is verified
  visually in a browser (each state shows pass/fail). Use this skill whenever
  the user wants to test Vue components, verify that inputs/buttons/forms work,
  check edge cases (empty, long text, whitespace-only, special characters,
  disabled states), add Storybook, write stories, set up component/interaction
  tests, or asks "how do I make sure this component actually works" — even if
  they don't say the word "Storybook". Trigger for any Vue 3 component-testing
  or interaction-testing request.
---

# Vue 3 component testing with Storybook + Vitest

This skill installs and configures Storybook with the Vitest addon in an
existing Vue 3 + Vite project, then writes component **stories** whose `play`
functions simulate real interaction (typing, clicking) and assert behavior.
The result is a browser UI where every component state is listed in the sidebar
with a live pass/fail indicator — the same experience as a visual test runner.

## When to apply

Apply when the user wants any of: verifying that a Vue component behaves
correctly, testing inputs/buttons/forms, covering edge cases, adding Storybook,
writing stories, or setting up interaction/component tests. The components are
Vue 3 Single-File Components in a Vite project.

If the project is **not** Vite-based (e.g. Vue CLI / webpack), the Vitest addon
won't work; say so and offer the test-runner fallback or migrating to Vite.

## Workflow

Follow these steps in order. Don't skip the environment check — the most common
failure is an incompatible Vite version.

### 1. Check the environment

- Confirm it's Vue 3 + Vite (look for `vite` and `vue` in `package.json`).
- Confirm **Vite is version 6 or higher**. Storybook's Vitest addon fails to
  start its browser mode on Vite 5. If it's on Vite 5, tell the user to upgrade
  Vite to ^6 (or newer) first — this is the single most common setup blocker.
- Note the package manager in use (npm / pnpm / yarn) and use it consistently.

### 2. Install Storybook

Run the initializer in the project root:

```bash
npx storybook@latest init
```

It auto-detects the `vue3-vite` framework, installs Storybook, creates the
`.storybook/` config directory, and scaffolds a few example stories. After it
finishes, `npm run storybook` should open the Storybook UI.

### 3. Add the Vitest addon (this is what provides the pass/fail UI)

```bash
npx storybook add @storybook/addon-vitest
```

This installs and configures the addon, Vitest itself, and browser-mode test
infrastructure. If it prompts to install Playwright browser binaries, accept —
component tests run in a real browser (Chromium) via Playwright.

After this, a **testing widget appears at the bottom of the Storybook sidebar**,
and once tests run, each sidebar item shows a pass/fail status indicator.

### 4. Write stories with assertions

For each target component, create a `*.stories.ts` file next to it. Each
exported story is one state shown in the sidebar. Add a `play` function to
simulate interaction and assert outcomes.

**Critical — match imports to the scaffolded example.** Test-utility and
framework import paths differ across Storybook versions (e.g. `storybook/test`
in v9+ vs `@storybook/test` in older versions). Before writing stories, open the
example `*.stories.ts` that `init` generated and copy its import lines exactly,
rather than guessing. This avoids version-mismatch errors.

**Critical — match the real DOM.** Read the actual component SFC first. Use its
real placeholder text, button labels, roles, and prop names in queries. Never
invent selectors. Prefer accessible queries (`getByRole`, `getByPlaceholderText`,
`getByLabelText`) over brittle CSS selectors.

For ready-to-adapt templates covering inputs, long text, whitespace-only,
disabled buttons, list rendering, toggles, async/loading, and accessibility
checks, read `references/story-patterns.md`.

### 5. Decide which states to cover

Don't just render the happy path. For each component, cover the states that
actually break in production. A good default checklist:

- **Default / empty** — initial render, no interaction.
- **Typical input** — normal user value; assert it's reflected.
- **Long text** — e.g. 500+ chars; assert no overflow / correct truncation.
- **Whitespace-only or empty submit** — assert the submit/Add control is
  disabled or rejected.
- **Special characters** — emoji, quotes, `<script>`, RTL text.
- **Boundary states** — list empty vs populated vs all-complete; counts.

Map the user's stated worries (e.g. "超长文本", "按钮能不能点") directly onto
these states so the coverage matches their concern.

### 6. Run and report

- Interactive: `npm run storybook`, click the test widget → run all → the
  sidebar shows green/red per story. Clicking a failure opens the Interactions
  panel, which steps through the `play` function for debugging.
- Headless / CI: the addon wires stories into Vitest, so `npx vitest`
  (or the project's test script) runs them without opening Storybook.

After running, report a concise summary: which stories pass, which fail, and the
specific assertion that failed (with the failing state name). Do not claim a
component "works" — report what the assertions verified.

## Output expectations

- One `*.stories.ts` per component, colocated with the SFC.
- Stories named by state (`Empty`, `Typed`, `LongText`, `WhitespaceOnly`, ...).
- Every non-trivial state has a `play` function with at least one assertion.
- Imports copied from the project's scaffolded example, not guessed.
- A short written summary of pass/fail results at the end.

## Common pitfalls

See `references/story-patterns.md` for the troubleshooting section, including the
Vite 5 issue, Playwright install, slow `userEvent.type` on very long strings,
and import-path drift across Storybook versions.
