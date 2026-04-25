use async_trait::async_trait;
use serde::Deserialize;
use serde_json::json;

use super::{CategorizationInput, CategorizationOutput, Categorizer, SYSTEM_PROMPT};
use crate::config::OllamaConfig;
use crate::error::{AppError, AppResult};

pub struct OllamaProvider {
    cfg: OllamaConfig,
    http: reqwest::Client,
}

impl OllamaProvider {
    pub fn new(cfg: OllamaConfig) -> Self {
        Self {
            cfg,
            http: reqwest::Client::builder()
                // Local model warm-up + long batch responses.
                .timeout(std::time::Duration::from_secs(300))
                .build()
                .unwrap_or_default(),
        }
    }
}

#[async_trait]
impl Categorizer for OllamaProvider {
    async fn categorize(
        &self,
        batch: Vec<CategorizationInput>,
    ) -> AppResult<Vec<CategorizationOutput>> {
        let user_payload = serde_json::to_string(&batch)?;
        let body = json!({
            "model": self.cfg.model,
            "stream": false,
            "format": "json",
            "messages": [
                { "role": "system", "content": SYSTEM_PROMPT },
                { "role": "user", "content": user_payload }
            ],
        });

        let url = format!("{}/api/chat", self.cfg.base_url.trim_end_matches('/'));
        let resp = self.http.post(url).json(&body).send().await?;
        if !resp.status().is_success() {
            let status = resp.status();
            let text = resp.text().await.unwrap_or_default();
            return Err(AppError::Ai(format!("Ollama {status}: {text}")));
        }

        let parsed: OllamaChatResponse = resp.json().await?;
        // With `format: json` Ollama returns either a JSON array or an object
        // wrapping it under some key. Try array first, then a `{ "items": [...] }`
        // style fallback.
        let content = parsed.message.content;
        if let Ok(out) = serde_json::from_str::<Vec<CategorizationOutput>>(&content) {
            return Ok(out);
        }
        if let Ok(wrap) = serde_json::from_str::<OllamaArrayWrap>(&content) {
            return Ok(wrap.items);
        }
        Err(AppError::Ai(format!(
            "could not parse Ollama output as JSON array; got: {content}"
        )))
    }

    async fn ping(&self) -> AppResult<()> {
        let url = format!("{}/api/tags", self.cfg.base_url.trim_end_matches('/'));
        let resp = self.http.get(url).send().await?;
        if !resp.status().is_success() {
            return Err(AppError::Ai(format!(
                "Ollama not reachable at {} (status {})",
                self.cfg.base_url,
                resp.status()
            )));
        }
        Ok(())
    }
}

#[derive(Deserialize)]
struct OllamaChatResponse {
    message: OllamaMessage,
}

#[derive(Deserialize)]
struct OllamaMessage {
    content: String,
}

#[derive(Deserialize)]
struct OllamaArrayWrap {
    items: Vec<CategorizationOutput>,
}
