/**
 * 声掛け管理用スプレッドシート（1シート）を新規作成する
 *
 * 使い方:
 * 1. https://script.google.com/ で「新しいプロジェクト」（または既存PJにファイル追加）
 * 2. このコードを貼り付け
 * 3. 保存 → 関数 createOutreachManagementSheet を選択 →「実行」
 * 4. 初回は権限承認（スプレッドシートの作成）
 * 5. 実行ログにスプレッドシートURLが出力される
 *
 * 注意:
 * - 再実行のたびに**新しい**スプレッドシートが増えます。本番用は1回作ったらURLをメモし、以降は手編集してください。
 */

function createOutreachManagementSheet() {
  const title = 'サークルアップ連携PJ｜声掛け管理';
  const ss = SpreadsheetApp.create(title);
  const sheet = ss.getSheets()[0];
  sheet.setName('声掛け管理');

  const headers = [
    '団体ID',
    '正式名称',
    '大学',
    'エリア',
    'ステージ',
    '最終接触日',
    '次アクション日',
    '担当',
    'チャネル',
    '反応',
    '次の一手メモ',
  ];

  const numCols = headers.length;
  const maxRow = 2000;

  sheet.getRange(1, 1, 1, numCols).setValues([headers]);
  sheet
    .getRange(1, 1, 1, numCols)
    .setFontWeight('bold')
    .setBackground('#eff6ff')
    .setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);

  sheet.setFrozenRows(1);

  // 列幅（目安）
  sheet.setColumnWidth(1, 72);
  sheet.setColumnWidth(2, 160);
  sheet.setColumnWidth(3, 140);
  sheet.setColumnWidth(4, 72);
  sheet.setColumnWidth(5, 100);
  sheet.setColumnWidth(6, 110);
  sheet.setColumnWidth(7, 110);
  sheet.setColumnWidth(8, 88);
  sheet.setColumnWidth(9, 120);
  sheet.setColumnWidth(10, 88);
  sheet.setColumnWidth(11, 280);

  const bodyStart = 2;

  // D列: エリア
  const areaRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['仙台', '東京', '札幌', 'その他'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange(bodyStart, 4, maxRow, 4).setDataValidation(areaRule);

  // E列: ステージ（運用で文言を増やす場合はセルに直接入力可）
  const stageRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(
      [
        '未接触',
        '接触済',
        '説明予定',
        '説明済',
        'フォーム送付済',
        '保留',
        '辞退',
      ],
      true
    )
    .setAllowInvalid(true)
    .build();
  sheet.getRange(bodyStart, 5, maxRow, 5).setDataValidation(stageRule);

  // F, G列: 日付（空欄可・和暦テキストも許容）
  const dateRule = SpreadsheetApp.newDataValidation().requireDate().setAllowInvalid(true).build();
  sheet.getRange(bodyStart, 6, maxRow, 7).setDataValidation(dateRule);

  // I列: チャネル
  const channelRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['メンター紹介', '自己開拓', '既存接点', '紹介', 'その他'], true)
    .setAllowInvalid(true)
    .build();
  sheet.getRange(bodyStart, 9, maxRow, 9).setDataValidation(channelRule);

  // J列: 反応
  const reactionRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['前向き', '検討中', '無反応', '—'], true)
    .setAllowInvalid(true)
    .build();
  sheet.getRange(bodyStart, 10, maxRow, 10).setDataValidation(reactionRule);

  const ssUrl = ss.getUrl();
  Logger.log('--- 作成完了 ---');
  Logger.log('声掛け管理スプレッドシート: ' + ssUrl);
}
