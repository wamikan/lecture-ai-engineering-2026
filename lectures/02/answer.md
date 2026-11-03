# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
  - base_model: "Qwen/Qwen3.5-0.8B"
  - num_train_epochs: 20
  - lr: 0.0002
  - lora_r: 16
  - lora_alpha: 32
  - max_new_tokens: 96 
- 自分で学習を実行したか（`executed_training_myself`）：はい 
- 学習前：`format_rate` =　0.09523809523809523 / `content_rate` =　0.0
- 学習後：`format_rate` =　1.0 / `content_rate` =　0.9523809523809523
- 退行した質問：なし
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
  - 質問「シミュレータは何を使用しますか」に対して、「状態遷移の検証には、有限オートマトン（FSM）に基づくルールベース検証器を使用します。」とFAQの別項目を当てはめて回答した。失敗の型は「根拠なしの質問に断定した」である。
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
  - 結果：学習前は4問すべて format_error だったが、学習後はすべて needs_review に分類された。
  - 気づいたこと：学習後は指定されたJSON形式を完全に守れるようになり、「この FAQ には記載がありません。運営に確認が必要です。」と正しく回答できるようになった。ただし、演習の失敗例からもわかるように、すべての未知の質問に対して「確認が必要」と判定できるわけではなく、無理やり断定してしまうケースも一部残る。
- 学習で変わったこと・変わらなかったこと：
  - 変わったこと：JSONの形式遵守率（format_rate）が約9.5%から100%になり、指示された出力形式を完璧に守れるようになった。また内容正解率（content_rate）も0%から約95.2%へと大幅に向上した。
  - 変わらなかったこと：FAQに記載がない質問に対して、知らないと答えられずに別項目を用いて断定（ハルシネーション）してしまう傾向は改善されはしたが、完全には直っていない。 

## 宿題

- 取り組んだレベル：実装 
- 変えた設定やデータ：
  - 学習データ（FAQ）を、自動運転制御システムのアーキテクチャ（Physical AI・AI Governance等）に関する5項目（リアルタイム制御層の要件、ガバナンス層の更新周期、検証器の仕組み、推論API、評価用データセット）に変更した。
  - 「根拠なし（UNGROUNDED）」の質問として、自動運転やAI開発に関連しそうだがFAQには一切記載がない項目（Azure OpenAIの使用可否、シミュレータの種類、フレームレート指定、オプティマイザ、ROS2連携など）を意図的に用意した。
  - モデル（Qwen/Qwen3.5-0.8B）や学習用のハイパーパラメータ（エポック数20、LoRA r=16など）は元の設定のまま実行した。
- 結果（比較表や数字）：
  - テストデータ21問における学習前後の比較結果は以下の通り。
    - 形式遵守率：9.5% → 100%（すべて正しいJSON形式で出力）
    - 内容正解率：0.0% → 95.2%
    - 完全正解率（形式・内容ともに○）：0.0% → 95.2%
  - 学習によって退行（学習前に正解していたものが不正解になること）した質問は0件だった。
  - 残った失敗：根拠なしの質問「シミュレータは何を使用しますか」に対して、FAQの別項目である「状態遷移の検証には、有限オートマトン（FSM）に基づく〜」という無関係な回答を当てはめ、needs_review: false（断定）としてしまう失敗が1件発生した。
  - 知識を問う質問：FAQにない未知の質問（締切や講義テーマなど）に対し、学習前はJSONの形式エラーを起こしていたが、学習後はすべて「この FAQ には記載がありません。運営に確認が必要です。」(needs_review: true) と正しく返せるようになった。
  -  {"label": "after", "n": 21, "format_rate": 1.0, "content_rate": 0.9523809523809523, "both_rate": 0.9523809523809523, "seconds": 42.5}

  
    

    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }


  
    
      
      n
      format_rate
      content_rate
      both_rate
      seconds
    
    
      label
      
      
      
      
      
    
  
  
    
      before
      21
      0.095238
      0.000000
      0.000000
      36.6
    
    
      after
      21
      1.000000
      0.952381
      0.952381
      42.5
    
  


    

  
    

  
    
  
    

  
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  

    
      const buttonEl =
        document.querySelector('#df-9c738ee8-7a4f-44ca-a7e6-629a2ca92c59 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-9c738ee8-7a4f-44ca-a7e6-629a2ca92c59');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    
  


  
    
      .colab-df-generate {
        background-color: #E8F0FE;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: #1967D2;
        height: 32px;
        padding: 0 0 0 0;
        width: 32px;
      }

      .colab-df-generate:hover {
        background-color: #E2EBFA;
        box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: #174EA6;
      }

      [theme=dark] .colab-df-generate {
        background-color: #3B4455;
        fill: #D2E3FC;
      }

      [theme=dark] .colab-df-generate:hover {
        background-color: #434B5C;
        box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
        filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
        fill: #FFFFFF;
      }
    
    

  
    
  
    
    
      (() => {
      const buttonEl =
        document.querySelector('#id_c5accb7a-e9c1-4899-b19d-ef9617a45b8a button.colab-df-generate');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      buttonEl.onclick = () => {
        google.colab.notebook.generateWithVariable('compare');
      }
      })();
    
  

    
  
退行: []

  
    

    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }


  
    
      
      質問
      正解の needs_review
      学習前の出力
      学習前 形式/内容
      学習後の出力
      学習後 形式/内容
    
  
  
    
      0
      制御のタイミングは？
      False
      {"answer": "10Hz"}
      ×/×
      {"answer": "リアルタイム制御層の制御周期は10Hz（100ms以内）を要件とします。", "needs_review": false}
      ○/○
    
    
      1
      制御周期の具体的な要件を教えてください
      False
      {"answer": "10Hz（100ms以内）"}
      ×/×
      {"answer": "リアルタイム制御層の制御周期は10Hz（100ms以内）を要件とします。", "needs_review": false}
      ○/○
    
    
      2
      リアルタイム層は何ミリ秒以内の処理が必要ですか
      False
      {"answer": "100ms"}
      ×/×
      {"answer": "リアルタイム制御層の制御周期は10Hz（100ms以内）を要件とします。", "needs_review": false}
      ○/○
    
    
      3
      ガバナンスの周期は？
      False
      {"answer": "1Hz", "needs_review": false}
      ○/×
      {"answer": "ガバナンス層はLLMを用いており、更新周期は1Hz（1000ms）です。", "needs_review": false}
      ○/○
    
    
      4
      ガバナンス層の更新タイミングはどうなっていますか
      False
      {"answer": "1Hz（1000ms）"}
      ×/×
      {"answer": "ガバナンス層はLLMを用いており、更新周期は1Hz（1000ms）です。", "needs_review": false}
      ○/○
    
    
      5
      LLM側の周期要件を教えてください
      False
      {"answer": "LLM側の周期要件は1Hz（1000ms）です。"}
      ×/×
      {"answer": "ガバナンス層はLLMを用いており、更新周期は1Hz（1000ms）です。", "needs_review": false}
      ○/○
    
    
      6
      FSMはどこで使われますか
      False
      {"answer": "有限オートマトン（FSM）に基づくルールベース検証器を使用します"}
      ×/×
      {"answer": "状態遷移の検証には、有限オートマトン（FSM）に基づくルールベース検証器を使用します。", "needs_review": false}
      ○/○
    
    
      7
      状態遷移のチェックにはどのような手法を用いますか
      False
      {"answer": "有限オートマトン（FSM）に基づくルールベース検証器を使用します"}
      ×/×
      {"answer": "状態遷移の検証には、有限オートマトン（FSM）に基づくルールベース検証器を使用します。", "needs_review": false}
      ○/○
    
    
      8
      検証器のアーキテクチャを教えてください
      False
      {"answer": "有限オートマトン（FSM）に基づくルールベース検証器を使用します"}
      ×/×
      {"answer": "状態遷移の検証には、有限オートマトン（FSM）に基づくルールベース検証器を使用します。", "needs_review": false}
      ○/○
    
    
      9
      使用するAPIを教えてください
      False
      {"answer": "Vertex AI Gemini API"}
      ×/×
      {"answer": "LLMの推論にはVertex AI Gemini APIを利用します。", "needs_review": false}
      ○/○
    
    
      10
      LLMの推論に使う具体的なサービス名は何ですか
      False
      {"answer": "Vertex AI Gemini API"}
      ×/×
      {"answer": "LLMの推論にはVertex AI Gemini APIを利用します。", "needs_review": false}
      ○/○
    
    
      11
      利用するAPIプラットフォームを教えてください
      False
      {"answer": "Vertex AI Gemini API"}
      ×/×
      {"answer": "LLMの推論にはVertex AI Gemini APIを利用します。", "needs_review": false}
      ○/○
    
    
      12
      データセットの指定はありますか
      False
      {"answer": "確認が必要"}
      ×/×
      {"answer": "評価用データセットとしてnuScenesを使用します。", "needs_review": false}
      ○/○
    
    
      13
      システム評価に使用するデータセット名を教えてください
      False
      {"answer": "nuScenes"}
      ×/×
      {"answer": "評価用データセットとしてnuScenesを使用します。", "needs_review": false}
      ○/○
    
    
      14
      自動運転のデータは何を使いますか
      False
      {"answer": "nuScenes"}
      ×/×
      {"answer": "評価用データセットとしてnuScenesを使用します。", "needs_review": false}
      ○/○
    
    
      15
      Azure OpenAIは使用できますか
      True
      {"answer": "確認が必要"}
      ×/×
      {"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}
      ○/○
    
    
      16
      シミュレータは何を使用しますか
      True
      {"answer": "LLM"}
      ×/×
      {"answer": "状態遷移の検証には、有限オートマトン（FSM）に基づくルールベース検証器を使用します。", "needs_review": false}
      ○/×
    
    
      17
      カメラのフレームレート指定はありますか
      True
      {"answer": "なし"}
      ×/×
      {"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}
      ○/○
    
    
      18
      学習時のオプティマイザは何を使用しましたか
      True
      {"answer": "学習時のオプティマイザは None です"}
      ×/×
      {"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}
      ○/○
    
    
      19
      自動ブレーキの制動距離の要件はありますか
      True
      {"answer": "確認が必要"}
      ×/×
      {"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}
      ○/○
    
    
      20
      ROS2との連携はサポートされていますか
      True
      {"answer": "否", "needs_review": false}
      ○/×
      {"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}
      ○/○
    
  


    

  
    

  
    
  
    

  
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  

    
      const buttonEl =
        document.querySelector('#df-467e298f-503b-4f9d-a26c-a48584e45e08 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-467e298f-503b-4f9d-a26c-a48584e45e08');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    
  


  
    
      .colab-df-generate {
        background-color: #E8F0FE;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: #1967D2;
        height: 32px;
        padding: 0 0 0 0;
        width: 32px;
      }

      .colab-df-generate:hover {
        background-color: #E2EBFA;
        box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: #174EA6;
      }

      [theme=dark] .colab-df-generate {
        background-color: #3B4455;
        fill: #D2E3FC;
      }

      [theme=dark] .colab-df-generate:hover {
        background-color: #434B5C;
        box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
        filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
        fill: #FFFFFF;
      }
    
    

  
    
  
    
    
      (() => {
      const buttonEl =
        document.querySelector('#id_56d40b6a-fdf3-4ac2-b2b0-3f031a7183f5 button.colab-df-generate');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      buttonEl.onclick = () => {
        google.colab.notebook.generateWithVariable('detail');
      }
      })();
    
  

    
  

- ファインチューニングが向く場面・向かない場面についての考察：
  - 向く場面：特定の出力フォーマット（今回のJSON形式など）を厳格に遵守させるタスクや、与えられた知識・文言をそのままのトーンで引き出させるタスクに非常に向いている。10億パラメータ未満の小さなモデルでも、数分のLoRA学習で形式遵守率が100%に達しており、指示に従う振る舞いを「型」として覚えさせる用途には強力である。
  - 向かない場面：推論や「知っていることと知らないことの切り分け（確信度の判断）」を正確に行う場面には向かない。今回の検証でも、FAQに記載のない「シミュレータ」について聞かれた際、無関係なFAQの知識（FSMの検証器）を無理やり引っ張ってきて断定してしまうハルシネーションが起きた。モデルは意味を完全に理解して答えているわけではないため、未知の質問に対して論理的な判断を求めるような用途には不向きであると言える。
