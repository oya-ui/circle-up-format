# 声掛けダッシュボード

Google スプレッドシート（声掛け管理）の **CSV export** を読み、`声掛け_dashboard.html` を生成します。

## 必要なもの

- Python 3（標準ライブラリのみ・追加パッケージ不要）
- スプレッドシートが **リンクを知っている全員が閲覧可** など、export URL から CSV が取れる状態

## 使い方

```bash
cd "/Users/oyataiga/Documents/Obsidian Vault/business/01_project/サークルアップ/運用"
python3 dashboard/build_dashboard.py
```

ブラウザで同フォルダの **`声掛け_dashboard.html`** を開く。

## ファイル

| ファイル | 役割 |
|----------|------|
| `config.json` | CSV の URL、G1エリア目標、G2/G3の目標と**手入力実績**、`stageOrder`（ステージ表の並び） |
| `daily_memo.txt` | 会議用の **当日メモ・見込み**（ここだけ手で書いてから再生成） |
| `build_dashboard.py` | 取得・集計・HTML出力 |
| `last_snapshot.csv` | 直近成功した取得結果（自動保存・取得失敗時のフォールバックに使用） |

## 集計ルール

- **有効行**: **正式名称（B列）が空でない行**だけ（リポジトリのスキル `circleup-weekly-metrics` と同じ）
- **ステージ別・エリア別**: 有効行をカウント

## G2 / G3 の実績

フォーム回答シートはまだ自動連携していません。実績を出したい日は `config.json` の `g2.actual` / `g3.actual` に数値を入れてから再実行してください（`null` は「—」表示）。

## ステージの並び

スプレッドシートでステージ名を変えたら、`config.json` の `stageOrder` に **上から順に** 配列で列挙すると、ダッシュボードの表がその順になります。空のままならステージ名のソート順になります。

例:

```json
"stageOrder": [
  "未接触",
  "団体声かけ",
  "三角LG作成",
  "フォーム打診",
  "HP中間報告会調整済み",
  "三角LINE実施済み"
]
```

（実際の表記はシートのドロップダウンと **完全一致** させてください。）
