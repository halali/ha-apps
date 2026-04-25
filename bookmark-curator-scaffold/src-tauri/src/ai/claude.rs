use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use serde_json::json;

use super::{CategorizationInput, CategorizationOutput, Categorizer, SYSTEM_PROMPT};
use crate::config::ClaudeConfig;
use crate::error::{AppError, AppResult};

const ANTHROPIC_API_VERSION: &str = "2023-06-01";

pub struct ClaudeProvider {
    cfg: ClaudeConfig,
    http: reqwest::Client,
}

impl ClaudeProvider {
    pub fn new(cfg: ClaudeConfig) -> Self {
        Self {
            cfg,
            http: reqwest::Client::new(),
        }
    }

    fn require_key(&self) -> AppResult<&str> {
        if self.cfg.api_key.trim().is_empty() {
            return Err(AppError::Ai(
                "Claude API key is not set. Add it in Settings.".into(),
            ));
        }
        Ok(self.cfg.api_key.trim())
    }
}

#[async_trait]
impl Categorizer for ClaudeProvider {
    async fn categorize(
        &self,
        batch: Vec<CategorizationInput>,
    ) -> AppResult<Vec<CategorizationOutput>> {
        let api_key = self.require_key()?;
        let user_payload = serde_json::to_string(&batch)?;

        let body = json!({
            "model": self.cfg.model,
            "max_tokens": 4096,
            "system": SYSTEM_PROMPT,
            "messages": [
                { "role": "user", "content": user_payload }
            ],
        });

        let url = format!("{}/v1/messages", self.cfg.base_url.trim_end_matches('/'));
        let resp = self
            .http
            .post(url)
            .header("x-api-key", api_key)
            .header("anthropic-version", ANTHROPIC_API_VERSION)
            .header("content-type", "application/json")
            .json(&body)
            .send()
            .await?;

        if !resp.status().is_success() {
            let status = resp.status();
            let text = resp.text().await.unwrap_or_default();
            return Err(AppError::Ai(format!("Claude {status}: {text}")));
        }

        let parsed: ClaudeResponse = resp.json().await?;
        let raw_text = parsed
            .content
            .into_iter()
            .find_map(|b| match b {
                ContentBlock::Text { text } => Some(text),
            })
            .ok_or_else(|| AppError::Ai("Claude returned no text content".into()))?;

        let cleaned = strip_code_fence(&raw_text);
        let outputs: Vec<CategorizationOutput> = serde_json::from_str(cleaned)
            .map_err(|e| AppError::Ai(format!("could not parse Claude output as JSON: {e}")))?;
        Ok(outputs)
    }

    async fn ping(&self) -> AppResult<()> {
        let api_key = self.require_key()?;
        // Smallest possible request: 1 token of output, single-word user message.
        let body = json!({
            "model": self.cfg.model,
            "max_tokens": 1,
            "messages": [{ "role": "user", "content": "ok" }],
        });
        let url = format!("{}/v1/messages", self.cfg.base_url.trim_end_matches('/'));
        let resp = self
            .http
            .post(url)
            .header("x-api-key", api_key)
            .header("anthropic-version", ANTHROPIC_API_VERSION)
            .header("content-type", "application/json")
            .json(&body)
            .send()
            .await?;
        if !resp.status().is_success() {
            let status = resp.status();
            let text = resp.text().await.unwrap_or_default();
            return Err(AppError::Ai(format!("Claude {status}: {text}")));
        }
        Ok(())
    }
}

#[derive(Deserialize)]
struct ClaudeResponse {
    content: Vec<ContentBlock>,
}

#[derive(Deserialize, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
enum ContentBlock {
    Text { text: String },
}

/// LLMs occasionally wrap JSON in ```json fences even when told not to. Strip
/// them so `serde_json` doesn't choke.
fn strip_code_fence(s: &str) -> &str {
    let s = s.trim();
    let s = s
        .strip_prefix("```json")
        .or_else(|| s.strip_prefix("```"))
        .unwrap_or(s);
    s.strip_suffix("```").unwrap_or(s).trim()
}

#[cfg(test)]
mod tests {
    use super::strip_code_fence;

    #[test]
    fn strips_json_fence() {
        assert_eq!(strip_code_fence("```json\n[1,2,3]\n```"), "[1,2,3]");
    }

    #[test]
    fn strips_plain_fence() {
        assert_eq!(strip_code_fence("```\n{\"a\":1}\n```"), "{\"a\":1}");
    }

    #[test]
    fn passes_through_clean_json() {
        assert_eq!(strip_code_fence("[1,2,3]"), "[1,2,3]");
    }
}
