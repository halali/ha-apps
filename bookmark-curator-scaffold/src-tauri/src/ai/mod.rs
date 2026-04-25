//! AI provider abstraction.
//!
//! Each provider takes a batch of `{url, title}` pairs and returns the same
//! list with a `category` path attached to each one. Categories are forward-
//! slash separated, e.g. `Work/Reading/Rust`.
//!
//! Adding a new provider: implement `Categorizer`, register it in `build()`.

pub mod claude;
pub mod ollama;

use async_trait::async_trait;
use serde::{Deserialize, Serialize};

use crate::config::{Config, ProviderKind};
use crate::error::AppResult;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CategorizationInput {
    pub url: String,
    pub title: String,
    pub domain: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CategorizationOutput {
    pub url: String,
    pub title: String,
    pub domain: String,
    /// Forward-slash separated path, e.g. "Dev/Rust/Crates".
    pub category: String,
}

#[async_trait]
pub trait Categorizer: Send + Sync {
    async fn categorize(&self, batch: Vec<CategorizationInput>) -> AppResult<Vec<CategorizationOutput>>;

    /// Cheap round-trip used by the Settings "Test connection" button.
    async fn ping(&self) -> AppResult<()>;
}

pub fn build(cfg: &Config) -> Box<dyn Categorizer> {
    match cfg.provider {
        ProviderKind::Claude => Box::new(claude::ClaudeProvider::new(cfg.claude.clone())),
        ProviderKind::Ollama => Box::new(ollama::OllamaProvider::new(cfg.ollama.clone())),
    }
}

/// Shared system prompt. Both providers feed the model the same instructions
/// so switching providers doesn't change the taxonomy mid-run.
pub(crate) const SYSTEM_PROMPT: &str = "\
You are a librarian that organises web bookmarks into a hierarchical folder \
structure. You will be given a JSON array of items, each with a `url`, \
`title`, and `domain`. Return a JSON array of the same length and order, \
where each element has the original `url`, `title`, `domain`, plus a \
`category` field.

Rules for `category`:
- Use forward slashes to separate folder levels, e.g. \"Work/Reading/Rust\".
- 1 to 3 levels deep. Prefer 2.
- Use Title Case. Be consistent: don't switch between \"Dev\" and \"Development\".
- Top-level folders should be broad (Work, Personal, Reference, Entertainment, \
  Shopping, Finance, News, Social). Pick the most natural fit.
- Group similar sites into the same category, even if their domains differ.
- Never return an empty category.

Return ONLY the JSON array, no prose, no markdown fence.\
";
