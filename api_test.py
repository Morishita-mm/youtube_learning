import os
import google.generativeai as genai
from googleapiclient.discovery import build
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーを環境変数から取得
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def test_youtube_api():
    """YouTube Data API v3への接続をテストする"""
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY":
        print("YouTube APIキーが設定されていません。")
        return

    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q="Python programming",
            part="snippet",
            maxResults=5
        ).execute()
        
        print("--- YouTube API 接続テスト ---")
        print("正常に動画を検索できました。")
        for item in search_response.get("items", []):
            print(f"- {item['snippet']['title']}")
        print("-" * 20)

    except Exception as e:
        print(f"YouTube API 接続中にエラーが発生しました: {e}")

def test_gemini_api():
    """Gemini APIへの接続をテストする"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("Gemini APIキーが設定されていません。")
        return

    try:
        genai.configure(api_key=GEMINI_API_KEY)

        print("--- 利用可能なGeminiモデルのリスト ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        print("-" * 20)

        # 推奨モデル 'gemini-flash-latest' を使用
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("こんにちは、Gemini。接続テストです。")
        
        print("--- Gemini API 接続テスト ---")
        print("正常に応答を取得できました。")
        print(f"応答: {response.text[:80]}...")
        print("-" * 20)

    except Exception as e:
        print(f"Gemini API 接続中にエラーが発生しました: {e}")

if __name__ == "__main__":
    print("API接続テストを開始します...")
    test_youtube_api()
    test_gemini_api()
    print("テストが完了しました。")
