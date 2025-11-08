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
        
        prompt = f"""あなたはYouTube動画の学習を助けるアシスタントです。
以下の動画のトランスクリプトを読み、動画の内容を過不足なく理解し、学習者が動画を見ながら内容を把握しやすいように、**主要なセクションに分け、それぞれのセクションにタイトルを付け、時系列順に箇条書きで要約してください。**

要約は以下の点に注意して作成してください。
- 動画の主要なトピック、重要な概念、結論を網羅すること。
- 各セクションは動画の進行に沿って構成し、セクション内も時系列順に箇条書きで記述すること。
- 各箇条書きは簡潔かつ具体的に記述すること。
- 出力は{language}で行うこと。
- セクションタイトルはMarkdownのヘッダー（例: `## セクションタイトル`）を使用し、箇条書きはハイフン（`-`）を使用すること。

---
{text}
---
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
