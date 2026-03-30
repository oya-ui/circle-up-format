#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
声掛け管理シート（CSV export）を取得し、声掛け_dashboard.html を生成する。

使い方:
  cd .../運用/dashboard
  python3 build_dashboard.py

  オプション:
  --offline   同フォルダの last_snapshot.csv があればそれを使い取得しない
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DIR = Path(__file__).resolve().parent
ROOT = DIR.parent
CONFIG_PATH = DIR / "config.json"
MEMO_PATH = DIR / "daily_memo.txt"
OUT_HTML = ROOT / "声掛け_dashboard.html"
SNAPSHOT_PATH = DIR / "last_snapshot.csv"

HEADERS_EXPECTED = [
    "団体ID",
    "正式名称",
    "大学",
    "エリア",
    "ステージ",
    "最終接触日",
    "次アクション日",
    "担当",
    "チャネル",
    "反応",
    "次の一手メモ",
]


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def load_memo() -> str:
    if not MEMO_PATH.exists():
        return ""
    return MEMO_PATH.read_text(encoding="utf-8").strip()


def fetch_csv(url: str) -> str:
    req = Request(url, headers={"User-Agent": "CircleUpDashboard/1.0"})
    with urlopen(req, timeout=60) as resp:
        raw = resp.read()
    return raw.decode("utf-8")


def parse_csv(text: str) -> list[dict[str, str]]:
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return []
    header = rows[0]
    # ヘッダ名の揺れに少し寛容
    idx = {name.strip(): i for i, name in enumerate(header)}
    out = []
    for parts in rows[1:]:
        if not parts or all(not (c or "").strip() for c in parts):
            continue
        row = {}
        for name in HEADERS_EXPECTED:
            i = idx.get(name)
            row[name] = (parts[i].strip() if i is not None and i < len(parts) else "") if i is not None else ""
        out.append(row)
    return out


def filter_valid(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [r for r in rows if (r.get("正式名称") or "").strip()]


def sort_stage_items(counter: Counter, order: list[str]) -> list[tuple[str, int]]:
    items = list(counter.items())
    order_index = {name: i for i, name in enumerate(order)}

    def key(x: tuple[str, int]) -> tuple:
        name, _ = x
        if name in order_index:
            return (0, order_index[name], name)
        return (1, name)

    items.sort(key=key)
    return items


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fmt_num(n: float | int | None) -> str:
    if n is None:
        return "—"
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return str(n)


def build_html(
    *,
    fetched_at: str,
    config: dict,
    memo: str,
    rows_valid: list[dict[str, str]],
    by_area: Counter,
    by_stage: Counter,
    source_note: str,
) -> str:
    g1 = config.get("g1") or {}
    targets: dict[str, int] = dict(g1.get("perAreaTarget") or {})
    area_order = ["仙台", "東京", "札幌", "その他"]

    # その他: 設定に無いエリアも実績に出す
    for a in by_area:
        if a not in targets and a:
            targets.setdefault(a, 0)

    total_target = sum(targets.get(a, 0) for a in area_order if a in targets) + sum(
        v for k, v in targets.items() if k not in area_order and k != ""
    )
    total_actual = len(rows_valid)

    stage_order = list(config.get("stageOrder") or [])
    stage_items = sort_stage_items(by_stage, stage_order)
    max_stage = max((c for _, c in stage_items), default=0) or 1

    g2 = config.get("g2") or {}
    g3 = config.get("g3") or {}

    rows_area_html = []
    for area in area_order:
        if area not in targets and by_area.get(area, 0) == 0:
            continue
        t = targets.get(area, 0)
        act = by_area.get(area, 0)
        pct = min(100, int(100 * act / t)) if t else 0
        rows_area_html.append(
            f"<tr><td><strong>{escape_html(area)}</strong></td>"
            f'<td class="num">{act}</td><td class="num">{t if t else "—"}</td>'
            f'<td><div class="bar"><span style="width:{pct}%"></span></div></td></tr>'
        )
    for area, act in sorted(by_area.items()):
        if area in area_order or not area:
            continue
        t = targets.get(area, 0)
        pct = min(100, int(100 * act / t)) if t else 0
        rows_area_html.append(
            f"<tr><td><strong>{escape_html(area)}</strong></td>"
            f'<td class="num">{act}</td><td class="num">{t if t else "—"}</td>'
            f'<td><div class="bar"><span style="width:{pct}%"></span></div></td></tr>'
        )

    rows_stage_html = []
    for name, cnt in stage_items:
        label = name if name else "（ステージ未設定）"
        pct = int(100 * cnt / max_stage)
        rows_stage_html.append(
            f"<tr><td>{escape_html(label)}</td><td class=\"num\">{cnt}</td>"
            f'<td><div class="bar bar-stage"><span style="width:{pct}%"></span></div></td></tr>'
        )

    memo_block = (
        f'<section class="card"><h2>当日メモ・見込み</h2><pre class="memo">{escape_html(memo)}</pre>'
        f'<p class="hint">編集: <code>dashboard/daily_memo.txt</code> → 再実行</p></section>'
        if memo
        else '<section class="card"><h2>当日メモ・見込み</h2><p class="muted">（空）<code>dashboard/daily_memo.txt</code> に追記してください</p></section>'
    )

    g2_actual = g2.get("actual")
    g3_actual = g3.get("actual")

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>サークルアップ連携PJ｜声掛けダッシュボード</title>
  <style>
    :root {{
      --bg: #f4f5f8;
      --card: #fff;
      --text: #1c1f26;
      --muted: #5a6270;
      --border: #dde1ea;
      --accent: #1d4ed8;
      --accent-soft: #eff6ff;
      --ok: #15803d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 1.25rem 1rem 2rem;
      font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif;
      font-size: 14px;
      line-height: 1.5;
      color: var(--text);
      background: var(--bg);
    }}
    .wrap {{ max-width: 960px; margin: 0 auto; }}
    header {{
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      justify-content: space-between;
      gap: 0.5rem 1rem;
      margin-bottom: 1rem;
    }}
    h1 {{ margin: 0; font-size: 1.35rem; }}
    .meta {{ font-size: 0.85rem; color: var(--muted); }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 0.75rem;
      margin-bottom: 1rem;
    }}
    .kpi {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.85rem 1rem;
      box-shadow: 0 1px 3px rgba(0,0,0,.06);
    }}
    .kpi .t {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }}
    .kpi .v {{ font-size: 1.5rem; font-weight: 700; font-variant-numeric: tabular-nums; margin-top: 0.2rem; }}
    .kpi .sub {{ font-size: 0.8rem; color: var(--muted); margin-top: 0.25rem; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1rem 1.15rem 1.15rem;
      margin-bottom: 1rem;
      box-shadow: 0 1px 3px rgba(0,0,0,.06);
    }}
    h2 {{
      margin: 0 0 0.65rem;
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--muted);
      letter-spacing: 0.04em;
    }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    th, td {{ border: 1px solid var(--border); padding: 0.45rem 0.55rem; text-align: left; vertical-align: middle; }}
    th {{ background: var(--accent-soft); font-weight: 600; }}
    tr:nth-child(even) td {{ background: #fafbfd; }}
    .num {{ font-variant-numeric: tabular-nums; text-align: right; font-weight: 600; }}
    .bar {{
      height: 8px;
      background: #e5e7eb;
      border-radius: 4px;
      overflow: hidden;
      min-width: 80px;
    }}
    .bar span {{
      display: block;
      height: 100%;
      background: var(--accent);
      border-radius: 4px;
    }}
    .bar-stage span {{ background: #6366f1; }}
    pre.memo {{
      margin: 0;
      white-space: pre-wrap;
      font-family: inherit;
      font-size: 0.92rem;
      line-height: 1.55;
    }}
    .hint {{ font-size: 0.78rem; color: var(--muted); margin: 0.5rem 0 0; }}
    .muted {{ color: var(--muted); font-size: 0.9rem; }}
    code {{ font-size: 0.85em; background: #f1f5f9; padding: 0.1em 0.35em; border-radius: 4px; }}
    footer {{ font-size: 0.78rem; color: var(--muted); margin-top: 1rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>サークルアップ連携PJ｜声掛けダッシュボード</h1>
      <span class="meta">データ取得: {escape_html(fetched_at)}<br />{escape_html(source_note)}</span>
    </header>

    <div class="grid">
      <div class="kpi">
        <div class="t">G1 有効団体（全体）</div>
        <div class="v">{total_actual} <span style="font-size:0.95rem;font-weight:600;color:var(--muted)">/ 目標合計 {total_target}</span></div>
        <div class="sub">{escape_html(g1.get("label", ""))}</div>
      </div>
      <div class="kpi">
        <div class="t">{escape_html(g2.get("label", "G2"))}</div>
        <div class="v">{fmt_num(g2_actual)} <span style="font-size:0.95rem;font-weight:600;color:var(--muted)">/ {fmt_num(g2.get("target"))}</span></div>
        <div class="sub">{escape_html(g2.get("description", ""))}（実績は <code>config.json</code>）</div>
      </div>
      <div class="kpi">
        <div class="t">{escape_html(g3.get("label", "G3"))}</div>
        <div class="v">{fmt_num(g3_actual)} <span style="font-size:0.95rem;font-weight:600;color:var(--muted)">/ {fmt_num(g3.get("target"))}</span></div>
        <div class="sub">{escape_html(g3.get("description", ""))}（実績は <code>config.json</code>）</div>
      </div>
    </div>

    <section class="card">
      <h2>エリア別（実績 / 目標）</h2>
      <div style="overflow-x:auto">
        <table>
          <thead><tr><th>エリア</th><th class="num">実績</th><th class="num">目標</th><th>進捗</th></tr></thead>
          <tbody>
            {"".join(rows_area_html)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="card">
      <h2>ステージ別（有効団体の人数）</h2>
      <div style="overflow-x:auto">
        <table>
          <thead><tr><th>ステージ</th><th class="num">件数</th><th>内訳バー（最大比）</th></tr></thead>
          <tbody>
            {"".join(rows_stage_html)}
          </tbody>
        </table>
      </div>
      <p class="hint">並び順は <code>dashboard/config.json</code> の <code>stageOrder</code>（先に書いた順）。空なら五十音順相当。</p>
    </section>

    {memo_block}

    <footer>
      生成: <code>python3 dashboard/build_dashboard.py</code> ・ 設定: <code>dashboard/config.json</code>
    </footer>
  </div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="last_snapshot.csv を使う")
    args = parser.parse_args()

    config = load_config()
    memo = load_memo()
    url = config.get("csvExportUrl", "").strip()

    source_note = ""
    if args.offline and SNAPSHOT_PATH.exists():
        text = SNAPSHOT_PATH.read_text(encoding="utf-8")
        fetched_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
        source_note = "オフラインモード: last_snapshot.csv"
    else:
        if not url:
            print("config.json に csvExportUrl がありません")
            return 1
        try:
            text = fetch_csv(url)
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            print(f"CSV 取得に失敗: {e}")
            if SNAPSHOT_PATH.exists():
                print("last_snapshot.csv にフォールバックします")
                text = SNAPSHOT_PATH.read_text(encoding="utf-8")
                source_note = "取得失敗のためスナップショットを使用"
            else:
                return 1
        else:
            SNAPSHOT_PATH.write_text(text, encoding="utf-8")
            source_note = "CSV export（最新を取得）"
        fetched_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")

    rows = parse_csv(text)
    valid = filter_valid(rows)
    by_area = Counter()
    by_stage = Counter()
    for r in valid:
        a = (r.get("エリア") or "").strip() or "（エリア未設定）"
        by_area[a] += 1
        s = (r.get("ステージ") or "").strip()
        by_stage[s] += 1

    html = build_html(
        fetched_at=fetched_at,
        config=config,
        memo=memo,
        rows_valid=valid,
        by_area=by_area,
        by_stage=by_stage,
        source_note=source_note,
    )
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")
    print(f"  有効行: {len(valid)}  エリア種別: {len(by_area)}  ステージ種別: {len(by_stage)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
