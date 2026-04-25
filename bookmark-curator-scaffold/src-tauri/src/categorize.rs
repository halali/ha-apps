//! Batch a long list of history entries through the LLM in chunks.

use crate::ai::{CategorizationInput, CategorizationOutput, Categorizer};
use crate::error::AppResult;
use crate::history::HistoryEntry;

/// How many entries to send per LLM call. Small enough to fit comfortably in
/// model context plus reasoning budget, large enough that we don't waste
/// round trips on tiny batches.
pub const BATCH_SIZE: usize = 40;

pub async fn run(
    provider: &dyn Categorizer,
    entries: Vec<HistoryEntry>,
) -> AppResult<Vec<CategorizationOutput>> {
    if entries.is_empty() {
        return Ok(vec![]);
    }

    let mut out = Vec::with_capacity(entries.len());
    for chunk in entries.chunks(BATCH_SIZE) {
        let batch: Vec<CategorizationInput> = chunk
            .iter()
            .map(|e| CategorizationInput {
                url: e.url.clone(),
                title: e.title.clone(),
                domain: e.domain.clone(),
            })
            .collect();
        let result = provider.categorize(batch).await?;
        out.extend(result);
    }
    Ok(out)
}
