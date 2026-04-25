# Architecture

This document gives a quick map of the codebase. See module-level doc comments
in the Rust source for finer detail.

## Process model

```
┌────────────────────────┐     IPC (invoke / events)     ┌────────────────────────┐
│  React + TypeScript    │ ────────────────────────────▶ │  Rust (Tauri host)      │
│  src/                  │                               │  src-tauri/             │
│                        │ ◀──────────────────────────── │                         │
│  - pages/Scan.tsx      │                               │  - commands.rs          │
│  - pages/Review.tsx    │                               │  - history.rs           │
│  - pages/Settings.tsx  │                               │  - ai/{claude,ollama}.rs│
│  - lib/api.ts          │                               │  - categorize.rs        │
└────────────────────────┘                               │  - export.rs            │
                                                         │  - config.rs            │
                                                         └────────────────────────┘
```

The frontend never touches the filesystem, the network, or SQLite directly.
Everything goes through Tauri commands defined in `src-tauri/src/commands.rs`.

## Data flow

```
[Settings] ──▶ config.toml on disk
                       │
[Scan]  ──▶ list_browser_profiles ──▶ scan_history ──▶ HistoryEntry[]
                                                             │
                                                             ▼
                                                       categorize ──▶ CategorizedEntry[]
                                                                              │
                                                                              ▼
[Review]  ──▶ user edits categories ──▶ export_html ──▶ bookmarks.html on disk
```

## Module responsibilities

| Module | Responsibility |
|--------|----------------|
| `commands.rs` | Tauri command surface; thin glue layer |
| `config.rs` | Load/save TOML config, default values |
| `history.rs` | Discover Chrome profiles, copy History DB, run filter query |
| `ai/mod.rs` | `Categorizer` trait and shared system prompt |
| `ai/claude.rs` | Claude implementation of `Categorizer` |
| `ai/ollama.rs` | Ollama implementation of `Categorizer` |
| `categorize.rs` | Batch a long list of entries through a `Categorizer` |
| `export.rs` | Render Netscape Bookmark File HTML |
| `state.rs` | In-memory app state (last categorisation result) |
| `error.rs` | App-wide error type with serde for IPC |

## Adding a new browser

`Chrome` is the only `BrowserKind` today. Edge, Brave, Arc, and Vivaldi all use
the same SQLite schema as Chromium, so the work is:

1. Add a variant to `BrowserKind` in `history.rs`.
2. Extend `discover_profiles` to look in the browser-specific user-data dir.
3. The reader query and time-encoding logic can be shared.

Firefox uses a different schema (`places.sqlite`, microseconds since Unix epoch)
and would need its own reader.

## Adding a new AI provider

1. Create `src-tauri/src/ai/<name>.rs` with a struct implementing `Categorizer`.
2. Register it in `ai::build()`.
3. Add a variant to `ProviderKind` in `config.rs` and a config struct.
4. Surface it in `src/pages/Settings.tsx`.

The system prompt is shared across providers in `ai/mod.rs::SYSTEM_PROMPT`.

## Why a Netscape HTML export, not direct Chrome write-back?

Writing to Chrome's `Bookmarks` JSON file requires the browser to be closed and
will silently corrupt the profile if the schema changes between versions. The
Netscape HTML format is a stable, browser-agnostic interchange format. The user
imports it manually — slower, but recoverable if anything goes wrong.

A direct write-back may be added later behind an explicit opt-in toggle.
