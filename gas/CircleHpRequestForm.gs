/**
 * サークル新歓用HP（紹介ページ）依頼フォームを Google フォームで作成する
 *
 * 使い方:
 * 1. https://script.google.com/ で「新しいプロジェクト」
 * 2. このコードを貼り付け
 * 3. 「保存」→ 関数 createCircleHpRequestForm を選択 →「実行」
 * 4. 初回は権限承認（フォーム作成・スプレッドシート作成）
 * 5. ログにフォームURLとスプレッドシートURLが出る
 *
 * 注意:
 * - 画像はフォームでは受け付けず、「LINE のアルバム（または写真のまとめ）で担当に送付」する前提の文言にしています。
 * - 担当の LINE アカウント・オープンチャット URL は、フォーム説明文または別途配布の案内に追記してください。
 */

function createCircleHpRequestForm() {
  const formTitle = '【サークルアップ連携】新歓用サークル紹介ページ（HP）作成 依頼フォーム';
  const form = FormApp.create(formTitle);
  form.setDescription(
    '新歓向けのサークル紹介ページを作成するための情報を入力してください。\n' +
      '【写真について】掲載したい写真は、本フォームの送信後、担当者よりご案内する LINE のトークに、' +
      'アルバムにまとめて送付してください（URL貼付やフォームへの画像添付は不要です）。\n' +
      '不明点は担当（Geek長期インターン／社内）までご連絡ください。'
  );
  // setRequireLogin は Workspace 専用のため未使用（個人Gmailではエラーになる）
  form.setCollectEmail(true);
  form.setLimitOneResponsePerUser(false);

  // --- 基本情報 ---
  form
    .addSectionHeaderItem()
    .setTitle('① サークル基本情報');

  form
    .addTextItem()
    .setTitle('サークル名（正式名称）')
    .setRequired(true);

  form
    .addTextItem()
    .setTitle('拠点となる大学名（複数ある場合は列挙）')
    .setRequired(true);

  form
    .addMultipleChoiceItem()
    .setTitle('インカレサークルですか？')
    .setChoiceValues(['インカレ', 'インカレではない（単一大学）'])
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle('サークル紹介（200〜600字程度）')
    .setHelpText('新歓で見せたい魅力・雰囲気が伝わるように書いてください。')
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle('活動内容（3つ）')
    .setHelpText('見出し1行＋説明2〜4行 × 3つ、の形式で入力してください。')
    .setRequired(true);

  form
    .addTextItem()
    .setTitle('部員・メンバー人数（目安で可）')
    .setRequired(true);

  // --- 画像（LINE アルバムで送付。フォームでは受け付けない）---
  form
    .addSectionHeaderItem()
    .setTitle('② 写真・画像（LINEのアルバムで送付）')
    .setHelpText(
      '【このフォームでは画像ファイルは送れません】\n' +
        'フォーム送信後、担当者とつながっている LINE のトークに、掲載希望の写真をアルバムにまとめて送付してください。\n' +
        '・ヒーロー（トップ）に使いたい写真：1枚（横長の写真がおすすめ）\n' +
        '・活動の様子：3枚程度\n' +
        'アルバム内の並びや、どれをメインにしたいかが分かるよう、トークに一言メッセージも添えてください。'
    );

  form
    .addMultipleChoiceItem()
    .setTitle('写真の送付方法の理解・同意')
    .setChoiceValues([
      '上記のとおり、LINEのアルバム（または写真をまとめた投稿）で担当に送付します',
      'LINE以外の方法を相談したい（備考欄に記載します）',
    ])
    .setRequired(true);

  form
    .addTextItem()
    .setTitle('LINEの表示名（送付時の本人確認用・任意）')
    .setHelpText('トーク上の表示名が本名と違う場合などにご記入ください。')
    .setRequired(false);

  form
    .addParagraphTextItem()
    .setTitle('写真に関する補足・要望（任意）')
    .setHelpText(
      'メインにしたい写真の指定、活動写真の並び順、載せたくない人物、著作権・肖像権の注意事項など。' +
        'LINE以外で送る場合の希望もここに書いてください。'
    )
    .setRequired(false);

  // --- 代表・連絡先 ---
  form
    .addSectionHeaderItem()
    .setTitle('③ 代表者・連絡先（公開ページに載せる可能性があります）');

  form.addTextItem().setTitle('サークル長（または代表）氏名').setRequired(true);

  form.addTextItem().setTitle('代表の所属大学').setRequired(true);

  form.addListItem().setTitle('代表の学年').setChoiceValues(['1年', '2年', '3年', '4年', '修士', '博士', 'その他']).setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle('その他幹部（紹介ページに載せる場合：役職・氏名・大学・学年）')
    .setHelpText('任意。複数いる場合は箇条書きで。')
    .setRequired(false);

  form.addTextItem().setTitle('連絡用 電話番号（任意・ハイフンありで）').setRequired(false);

  form.addTextItem().setTitle('LINE ID または友だち追加用URL').setRequired(false);

  form.addTextItem().setTitle('Instagram アカウント（@から）').setRequired(false);

  form
    .addParagraphTextItem()
    .setTitle('打ち合わせ（納品確認MTG）の希望日程')
    .setHelpText(
      '第3希望まで（例: 4/5(土) 14:00-18:00 など）。代表＋新歓関係の役職の方など2名以上参加できる候補をお願いします。'
    )
    .setRequired(true);

  form
    .addParagraphTextItem()
    .setTitle('その他・要望（デザインの雰囲気、載せたくない情報など）')
    .setRequired(false);

  // --- 同意（各項目を個別に必須にして「すべて同意」を担保）---
  form
    .addCheckboxItem()
    .setTitle('活動費補助の選択肢として「サークルアップ」の紹介を、担当から説明してもよい')
    .setChoiceValues(['同意する'])
    .setRequired(true);

  form
    .addCheckboxItem()
    .setTitle('納品MTGにサークル幹部が参加し、画面確認と必要な訴求の時間を取ってもよい')
    .setChoiceValues(['同意する'])
    .setRequired(true);

  form
    .addCheckboxItem()
    .setTitle('入力内容が紹介ページ作成に利用されることに同意する')
    .setChoiceValues(['同意する'])
    .setRequired(true);

  // 回答先スプレッドシート
  const ss = SpreadsheetApp.create('【回答】' + formTitle);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  const url = form.getPublishedUrl();
  const editUrl = form.getEditUrl();
  const ssUrl = ss.getUrl();

  Logger.log('--- 作成完了 ---');
  Logger.log('回答用URL（これを配布）: ' + url);
  Logger.log('編集用URL（管理者のみ）: ' + editUrl);
  Logger.log('回答スプレッドシート: ' + ssUrl);
}
