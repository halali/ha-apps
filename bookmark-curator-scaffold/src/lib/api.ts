import { invoke } from "@tauri-apps/api/core";

// These types mirror the Rust structs in src-tauri. Keep them in sync by hand
// for now; once the surface stabilises we can codegen with `specta` or similar.

export type ProviderKind = "claude" | "ollama";

export interface ClaudeConfig {
  api_key: string;
  model: string;
  base_url: string;
}

export interface OllamaConfig {
  model: string;
  base_url: string;
}

export interface ScanConfig {
  lookback_days: number;
  min_visit_count: number;
  blocklist_domains: string[];
}

export interface Config {
  provider: ProviderKind;
  claude: ClaudeConfig;
  ollama: OllamaConfig;
  scan: ScanConfig;
}

export interface BrowserProfile {
  browser: "chrome";
  name: string;
  path: string;
}

export interface HistoryEntry {
  url: string;
  title: string;
  visit_count: number;
  last_visit: string; // ISO-8601
  domain: string;
}

export interface CategorizedEntry {
  url: string;
  title: string;
  domain: string;
  category: string;
}

export const api = {
  getConfig: () => invoke<Config>("get_config"),
  saveConfig: (cfg: Config) => invoke<void>("save_config", { cfg }),
  listBrowserProfiles: () => invoke<BrowserProfile[]>("list_browser_profiles"),
  scanHistory: (profile: BrowserProfile) =>
    invoke<HistoryEntry[]>("scan_history", { profile }),
  categorize: (entries: HistoryEntry[]) =>
    invoke<CategorizedEntry[]>("categorize", { entries }),
  exportHtml: (items: CategorizedEntry[], path: string) =>
    invoke<void>("export_html", { items, path }),
  testProvider: () => invoke<void>("test_provider"),
};
