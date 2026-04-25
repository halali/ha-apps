//! Read browser history.
//!
//! Chrome (and Chromium-derivatives like Edge, Brave, Arc) stores history in a
//! SQLite database that gets locked while the browser is running. We always
//! copy the file to a temp location before opening it, so the user doesn't
//! have to quit Chrome.

use std::path::{Path, PathBuf};

use chrono::{DateTime, Duration, TimeZone, Utc};
use rusqlite::Connection;
use serde::{Deserialize, Serialize};

use crate::config::ScanConfig;
use crate::error::{AppError, AppResult};

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum BrowserKind {
    Chrome,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BrowserProfile {
    pub browser: BrowserKind,
    /// Display name like "Default" or "Profile 1".
    pub name: String,
    /// Absolute path to the profile folder containing the History file.
    pub path: PathBuf,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HistoryEntry {
    pub url: String,
    pub title: String,
    pub visit_count: u32,
    /// Last visit, as ISO-8601 UTC.
    pub last_visit: DateTime<Utc>,
    pub domain: String,
}

/// Discover Chrome profile directories on this machine.
pub fn discover_profiles() -> AppResult<Vec<BrowserProfile>> {
    let Some(root) = chrome_user_data_dir() else {
        return Ok(vec![]);
    };
    if !root.exists() {
        return Ok(vec![]);
    }

    let mut out = Vec::new();
    for entry in std::fs::read_dir(&root)? {
        let entry = entry?;
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }
        let name = entry.file_name().to_string_lossy().into_owned();
        // Chrome's profile dirs are "Default" and "Profile N".
        let looks_like_profile = name == "Default" || name.starts_with("Profile ");
        if !looks_like_profile {
            continue;
        }
        if !path.join("History").exists() {
            continue;
        }
        out.push(BrowserProfile {
            browser: BrowserKind::Chrome,
            name,
            path,
        });
    }
    Ok(out)
}

fn chrome_user_data_dir() -> Option<PathBuf> {
    // We only support macOS in this MVP; Linux/Windows paths are listed for
    // future reference and unit-test mocking.
    if cfg!(target_os = "macos") {
        dirs::home_dir().map(|h| h.join("Library/Application Support/Google/Chrome"))
    } else if cfg!(target_os = "linux") {
        dirs::config_dir().map(|c| c.join("google-chrome"))
    } else if cfg!(target_os = "windows") {
        dirs::data_local_dir().map(|d| d.join("Google/Chrome/User Data"))
    } else {
        None
    }
}

/// Read entries from the given profile's History DB, applying scan filters.
///
/// The DB file is copied to a temp path first so an open Chrome doesn't block
/// us with its write lock.
pub fn read_history(profile: &BrowserProfile, scan: &ScanConfig) -> AppResult<Vec<HistoryEntry>> {
    let history_path = profile.path.join("History");
    if !history_path.exists() {
        return Err(AppError::History(format!(
            "no History file at {}",
            history_path.display()
        )));
    }

    let tmp_path = copy_to_temp(&history_path)?;
    let conn = Connection::open_with_flags(
        &tmp_path,
        rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY | rusqlite::OpenFlags::SQLITE_OPEN_URI,
    )?;

    let cutoff_chrome = chrome_time(Utc::now() - Duration::days(scan.lookback_days as i64));

    // Chrome stores last_visit_time in microseconds since 1601-01-01 UTC.
    let mut stmt = conn.prepare(
        "SELECT url, title, visit_count, last_visit_time
         FROM urls
         WHERE last_visit_time >= ?1
           AND visit_count >= ?2
         ORDER BY last_visit_time DESC",
    )?;

    let rows = stmt.query_map(
        rusqlite::params![cutoff_chrome, scan.min_visit_count],
        |row| {
            let url: String = row.get(0)?;
            let title: String = row.get(1)?;
            let visit_count: i64 = row.get(2)?;
            let last_visit_chrome: i64 = row.get(3)?;
            Ok((url, title, visit_count, last_visit_chrome))
        },
    )?;

    let blocklist: Vec<String> = scan
        .blocklist_domains
        .iter()
        .map(|d| d.to_lowercase())
        .collect();

    let mut entries = Vec::new();
    for row in rows {
        let (url, title, visit_count, last_visit_chrome) = row?;
        let domain = match url::Url::parse(&url).ok().and_then(|u| u.host_str().map(str::to_string)) {
            Some(d) => d,
            None => continue,
        };
        if blocklist
            .iter()
            .any(|b| domain == *b || domain.ends_with(&format!(".{b}")))
        {
            continue;
        }
        if title.trim().is_empty() {
            // Pages without a title give the LLM nothing to work with.
            continue;
        }
        entries.push(HistoryEntry {
            url,
            title,
            visit_count: visit_count.max(0) as u32,
            last_visit: from_chrome_time(last_visit_chrome),
            domain,
        });
    }

    let _ = std::fs::remove_file(&tmp_path);
    Ok(dedupe(entries))
}

fn copy_to_temp(src: &Path) -> AppResult<PathBuf> {
    let mut dst = std::env::temp_dir();
    dst.push(format!(
        "bookmark-curator-history-{}.sqlite",
        std::process::id()
    ));
    std::fs::copy(src, &dst)?;
    Ok(dst)
}

/// Microseconds since 1601-01-01 UTC (Chrome's epoch).
fn chrome_time(t: DateTime<Utc>) -> i64 {
    const EPOCH_DELTA_MICROS: i64 = 11_644_473_600_000_000;
    t.timestamp_micros() + EPOCH_DELTA_MICROS
}

fn from_chrome_time(micros: i64) -> DateTime<Utc> {
    const EPOCH_DELTA_MICROS: i64 = 11_644_473_600_000_000;
    let unix_micros = micros - EPOCH_DELTA_MICROS;
    Utc.timestamp_micros(unix_micros).single().unwrap_or_else(Utc::now)
}

/// Drop duplicate URLs, keeping the entry with the most visits.
fn dedupe(mut entries: Vec<HistoryEntry>) -> Vec<HistoryEntry> {
    entries.sort_by(|a, b| b.visit_count.cmp(&a.visit_count));
    let mut seen = std::collections::HashSet::new();
    entries.retain(|e| seen.insert(e.url.clone()));
    entries
}
