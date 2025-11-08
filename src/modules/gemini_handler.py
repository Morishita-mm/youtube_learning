import os
import google.generativeai as genai

def summarize_text(text: str, language: str = "Japanese"):
    """
    与えられたテキストをGemini APIを使って要約する。

    Args:
        text (str): 要約するテキスト。
        language (str): 要約文の言語。

    Returns:
        str: 要約されたテキスト。エラー時はNoneを返す。
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("エラー: 環境変数 GEMINI_API_KEY が設定されていません。")
        return None

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-flash-latest') # または 'gemini-pro'
        
        prompt = f"""以下の文章を{language}で簡潔に要約してください。

---
{text}
---

要約:
"""
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Gemini APIの呼び出し中にエラーが発生しました: {e}")
        return None

if __name__ == '__main__':
    # --- モジュール単体でのテスト ---
    # from dotenv import load_dotenv
    # load_dotenv()
    sample_text = """
    Streamlitは、Pythonだけで対話的なWebアプリケーションを構築できるオープンソースのフレームワークです。
    データサイエンティストや機械学習エンジニアが、複雑なフロントエンドの知識なしに、
    データを可視化したり、モデルのデモを作成したりするのに非常に便利です。
    ウィジェットを追加するだけで、スライダーやボタンなどを簡単に実装できます。
    """
    summary = summarize_text(sample_text)
    if summary:
        print("--- 要約テスト ---")
        print(summary)
    else:
        print("要約の生成に失敗しました。")
