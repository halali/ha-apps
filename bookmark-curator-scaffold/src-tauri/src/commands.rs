//! Tauri command surface. Each function here is what the React frontend calls
//! through `invoke()`. Keep these thin: they validate inputs, delegate to
//! domain modules, and convert errors to the wire format.

use std::path::PathBuf;
use tauri::State;

use crate::ai::{self, CategorizationOutput};
use crate::categorize;
use crate::config::{self, Config};
use crate::error::AppResult;
use crate::export;
use crate::history::{self, BrowserProfile, HistoryEntry};
use crate::state::AppState;

#[tauri::command]
pub async fn get_config() -> AppResult<Config> {
    config::load()
}

#[tauri::command]
pub async fn save_config(cfg: Config) -> AppResult<()> {
    config::save(&cfg)
}

#[tauri::command]
pub async fn list_browser_profiles() -> AppResult<Vec<BrowserProfile>> {
    history::discover_profiles()
}

#[tauri::command]
pub async fn scan_history(profile: BrowserProfile) -> AppResult<Vec<HistoryEntry>> {
    let cfg = config::load()?;
    history::read_history(&profile, &cfg.scan)
}

#[tauri::command]
pub async fn categorize(
    entries: Vec<HistoryEntry>,
    state: State<'_, AppState>,
) -> AppResult<Vec<CategorizationOutput>> {
    let cfg = config::load()?;
    let provider = ai::build(&cfg);
    let result = categorize::run(provider.as_ref(), entries).await?;

    let mut last = state.last_categorized.lock().await;
    *last = result.clone();
    Ok(result)
}

#[tauri::command]
pub async fn export_html(
    items: Vec<CategorizationOutput>,
    path: String,
) -> AppResult<()> {
    export::write_html(&PathBuf::from(path), &items)
}

#[tauri::command]
pub async fn test_provider() -> AppResult<()> {
    let cfg = config::load()?;
    let provider = ai::build(&cfg);
    provider.ping().await
}
