import { useEffect, useState } from "react";
import { api } from "../lib/api";
import type { Config, ProviderKind } from "../lib/api";

export function Settings() {
  const [cfg, setCfg] = useState<Config | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const [testResult, setTestResult] = useState<string | null>(null);

  useEffect(() => {
    api
      .getConfig()
      .then(setCfg)
      .catch((e) => setError(String(e)));
  }, []);

  async function handleSave() {
    if (!cfg) return;
    setError(null);
    try {
      await api.saveConfig(cfg);
      setSavedAt(Date.now());
    } catch (e) {
      setError(String(e));
    }
  }

  async function handleTest() {
    setTestResult("Testing…");
    try {
      await api.testProvider();
      setTestResult("✓ Provider is reachable.");
    } catch (e) {
      setTestResult(`✗ ${e}`);
    }
  }

  if (!cfg) return <p>Loading…</p>;

  return (
    <>
      <h1>Settings</h1>
      <p className="muted">
        Stored in <code>~/Library/Application Support/bookmark-curator/config.toml</code>.
      </p>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <label>AI provider</label>
        <select
          value={cfg.provider}
          onChange={(e) =>
            setCfg({ ...cfg, provider: e.target.value as ProviderKind })
          }
        >
          <option value="claude">Claude (Anthropic API)</option>
          <option value="ollama">Ollama (local)</option>
        </select>
      </div>

      {cfg.provider === "claude" && (
        <div className="card">
          <h2 style={{ marginTop: 0 }}>Claude</h2>
          <label>API key</label>
          <input
            type="password"
            value={cfg.claude.api_key}
            onChange={(e) =>
              setCfg({
                ...cfg,
                claude: { ...cfg.claude, api_key: e.target.value },
              })
            }
            placeholder="sk-ant-…"
          />
          <label>Model</label>
          <input
            type="text"
            value={cfg.claude.model}
            onChange={(e) =>
              setCfg({
                ...cfg,
                claude: { ...cfg.claude, model: e.target.value },
              })
            }
          />
          <label>Base URL</label>
          <input
            type="text"
            value={cfg.claude.base_url}
            onChange={(e) =>
              setCfg({
                ...cfg,
                claude: { ...cfg.claude, base_url: e.target.value },
              })
            }
          />
        </div>
      )}

      {cfg.provider === "ollama" && (
        <div className="card">
          <h2 style={{ marginTop: 0 }}>Ollama</h2>
          <label>Model</label>
          <input
            type="text"
            value={cfg.ollama.model}
            onChange={(e) =>
              setCfg({
                ...cfg,
                ollama: { ...cfg.ollama, model: e.target.value },
              })
            }
          />
          <label>Base URL</label>
          <input
            type="text"
            value={cfg.ollama.base_url}
            onChange={(e) =>
              setCfg({
                ...cfg,
                ollama: { ...cfg.ollama, base_url: e.target.value },
              })
            }
          />
        </div>
      )}

      <div className="card">
        <h2 style={{ marginTop: 0 }}>Scan</h2>
        <label>Lookback (days)</label>
        <input
          type="number"
          min={1}
          value={cfg.scan.lookback_days}
          onChange={(e) =>
            setCfg({
              ...cfg,
              scan: {
                ...cfg.scan,
                lookback_days: Math.max(1, Number(e.target.value) || 1),
              },
            })
          }
        />
        <label>Minimum visit count</label>
        <input
          type="number"
          min={1}
          value={cfg.scan.min_visit_count}
          onChange={(e) =>
            setCfg({
              ...cfg,
              scan: {
                ...cfg.scan,
                min_visit_count: Math.max(1, Number(e.target.value) || 1),
              },
            })
          }
        />
        <label>Blocklist domains (one per line)</label>
        <textarea
          rows={5}
          value={cfg.scan.blocklist_domains.join("\n")}
          onChange={(e) =>
            setCfg({
              ...cfg,
              scan: {
                ...cfg.scan,
                blocklist_domains: e.target.value
                  .split("\n")
                  .map((s) => s.trim())
                  .filter(Boolean),
              },
            })
          }
        />
      </div>

      <div className="row">
        <button className="primary" onClick={handleSave}>
          Save
        </button>
        <button className="secondary" onClick={handleTest}>
          Test connection
        </button>
        {savedAt && (
          <span className="muted">
            Saved {new Date(savedAt).toLocaleTimeString()}.
          </span>
        )}
        {testResult && <span className="muted">{testResult}</span>}
      </div>
    </>
  );
}
