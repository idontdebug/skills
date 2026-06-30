# Story patterns & troubleshooting

Copy-and-adapt templates for common Vue component testing cases, plus fixes for
known setup issues. Always replace placeholder names, selectors, and labels with
the **real** ones from the component SFC.

## Table of contents

- Import note (read first)
- Pattern: text input (typed / long / whitespace / special chars)
- Pattern: button enabled/disabled
- Pattern: click handler / emitted event
- Pattern: list rendering (empty / populated / all-done)
- Pattern: toggle / checkbox
- Pattern: async / loading state
- Pattern: accessibility check
- Troubleshooting

---

## Import note (read first)

Import paths differ across Storybook versions. **Open the example `*.stories.ts`
that `storybook init` generated and copy its import lines.** The patterns below
use Storybook 9+ conventions; if the scaffold differs, follow the scaffold.

- Framework types/render: `@storybook/vue3-vite`
- Test utilities (`expect`, `userEvent`, `within`, `fn`): `storybook/test`
  (older projects: `@storybook/test`)

```ts
import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { expect, userEvent, within, fn } from 'storybook/test'
import MyComponent from './MyComponent.vue'

const meta = {
  title: 'Todo/MyComponent',
  component: MyComponent,
} satisfies Meta<typeof MyComponent>
export default meta
type Story = StoryObj<typeof meta>
```

`canvasElement` is passed into every `play` function; wrap it with `within()` to
query the rendered DOM.

---

## Pattern: text input

```ts
export const Empty: Story = {}

export const Typed: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const input = canvas.getByPlaceholderText('What needs doing?') // real placeholder
    await userEvent.type(input, 'Buy milk')
    await expect(input).toHaveValue('Buy milk')
  },
}

export const LongText: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const input = canvas.getByPlaceholderText('What needs doing?')
    const long = 'a'.repeat(500)
    // Setting value directly is far faster than typing 500 chars one by one:
    await userEvent.clear(input)
    await userEvent.type(input, long.slice(0, 20)) // trigger reactivity once
    ;(input as HTMLInputElement).value = long
    input.dispatchEvent(new Event('input', { bubbles: true }))
    await expect(input).toHaveValue(long)
    // If the component truncates, assert the truncated length instead.
  },
}

export const WhitespaceOnly: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const input = canvas.getByPlaceholderText('What needs doing?')
    await userEvent.type(input, '   ')
    const addButton = canvas.getByRole('button', { name: /add/i })
    await expect(addButton).toBeDisabled()
  },
}

export const SpecialCharacters: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const input = canvas.getByPlaceholderText('What needs doing?')
    await userEvent.type(input, '😀 "quote" <script>')
    await expect(input).toHaveValue('😀 "quote" <script>')
  },
}
```

## Pattern: button enabled/disabled

```ts
export const SubmitDisabledWhenEmpty: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    await expect(canvas.getByRole('button', { name: /add/i })).toBeDisabled()
  },
}
```

## Pattern: click handler / emitted event

Use `fn()` as a spy passed via args, then assert it was called.

```ts
export const FiresSubmit: Story = {
  args: { onSubmit: fn() },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement)
    await userEvent.type(canvas.getByRole('textbox'), 'Task')
    await userEvent.click(canvas.getByRole('button', { name: /add/i }))
    await expect(args.onSubmit).toHaveBeenCalledWith('Task') // adapt payload
  },
}
```

For Vue `emit`, map the event to a prop named `on<Event>` in args (Storybook's
Vue renderer supports this), or assert resulting DOM changes instead.

## Pattern: list rendering

```ts
export const ListEmpty: Story = { args: { items: [] } }

export const ListPopulated: Story = {
  args: { items: [{ id: 1, text: 'A', done: false }, { id: 2, text: 'B', done: true }] },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    await expect(canvas.getAllByRole('listitem')).toHaveLength(2)
    await expect(canvas.getByText('A')).toBeInTheDocument()
  },
}

export const AllDone: Story = {
  args: { items: [{ id: 1, text: 'A', done: true }, { id: 2, text: 'B', done: true }] },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    // e.g. assert an "all complete" message / styling exists
    await expect(canvas.getByText(/all done/i)).toBeInTheDocument()
  },
}
```

## Pattern: toggle / checkbox

```ts
export const ToggleComplete: Story = {
  args: { item: { id: 1, text: 'A', done: false }, onToggle: fn() },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement)
    await userEvent.click(canvas.getByRole('checkbox'))
    await expect(args.onToggle).toHaveBeenCalled()
  },
}
```

## Pattern: async / loading state

```ts
export const Loading: Story = {
  args: { loading: true },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    await expect(canvas.getByRole('status')).toBeInTheDocument() // spinner, etc.
  },
}
```

For data fetching, mock the network at the story level (e.g. MSW) rather than
hitting real endpoints, so the test is deterministic.

## Pattern: accessibility check

If the a11y addon is installed (`npx storybook add @storybook/addon-a11y`),
accessibility violations surface automatically in the sidebar alongside
interaction results — no extra code needed per story.

---

## Troubleshooting

**Vitest addon fails to start / browser mode error on install.**
Usually the project is on Vite 5. Upgrade Vite to ^6 (or newer) and reinstall.
A telltale error mentions a duplicate/nested browser project name.

**"Cannot find module 'storybook/test'" (or `@storybook/test`).**
Version mismatch on the import path. Copy the import lines from the example
story that `init` generated; use whichever path that file uses.

**`userEvent.type` is very slow for long strings.**
Typing dispatches an event per character. For 100+ char cases, type a few chars
to trigger reactivity, then set `.value` directly and dispatch one `input`
event (see the LongText pattern).

**Playwright not installed / tests won't run in browser.**
Re-run the addon setup and accept the Playwright install, or run
`npx playwright install chromium`.

**Queries can't find an element.**
The selector doesn't match the real DOM. Re-read the SFC; confirm the actual
placeholder, label, role, or text. Prefer `getByRole`/`getByLabelText`. Use the
Storybook UI to inspect the rendered output and the Interactions panel to step
through the `play` function.

**Story renders but assertions are skipped.**
Only stories with a `play` function are run as interaction tests. Add a `play`
with at least one `expect` to states you want verified.
