use serde::{Deserialize, Serialize};
use std::path::PathBuf;

use crate::error::{AppError, AppResult};

/// On-disk configuration. Lives at:
/// - macOS:   `~/Library/Application Support/bookmark-curator/config.toml`
/// - Linux:   `~/.config/bookmark-curator/config.toml`
/// - Windows: `%APPDATA%\bookmark-curator\config.toml`
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(default)]
pub struct Config {
    pub provider: ProviderKind,
    pub claude: ClaudeConfig,
    pub ollama: OllamaConfig,
    pub scan: ScanConfig,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum ProviderKind {
    Claude,
    Ollama,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(default)]
pub struct ClaudeConfig {
    /// API key. Empty string means "not set".
    pub api_key: String,
    pub model: String,
    pub base_url: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(default)]
pub struct OllamaConfig {
    pub model: String,
    pub base_url: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(default)]
pub struct ScanConfig {
    /// How many days back to scan from "now".
    pub lookback_days: u32,
    /// Drop URLs that were visited fewer than this many times.
    pub min_visit_count: u32,
    /// Domains to skip entirely (search engines, internal tools, etc.).
    pub blocklist_domains: Vec<String>,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            provider: ProviderKind::Claude,
            claude: ClaudeConfig::default(),
            ollama: OllamaConfig::default(),
            scan: ScanConfig::default(),
        }
    }
}

impl Default for ClaudeConfig {
    fn default() -> Self {
        Self {
            api_key: String::new(),
            model: "claude-sonnet-4-6".to_string(),
            base_url: "https://api.anthropic.com".to_string(),
        }
    }
}

impl Default for OllamaConfig {
    fn default() -> Self {
        Self {
            model: "qwen2.5:7b".to_string(),
            base_url: "http://localhost:11434".to_string(),
        }
    }
}

impl Default for ScanConfig {
    fn default() -> Self {
        Self {
            lookback_days: 90,
            min_visit_count: 2,
            blocklist_domains: vec![
                "google.com".to_string(),
                "bing.com".to_string(),
                "duckduckgo.com".to_string(),
                "localhost".to_string(),
                "127.0.0.1".to_string(),
            ],
        }
    }
}

pub fn config_dir() -> AppResult<PathBuf> {
    let base = dirs::config_dir()
        .ok_or_else(|| AppError::Config("could not resolve config dir for this OS".into()))?;
    Ok(base.join("bookmark-curator"))
}

pub fn config_path() -> AppResult<PathBuf> {
    Ok(config_dir()?.join("config.toml"))
}

pub fn load() -> AppResult<Config> {
    let path = config_path()?;
    if !path.exists() {
        let cfg = Config::default();
        save(&cfg)?;
        return Ok(cfg);
    }
    let raw = std::fs::read_to_string(&path)?;
    let cfg: Config = toml::from_str(&raw)?;
    Ok(cfg)
}

pub fn save(cfg: &Config) -> AppResult<()> {
    let dir = config_dir()?;
    std::fs::create_dir_all(&dir)?;
    let path = config_path()?;
    let raw = toml::to_string_pretty(cfg)?;
    std::fs::write(path, raw)?;
    Ok(())
}
