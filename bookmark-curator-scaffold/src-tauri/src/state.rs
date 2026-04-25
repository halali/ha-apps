use tokio::sync::Mutex;

use crate::ai::CategorizationOutput;

/// In-memory state shared across Tauri commands.
///
/// Right now this just holds the most recent categorisation result so the
/// frontend can navigate Scan → Review → Export without re-running the LLM.
pub struct AppState {
    pub last_categorized: Mutex<Vec<CategorizationOutput>>,
}

impl AppState {
    pub fn new() -> Self {
        Self {
            last_categorized: Mutex::new(Vec::new()),
        }
    }
}
