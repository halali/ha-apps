import { useEffect, useState } from "react";
import { api } from "../lib/api";
import type {
  BrowserProfile,
  CategorizedEntry,
  HistoryEntry,
} from "../lib/api";

interface Props {
  onCategorized: (items: CategorizedEntry[]) => void;
}

export function Scan({ onCategorized }: Props) {
  const [profiles, setProfiles] = useState<BrowserProfile[]>([]);
  const [selected, setSelected] = useState<BrowserProfile | null>(null);
  const [entries, setEntries] = useState<HistoryEntry[]>([]);
  const [busy, setBusy] = useState<"idle" | "scanning" | "categorizing">(
    "idle",
  );
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listBrowserProfiles()
      .then((p) => {
        setProfiles(p);
        if (p.length > 0) setSelected(p[0]);
      })
      .catch((e) => setError(String(e)));
  }, []);

  async function handleScan() {
    if (!selected) return;
    setBusy("scanning");
    setError(null);
    try {
      const result = await api.scanHistory(selected);
      setEntries(result);
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy("idle");
    }
  }

  async function handleCategorize() {
    if (entries.length === 0) return;
    setBusy("categorizing");
    setError(null);
    try {
      const result = await api.categorize(entries);
      onCategorized(result);
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy("idle");
    }
  }

  return (
    <>
      <h1>Scan</h1>
      <p className="muted">
        Pick a Chrome profile, fetch its history, then send it through the
        currently configured AI provider.
      </p>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <label>Chrome profile</label>
        {profiles.length === 0 ? (
          <p className="muted">
            No Chrome profiles found on this machine.
          </p>
        ) : (
          <select
            value={selected?.path ?? ""}
            onChange={(e) =>
              setSelected(
                profiles.find((p) => p.path === e.target.value) ?? null,
              )
            }
          >
            {profiles.map((p) => (
              <option key={p.path} value={p.path}>
                {p.name} — {p.path}
              </option>
            ))}
          </select>
        )}

        <div className="row" style={{ marginTop: 16 }}>
          <button
            className="primary"
            onClick={handleScan}
            disabled={!selected || busy !== "idle"}
          >
            {busy === "scanning" ? "Scanning…" : "Scan history"}
          </button>
          <button
            className="secondary"
            onClick={handleCategorize}
            disabled={entries.length === 0 || busy !== "idle"}
          >
            {busy === "categorizing"
              ? "Categorising…"
              : `Categorise ${entries.length || ""} entries`}
          </button>
        </div>
      </div>

      {entries.length > 0 && (
        <>
          <h2>Preview ({entries.length} entries)</h2>
          <table className="entries">
            <thead>
              <tr>
                <th>Title</th>
                <th>Domain</th>
                <th>Visits</th>
                <th>Last visit</th>
              </tr>
            </thead>
            <tbody>
              {entries.slice(0, 50).map((e) => (
                <tr key={e.url}>
                  <td>{e.title}</td>
                  <td>{e.domain}</td>
                  <td>{e.visit_count}</td>
                  <td>{new Date(e.last_visit).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {entries.length > 50 && (
            <p className="muted">…and {entries.length - 50} more.</p>
          )}
        </>
      )}
    </>
  );
}
