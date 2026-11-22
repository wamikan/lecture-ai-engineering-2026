"""第1回: 素のLLMに質問し、会話履歴を保持しながら対話するスクリプト。"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"

def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する（会話履歴保持）")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    
    try:
        # クライアントの初期化
        client = genai.Client(api_key=get_api_key())
        
        # 宿題(実装レベル): 会話履歴を保持するため、Chatセッションを作成
        chat = client.chats.create(model=MODEL)
        
        current_question = args.question

        while True:
            if current_question:
                print(f"[質問] {current_question}")
                
                # generate_content の代わりに send_message を使用して履歴をスタック
                response = chat.send_message(current_question)
                
                # 第1回 演習: トークン数の表示
                if response.usage_metadata:
                    in_tokens = response.usage_metadata.prompt_token_count
                    out_tokens = response.usage_metadata.candidates_token_count
                    print(f"（トークン数 - 入力: {in_tokens} / 出力: {out_tokens}）")

                print(f"{response.text}\n")
                    
            # 対話ループ: 標準入力から次の質問を受け取る
            current_question = input("次の質問を入力 (終了するには 'exit' を入力): ")
            
            # 終了条件
            if current_question.strip().lower() in ['exit', 'quit']:
                print("終了します。")
                break
            
            # 空入力の場合は再度入力を促す
            if not current_question.strip():
                current_question = None

    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)
    except (KeyboardInterrupt, EOFError):
        print("\n終了します。")
        raise SystemExit(0)

if __name__ == "__main__":
    main()
    


# """第1回: 素のLLMに1回だけ質問するスクリプト。

# 使い方:
#     uv run python -m app.ask "LoRAとは何ですか？"
#     uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

# ツールも会話履歴も持たない「素の」呼び出し。
# 講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
# （講座の実際とは違う）ことを確かめよう。
# （第3回で、用語集を検索できるエージェントにして改善する）
# """

# import argparse

# from google import genai
# from google.genai import errors

# from app.config import MODEL, api_error_message, get_api_key

# # 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
# DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


# def ask(question: str) -> str:
#     client = genai.Client(api_key=get_api_key())
#     response = client.models.generate_content(model=MODEL, contents=question)

#     # TODO(第1回 演習): response.usage_metadata から
#     #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）

#     return response.text


# def main() -> None:
#     parser = argparse.ArgumentParser(description="素のLLMに質問する")
#     parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
#     args = parser.parse_args()

#     print(f"[model] {MODEL}")
#     print(f"[質問] {args.question}\n")
#     try:
#         print(ask(args.question))
#     except errors.APIError as e:
#         print(api_error_message(e.code, e.message))
#         raise SystemExit(1)


# if __name__ == "__main__":
#     main()
