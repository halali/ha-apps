import { useState } from "react";
import { Scan } from "./pages/Scan";
import { Review } from "./pages/Review";
import { Settings } from "./pages/Settings";
import type { CategorizedEntry } from "./lib/api";

type Page = "scan" | "review" | "settings";

export function App() {
  const [page, setPage] = useState<Page>("scan");
  const [categorized, setCategorized] = useState<CategorizedEntry[]>([]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-title">bookmark-curator</div>
        <NavButton active={page === "scan"} onClick={() => setPage("scan")}>
          Scan
        </NavButton>
        <NavButton active={page === "review"} onClick={() => setPage("review")}>
          Review
        </NavButton>
        <NavButton
          active={page === "settings"}
          onClick={() => setPage("settings")}
        >
          Settings
        </NavButton>
      </aside>

      <main className="main">
        {page === "scan" && (
          <Scan
            onCategorized={(items) => {
              setCategorized(items);
              setPage("review");
            }}
          />
        )}
        {page === "review" && (
          <Review items={categorized} onChange={setCategorized} />
        )}
        {page === "settings" && <Settings />}
      </main>
    </div>
  );
}

function NavButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      className={`nav-button${active ? " active" : ""}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
