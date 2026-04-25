# Handoff: bookmark-curator scaffold

This directory is a **temporary handoff artefact**. It does not belong in the
`halali/ha-apps` repository long term — it lives here only because the CCR
session that produced it was bound to `halali/ha-apps` as its signing source,
so it could not commit directly to the new `halali/bookmark-curator` repo.

## How to land this in `halali/bookmark-curator`

1. Open a fresh Claude Code session bound to `halali/bookmark-curator`.
2. In that session, ask Claude to copy this directory's contents into the
   new repo's working tree, then commit and push.
3. After the new repo has its first commit, **delete this directory** from
   `halali/ha-apps` and merge the brainstorm branch (or just close it).

## What's in here

A complete, locally-verified scaffold for a Tauri 2 + React + TypeScript
desktop app that reads Chrome history and uses an LLM (Claude or Ollama) to
auto-organise it into a Netscape bookmarks file.

Verified in the source session:

- `cargo check --lib` — passes
- `cargo test --lib` — 1/1 passes (`export::tests::renders_nested_folders`)
- `pnpm typecheck` — passes
- `pnpm install` — completes (lock file is included)

## File map

```
bookmark-curator-scaffold/
├── README.md              user-facing project README
├── LICENSE                MIT
├── docs/ARCHITECTURE.md   module layout + extension points
├── package.json           Tauri 2 + React 18 + Vite 5
├── pnpm-lock.yaml
├── tsconfig.json, tsconfig.node.json, vite.config.ts, index.html
├── src-tauri/
│   ├── Cargo.toml          crate config (rusqlite, reqwest, tauri 2, …)
│   ├── build.rs
│   ├── tauri.conf.json
│   ├── capabilities/default.json
│   ├── icons/              **placeholder solid-blue PNGs — replace before release**
│   └── src/
│       ├── main.rs
│       ├── lib.rs
│       ├── commands.rs     Tauri command surface (thin glue)
│       ├── config.rs       TOML config (provider, models, scan filters)
│       ├── history.rs      Chrome SQLite reader
│       ├── ai/
│       │   ├── mod.rs      Categorizer trait + shared system prompt
│       │   ├── claude.rs   Claude API impl
│       │   └── ollama.rs   Ollama impl
│       ├── categorize.rs   Batch pipeline
│       ├── export.rs       Netscape Bookmark File writer (+ unit test)
│       ├── state.rs
│       └── error.rs
└── src/
    ├── main.tsx, App.tsx, styles.css
    ├── lib/api.ts          typed Tauri command wrappers
    └── pages/
        ├── Scan.tsx        profile picker + scan + categorise trigger
        ├── Review.tsx      grouped-by-folder editor + HTML export
        └── Settings.tsx    provider switch + per-provider config + scan filters
```

## Decisions captured

| Area | Choice | Notes |
|------|--------|-------|
| GUI  | Tauri 2 (Rust + React) | Small bundle, native macOS feel |
| AI providers | Claude **and** Ollama, switchable | Behind a `Categorizer` trait |
| Default Claude model | `claude-sonnet-4-6` | |
| Default Ollama model | `qwen2.5:7b` | |
| Bookmark structure | hierarchical folders, 1–3 levels deep | Matches Chrome import |
| Output format | Netscape Bookmark File (HTML) | User imports manually — never write back to Chrome |
| Privacy | Read History from a temp copy; Ollama path keeps everything local | |
| Config location | `~/Library/Application Support/bookmark-curator/config.toml` | |
| Browser | Chrome only in MVP | Edge/Brave/Arc trivial to add (same schema) |
| Scope of MVP | scan → AI → review/edit → export | No write-back, no scheduling |

## Known follow-ups for the new session

- Replace placeholder icons in `src-tauri/icons/`
- Add `.github/workflows/ci.yml` (cargo check + cargo test + tsc)
- Add `CONTRIBUTING.md`
- Decide whether to commit `pnpm-lock.yaml` (currently yes) or
  `package-lock.json` (currently no) — pick one
- Smoke-test `pnpm tauri dev` on macOS (could not run in source session — Linux)
