import { useMemo, useState } from "react";
import { save } from "@tauri-apps/plugin-dialog";
import { api } from "../lib/api";
import type { CategorizedEntry } from "../lib/api";

interface Props {
  items: CategorizedEntry[];
  onChange: (items: CategorizedEntry[]) => void;
}

export function Review({ items, onChange }: Props) {
  const [error, setError] = useState<string | null>(null);
  const [exporting, setExporting] = useState(false);

  const grouped = useMemo(() => {
    const map = new Map<string, CategorizedEntry[]>();
    for (const it of items) {
      const arr = map.get(it.category) ?? [];
      arr.push(it);
      map.set(it.category, arr);
    }
    return Array.from(map.entries()).sort(([a], [b]) => a.localeCompare(b));
  }, [items]);

  function updateCategory(url: string, category: string) {
    onChange(
      items.map((it) => (it.url === url ? { ...it, category } : it)),
    );
  }

  async function handleExport() {
    setError(null);
    try {
      const path = await save({
        defaultPath: "bookmarks.html",
        filters: [{ name: "HTML", extensions: ["html"] }],
      });
      if (!path) return;
      setExporting(true);
      await api.exportHtml(items, path);
    } catch (e) {
      setError(String(e));
    } finally {
      setExporting(false);
    }
  }

  if (items.length === 0) {
    return (
      <>
        <h1>Review</h1>
        <p className="muted">
          Run a scan and categorisation first. The result will appear here so
          you can edit folders before exporting.
        </p>
      </>
    );
  }

  return (
    <>
      <h1>Review</h1>
      <p className="muted">
        {items.length} bookmarks across {grouped.length} folders. Edit a
        category inline to move a bookmark.
      </p>

      {error && <div className="error">{error}</div>}

      <div className="row" style={{ marginBottom: 16 }}>
        <button
          className="primary"
          onClick={handleExport}
          disabled={exporting}
        >
          {exporting ? "Exporting…" : "Export bookmarks.html"}
        </button>
      </div>

      {grouped.map(([category, entries]) => (
        <div className="card" key={category}>
          <h2 style={{ margin: 0 }}>
            {category}{" "}
            <span className="badge">{entries.length}</span>
          </h2>
          <table className="entries">
            <thead>
              <tr>
                <th style={{ width: "40%" }}>Title</th>
                <th style={{ width: "30%" }}>Domain</th>
                <th>Category</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((e) => (
                <tr key={e.url}>
                  <td title={e.url}>{e.title}</td>
                  <td>{e.domain}</td>
                  <td>
                    <input
                      type="text"
                      value={e.category}
                      onChange={(ev) =>
                        updateCategory(e.url, ev.target.value)
                      }
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </>
  );
}
