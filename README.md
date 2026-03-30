# サークルアップ連携PJ｜運用（oya-ui）

声掛けダッシュボード・GAS・運用メモの置き場です。

## ダッシュボード（上司共有用HTMLの元）

```bash
python3 dashboard/build_dashboard.py
```

生成物: `声掛け_dashboard.html` と **`index.html`（同一・Netlify のトップ用）**  
詳細: [dashboard/README.md](dashboard/README.md)  
Netlify は **`index.html` がリポジトリルート** にないと `/` が 404 になる。`netlify.toml` で `publish = "."` を指定済み。

## その他

- `運用_リンク一覧.md` … フォーム・スプレッドシート・資料のURL
- `gas/` … Google Apps Script のローカルコピー

## GitHub へプッシュする

リモート: **`https://github.com/oya-ui/circle-up-format.git`**（ユーザー `oya-ui`・リポジトリ `circle-up-format`）

```bash
cd "/Users/oyataiga/Documents/Obsidian Vault/business/01_project/サークルアップ/運用"
git push -u origin main
```

初回は GitHub 側で空の **`circle-up-format`** を作成してから push。認証は **SSH** または **HTTPS + Personal Access Token**。`Repository not found` は未作成・権限・未ログインを確認。
