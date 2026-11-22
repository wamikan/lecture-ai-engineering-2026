# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：講座に固有の事柄に関する質問に対して、第1回では用語集を使用せず回答していたため全く的外れな回答をしていたが、今回のエージェントは用語集から検索しているため正しい回答をしていた。
以下、実際の出力。

[model] gemini-3.5-flash-lite
AIE2026の講座における「3レベル」とは、宿題の難易度や取り組み方の構成を指しています。

具体的には以下の3つの段階に分かれており、ご自身の学習状況に合わせて**どれか1つに取り組めば、その回の宿題は完了**となります。

1. **基礎**：講義内容の確認を中心とした問題
2. **実装**：自分で実際にコードを書く問題
3. **発展**：さらに踏み込んだ調査や新しい試みを行う問題

原則として採点などは行われませんので、ご自身のペースや興味に合わせて選んで取り組んでみてください。

関連する回：第1回

---

- `--trace` で見えたツール呼び出し（ツール名と引数）：search_glossary({'query': 'LoRA'})、search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：2。
以下、実際の出力。

[model] gemini-3.5-flash-lite
LoRAとQLoRAの違いは以下の通りです。

* **LoRA（Low-Rank Adaptation）**
  事前学習済みの重みを固定したまま、重みの更新分を2つの小さな行列（低ランク行列）の積で表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習するパラメータ数を大幅に減らすことができます。

* **QLoRA**
  ベースモデルの重みを4ビットなどに**量子化**してメモリを大幅に節約した状態で、その上からLoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPUでも効率よく扱えるようになります。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008338'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=190, requests=2, tool_calls=2)

---

- 追加したツールと、docstring に書いた説明：docstring に書いた説明は無い。追加したツールは以下：

def make_quiz(lecture: int) -> str:
    """指定した回（1始まりの整数）の講義内容から、確認問題を1問作成して返す。
    
    「第X回の確認問題を出して」のように、利用者が理解度を確かめたいときに使う。
    """
    glossary = load_glossary()
    
    # 指定された回の用語を抽出
    lecture_terms = [e for e in glossary if e.get("lecture") == lecture]
    
    # 第0回など、用語が存在しない場合のエラーハンドリング
    if not lecture_terms:
        return f"第{lecture}回の用語は見つかりませんでした。別の回を指定してください。"
    
    # ランダムに1つ選ぶ
    term = random.choice(lecture_terms)
    
    # 問題と答えを辞書にまとめる
    quiz = {
        "question": f"「{term['term']}」の意味は？",
        "answer": term['definition']
    }
    
    return json.dumps(quiz, ensure_ascii=False)

---

## 宿題

- 取り組んだレベル：実装 
- やったこと：
  - app/tools.py に、引数の文字列をテキストファイルとして保存する save_learning_log ツールを作成した。
  - app/agent.py で、Agent の output_type に DeferredToolRequests を追加し、requires_approval=True を指定してツールを登録した。
  - app/agent.py のメインループを改修し、モデルの出力が DeferredToolRequests の場合は while ループで利用者に y/n を求め、その結果を approvals_dict = {call.tool_call_id: True/False} として記録。それを result.output.build_results(approvals=approvals_dict) に渡し、会話履歴と共に再度 run_sync を呼び出す承認フローを実装した。

- 結果：「今日の学習内容『Pydantic AIの承認フローについて学んだ』を保存して」と入力して実行したところ、ターミナル上で処理が一時停止し、「保存を許可しますか？ (y/n):」と正しくプロンプトが表示された。y を入力して承認すると、エラーなく処理が再開され、最終的にモデルから「保存しました！」という完了報告と関係する回（第7回）の回答が得られた。

以下、実際の出力。

uv run python -m app.agent "今 日の学習内容「Pydantic AIの承認フローについて学んだ」を保存して"
[model] gemini-3.5-flash-lite

[確認] 学習記録を保存しようとしています。
保存内容: {'content': '今日の学習内容：Pydantic AIの承認フローについて学んだ'}
保存を許可しますか？ (y/n): y
保存を承認しました。
今日の学習内容「Pydantic AIの承認フローについて学んだ」を学習記録として保存しました！

（関係する回：第7回）

---

- 気づき・疑問：Pydantic AI (v1.x系) における承認フローの実装方法について気づきがあった。承認が下りた際に、開発者が手動で関数（ツール）を実行してその結果をモデルに返すのではなく、「どのツール呼び出しを承認(True)/拒否(False)したか」という辞書を build_results(approvals=...) に渡して処理を再開させれば、フレームワーク側で勝手に関数を実行してくれるという設計思想になっていることが分かった。
