# Google フォーム作成スクリプト（GAS）

## 本番・回答用URL（幹部・依頼先に配布）

**回答用（viewform）**  
https://docs.google.com/forms/d/e/1FAIpQLSeFVBEoz5WxbuBQQ8pHczL3kePpmTCcD34eieh0Tgg8ynYjgQ/viewform  

※ フォームを GAS で作り直した場合は、この URL および `運用_リンク一覧.md` を更新すること。

## ファイル

- `CircleHpRequestForm.gs` … `createCircleHpRequestForm` を実行すると、依頼フォームと回答用スプレッドシートが作成されます（**既に本番フォームがある場合は再実行で二重作成に注意**）。
- `OutreachManagementSheet.gs` … `createOutreachManagementSheet` を実行すると、**声掛け管理**用の1シート構成スプレッドシートが新規作成されます（列・入力規則つき）。**再実行するたびに別ファイルが増える**ので、本番URLは `運用_リンク一覧.md` などに記録してください。  
  **コードを読まなくてよい説明** → [OutreachManagementSheet.md](OutreachManagementSheet.md)

## 手順

1. [Google Apps Script](https://script.google.com/) でプロジェクトを新規作成する。
2. `Code.gs` の中身を `CircleHpRequestForm.gs` の内容に置き換える（またはファイルをコピー）。
3. 保存し、作成したい関数を選んで **実行**。
   - 依頼フォーム一式: **`createCircleHpRequestForm`**
   - 声掛け管理シートのみ: **`createOutreachManagementSheet`**
4. 初回は権限の承認（フォーム・スプレッドシートの作成）を求められる。
5. **実行ログ**（表示メニュー → ログ）に、作成物のURLが出力される。

## トラブルシュート

- **画像の受け取り**  
  現行スクリプトは、画像をフォームに添付させず、**LINE のアルバム（または写真のまとめ）で担当に送付**する前提の文言になっています。  
  担当の LINE（公式アカウント／オープンチャット／担当者個人）の案内は、**フォームの説明文に追記**するか、依頼メッセージとセットで送ってください。

- **`TypeError: form.addFileUploadItem` / `addItem`（過去版）**  
  スクリプトからファイルアップロード設問を作らない方針のため、該当コードは使っていません。画像をフォームで受けたい場合は、作成後に編集画面から手動で「ファイルアップロード」を追加してください。

- **回答用URLが知りたい**  
  フォームの編集画面を開く → 右上「送信」→ リンクアイコンから取得。

## 長期インターン向けインセンティブ（運用メモ）

- **楠と面談実施**: 2,000円 / 団体  
- **サークルアップ導入開始後**: 5,000円 / 団体  

※ 契約・支払い条件は担当（楠・契約窓口）の最新案内に従うこと。
