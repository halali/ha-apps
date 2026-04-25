# bookmark-curator

Turn your browser history into a clean, organised set of bookmarks — automatically.

`bookmark-curator` is a desktop app that reads your **Chrome** history, asks an
**LLM** (cloud or local) to cluster the URLs into a sensible folder structure,
lets you review and edit the result, and exports a Netscape-format HTML file
you can import back into any browser.

> **Status:** early scaffolding. Not yet shipping a release. macOS first, Linux
> and Windows follow once the core flow is stable.

## Why

Most people's bookmark bars are a graveyard, while their history holds hundreds
of pages they actually return to. This app closes that gap without you having
to manually triage 5,000 URLs.

## How it works

```
Chrome SQLite history  →  filter & dedupe  →  LLM categorisation
                                                     │
                              review UI  ←───────────┘
                                  │
                                  ▼
                         Netscape bookmarks.html
                                  │
                                  ▼
                         import into any browser
```

The history file is **copied** before reading, so Chrome can stay open. Nothing
is written back to Chrome automatically — export is always opt-in.

## AI providers

Both are first-class and switchable from the Settings panel:

| Provider | When to choose it | Default model |
|----------|-------------------|---------------|
| **Anthropic Claude** | Best categorisation quality, requires API key, sends URLs + page titles to the API | `claude-sonnet-4-6` |
| **Ollama** (local)   | Fully private, runs on your machine, requires Ollama installed and a pulled model | `qwen2.5:7b` |

Configuration lives in `~/Library/Application Support/bookmark-curator/config.toml`
on macOS. The Settings UI writes the same file.

## Privacy

- History is read from a **local copy** — Chrome is never modified.
- With **Ollama**, no data leaves your machine.
- With **Claude**, only `{url, title}` pairs are sent — never page contents,
  never cookies, never anything from outside the selected time range.
- No telemetry, no analytics, no auto-updater phoning home.

## Tech stack

- **Tauri 2** — Rust backend, system webview, small bundle
- **React + TypeScript + Vite** — frontend
- **rusqlite** — read Chrome's `History` SQLite file
- **reqwest** — call Claude / Ollama APIs
- **MIT** licensed

## Development

Prerequisites: Rust (stable), Node 20+, pnpm.

```bash
pnpm install
pnpm tauri dev
```

See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) for the module layout.

## Contributing

Issues and pull requests welcome. Please keep PRs focused — a small fix beats
a sprawling refactor.

## License

[MIT](./LICENSE)
