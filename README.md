# サークルアップ連携PJ｜運用（oya-ui）

声掛けダッシュボード・GAS・運用メモの置き場です。

## ダッシュボード（上司共有用HTMLの元）

```bash
python3 dashboard/build_dashboard.py
```

生成物: `声掛け_dashboard.html`  
詳細: [dashboard/README.md](dashboard/README.md)

## その他

- `運用_リンク一覧.md` … フォーム・スプレッドシート・資料のURL
- `gas/` … Google Apps Script のローカルコピー

## GitHub（oya-ui）へプッシュする

このフォルダは `git init` 済み。**初回プッシュ前**に GitHub 側で空のリポジトリ `oya-ui` を作成してください（README テンプレは付けないと楽です）。

アカウント名が `oyataiga` でない場合は URL を差し替えます。

```bash
cd "/Users/oyataiga/Documents/Obsidian Vault/business/01_project/サークルアップ/運用"
git remote -v   # origin が違うURLなら次で修正
git remote set-url origin https://github.com/<あなたのユーザー名>/oya-ui.git
git push -u origin main
```

認証は **GitHub CLI**、**SSH（git@github.com:…）**、または **HTTPS + Personal Access Token** のいずれかが必要です。`Repository not found` のときは「リポジトリ未作成」「ユーザー名違い」「未ログイン」のどれかです。
