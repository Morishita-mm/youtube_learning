import os
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def search_videos(keyword: str, max_results: int = 10):
    """
    指定されたキーワードでYouTube動画を検索する。
    環境変数 API_BASE_URL が設定されていればモックサーバーに、
    なければ実際のYouTube APIに接続する。

    Args:
        keyword (str): 検索キーワード。
        max_results (int): 最大取得件数。

    Returns:
        list: 動画情報の辞書を含むリスト。
              例: [{'video_id': '...', 'title': '...', 'thumbnail_url': '...'}]
              エラー時は空のリストを返す。
    """
    api_base_url = os.getenv("API_BASE_URL")

    if api_base_url:
        # --- 開発モード: モックサーバーに接続 ---
        try:
            response = requests.get(f"{api_base_url}/youtube/search", params={"q": keyword})
            response.raise_for_status()  # HTTPエラーがあれば例外を発生
            search_result = response.json().get("items", [])
            
            # データを統一形式に整形
            videos = [
                {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["default"]["url"],
                }
                for item in search_result
            ]
            return videos
        except requests.exceptions.RequestException as e:
            print(f"モックサーバーへの接続に失敗しました: {e}")
            return []

    else:
        # --- 本番モード: YouTube Data APIに接続 ---
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if not youtube_api_key:
            print("エラー: 環境変数 YOUTUBE_API_KEY が設定されていません。")
            return []

        try:
            youtube = build("youtube", "v3", developerKey=youtube_api_key)
            search_response = (
                youtube.search()
                .list(q=keyword, part="snippet", maxResults=max_results, type="video")
                .execute()
            )
            search_result = search_response.get("items", [])

            # データを統一形式に整形
            videos = [
                {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["default"]["url"],
                }
                for item in search_result
            ]
            return videos
        except HttpError as e:
            print(f"YouTube APIの呼び出し中にエラーが発生しました: {e}")
            return []
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            return []

if __name__ == '__main__':
    # --- モジュール単体でのテスト ---
    print("--- 開発モード（モックサーバー）でのテスト ---")
    os.environ['API_BASE_URL'] = 'http://localhost:5001'
    mock_videos = search_videos("test keyword")
    if mock_videos:
        print(f"{len(mock_videos)}件の動画を取得しました。")
        print(mock_videos[0])
    
    print("\n--- 本番モード（YouTube API）でのテスト ---")
    # .envファイルからAPIキーを読み込むためにdotenvが必要
    # from dotenv import load_dotenv
    # load_dotenv()
    del os.environ['API_BASE_URL']
    real_videos = search_videos("Python programming")
    if real_videos:
        print(f"{len(real_videos)}件の動画を取得しました。")
        print(real_videos[0])
    else:
        print("動画を取得できませんでした。YOUTUBE_API_KEYが正しく設定されているか確認してください。")

