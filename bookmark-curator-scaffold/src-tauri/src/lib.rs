//! bookmark-curator backend library.
//!
//! Tauri's `main.rs` is intentionally a one-liner that defers to `run()` here.
//! All command handlers, AI plumbing, and history scanning live in submodules.

mod ai;
mod categorize;
mod commands;
mod config;
mod error;
mod export;
mod history;
mod state;

use tracing_subscriber::EnvFilter;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("info,bookmark_curator_lib=debug")),
        )
        .init();

    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .manage(state::AppState::new())
        .invoke_handler(tauri::generate_handler![
            commands::get_config,
            commands::save_config,
            commands::list_browser_profiles,
            commands::scan_history,
            commands::categorize,
            commands::export_html,
            commands::test_provider,
        ])
        .run(tauri::generate_context!())
        .expect("error while running bookmark-curator");
}
