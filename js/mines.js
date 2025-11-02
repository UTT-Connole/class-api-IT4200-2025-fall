import React, { useEffect, useMemo, useState } from "react";

// ======== Quick Start ========
// 1) Ensure your Flask API is running on http://127.0.0.1:8000
// 2) This single React component talks to the endpoints:
//    POST   /games
//    GET    /games/:id
//    POST   /games/:id/reveal
//    POST   /games/:id/cashout
// 3) Use the controls to create a game, click cells to reveal, and cash out.
//
// If the UI can’t reach your API due to CORS, add this to Flask:
//   pip install flask-cors
//   from flask_cors import CORS
//   CORS(app, resources={r"/*": {"origins": "*"}})
// (or limit origins to your dev host)

const API_BASE_DEFAULT = "http://127.0.0.1:8000";

export default function MinesUI() {
  const [apiBase, setApiBase] = useState(API_BASE_DEFAULT);
  const [rows, setRows] = useState(5);
  const [cols, setCols] = useState(5);
  const [mines, setMines] = useState(3);
  const [bet, setBet] = useState(100);

  const [game, setGame] = useState(null); // server state snapshot
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const totalCells = useMemo(() => (game ? game.total_cells : rows * cols), [game, rows, cols]);

  useEffect(() => {
    setError("");
  }, [apiBase]);

  async function createGame() {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/games`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rows: Number(rows), cols: Number(cols), mines: Number(mines), bet: Number(bet) }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setGame(data);
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  async function refreshGame() {
    if (!game) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/games/${game.game_id}`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setGame(data);
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  async function reveal(r, c) {
    if (!game || game.is_over) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/games/${game.game_id}/reveal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ row: r, col: c }),
      });
      const txt = await res.text();
      if (!res.ok) throw new Error(txt);
      const data = JSON.parse(txt);
      setGame(data);
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  async function cashout() {
    if (!game || game.is_over) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${apiBase}/games/${game.game_id}/cashout`, { method: "POST" });
      const txt = await res.text();
      if (!res.ok) throw new Error(txt);
      const data = JSON.parse(txt);
      setGame(data);
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  function isRevealed(r, c) {
    if (!game) return false;
    return game.revealed_cells?.some(([rr, cc]) => rr === r && cc === c);
  }

  function isMine(r, c) {
    // Only revealed after game over, for transparency
    if (!game || !game.is_over) return false;
    return game.mine_positions?.some(([rr, cc]) => rr === r && cc === c);
  }

  function renderCell(r, c) {
    const revealed = isRevealed(r, c);
    const mine = isMine(r, c);
    const disabled = (game?.is_over) || revealed || loading;

    let content = "";
    if (game?.is_over && mine) content = "BOMB";
    else if (revealed) content = "OK";

    return (
      <button
        key={`${r}-${c}`}
        onClick={() => reveal(r, c)}
        disabled={disabled}
        className={
          "flex items-center justify-center rounded-xl border text-lg font-semibold h-12 w-12 transition " +
          (disabled ? "opacity-60 cursor-not-allowed " : "hover:scale-[1.02] active:scale-[0.98] ") +
          (revealed ? "bg-emerald-50 border-emerald-300 " : "bg-white border-gray-300 ") +
          (mine && game?.is_over ? "bg-red-50 border-red-300 " : "")
        }
        aria-label={`Cell ${r},${c}`}
      >
        {content || ""}
      </button>
    );
  }

  function Grid() {
    const r = game?.rows ?? rows;
    const c = game?.cols ?? cols;

    return (
      <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${c}, minmax(0, 1fr))` }}>
        {Array.from({ length: r }).map((_, ri) =>
          Array.from({ length: c }).map((_, ci) => renderCell(ri, ci))
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-slate-50 to-slate-100 text-slate-900">
      <div className="max-w-5xl mx-auto p-6">
        <header className="flex items-center justify-between gap-4 mb-6">
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">DIAMOND Mines - Play‑Money</h1>
          <div className="flex items-center gap-2">
            <input
              className="px-3 py-2 rounded-xl border border-slate-300 bg-white focus:outline-none focus:ring-2 focus:ring-slate-300 text-sm w-64"
              value={apiBase}
              onChange={(e) => setApiBase(e.target.value)}
              placeholder="API base (http://127.0.0.1:8000)"
            />
            <button
              onClick={refreshGame}
              className="px-3 py-2 rounded-xl bg-slate-900 text-white text-sm font-semibold shadow hover:shadow-md"
            >
              Refresh
            </button>
          </div>
        </header>

        {/* Controls / Create Game */}
        <section className="mb-6">
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 bg-white rounded-2xl p-4 shadow">
            <div className="flex flex-col">
              <label className="text-xs font-medium text-slate-600">Rows</label>
              <input type="number" min={2} className="px-3 py-2 rounded-xl border border-slate-300"
                     value={rows} onChange={(e)=>setRows(parseInt(e.target.value||"0",10))} />
            </div>
            <div className="flex flex-col">
              <label className="text-xs font-medium text-slate-600">Cols</label>
              <input type="number" min={2} className="px-3 py-2 rounded-xl border border-slate-300"
                     value={cols} onChange={(e)=>setCols(parseInt(e.target.value||"0",10))} />
            </div>
            <div className="flex flex-col">
              <label className="text-xs font-medium text-slate-600">Mines</label>
              <input type="number" min={1} className="px-3 py-2 rounded-xl border border-slate-300"
                     value={mines} onChange={(e)=>setMines(parseInt(e.target.value||"0",10))} />
            </div>
            <div className="flex flex-col">
              <label className="text-xs font-medium text-slate-600">Bet (play‑money)</label>
              <input type="number" min={0} className="px-3 py-2 rounded-xl border border-slate-300"
                     value={bet} onChange={(e)=>setBet(parseFloat(e.target.value||"0"))} />
            </div>
            <div className="flex items-end">
              <button
                onClick={createGame}
                disabled={loading}
                className="w-full px-4 py-3 rounded-2xl bg-emerald-600 text-white font-semibold shadow hover:shadow-md disabled:opacity-60"
              >
                {loading ? "Creating…" : "Create Game"}
              </button>
            </div>
          </div>
        </section>

        {/* Game Panel */}
        {game && (
          <section className="grid md:grid-cols-5 gap-6">
            <div className="md:col-span-3">
              <div className="bg-white rounded-2xl p-4 shadow">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <div className="text-sm text-slate-500">Game ID</div>
                    <div className="font-mono text-xs break-all">{game.game_id}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-500">Multiplier</div>
                    <div className="text-xl font-bold">× {Number(game.current_multiplier || 1).toFixed(4)}</div>
                  </div>
                </div>

                <Grid />

                <div className="mt-4 flex items-center justify-between">
                  <div className="text-sm text-slate-600">
                    Revealed: <strong>{game.safe_revealed}</strong> / Safe Total: <strong>{game.safe_total}</strong> / Cells: <strong>{totalCells}</strong>
                  </div>
                  <div className="flex items-center gap-3">
                    {!game.is_over ? (
                      <button
                        onClick={cashout}
                        disabled={loading}
                        className="px-4 py-2 rounded-xl bg-blue-600 text-white font-semibold shadow hover:shadow-md disabled:opacity-60"
                      >
                        Cash Out
                      </button>
                    ) : (
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${game.is_bust ? "bg-red-100 text-red-700" : "bg-emerald-100 text-emerald-700"}`}>
                        {game.is_bust ? "BUST" : "CASHED OUT"}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <aside className="md:col-span-2">
              <div className="bg-white rounded-2xl p-4 shadow space-y-3">
                <h2 className="text-lg font-semibold">Game Summary</h2>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="text-slate-500">Rows</div>
                  <div className="font-medium">{game.rows}</div>
                  <div className="text-slate-500">Cols</div>
                  <div className="font-medium">{game.cols}</div>
                  <div className="text-slate-500">Mines</div>
                  <div className="font-medium">{game.mines}</div>
                  <div className="text-slate-500">Bet</div>
                  <div className="font-medium">{Number(game.bet || 0).toFixed(2)}</div>
                  <div className="text-slate-500">Status</div>
                  <div className="font-medium">{game.is_over ? (game.is_bust ? "Bust" : "Cashed Out") : "In progress"}</div>
                  <div className="text-slate-500">Payout</div>
                  <div className="font-medium">{game.cashout_amount != null ? Number(game.cashout_amount).toFixed(4) : "-"}</div>
                  <div className="text-slate-500">Created</div>
                  <div className="font-medium">{new Date(game.created_at).toLocaleString()}</div>
                </div>

                {game.is_over && game.mine_positions && (
                  <div className="pt-2">
                    <div className="text-sm text-slate-600 mb-1">Mines revealed (after game end)</div>
                    <div className="text-xs font-mono break-all bg-slate-50 border rounded-xl p-2">
                      {JSON.stringify(game.mine_positions)}
                    </div>
                  </div>
                )}

                {error && (
                  <div className="text-sm text-red-700 bg-red-50 border border-red-200 rounded-xl p-2">{error}</div>
                )}
              </div>

              <div className="mt-4 text-xs text-slate-500">
                Tip: You can change the API base at the top if your backend runs elsewhere.
              </div>
            </aside>
          </section>
        )}

        {!game && (
          <div className="text-sm text-slate-600">
            Create a game to get started. Click any tile to reveal. Cash out anytime. If you bust, mines are revealed.
          </div>
        )}
      </div>
    </div>
  );
}
