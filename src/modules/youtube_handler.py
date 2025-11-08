import os
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

def get_transcript_text(video_id: str):
    """
    指定されたYouTube動画のトランスクリプト（字幕）を取得し、全文を結合して返す。
    youtube-transcript-apiライブラリを使用する。

    Args:
        video_id (str): YouTube動画のID。

    Returns:
        str: 取得したトランスクリプトの全文。取得できない場合はNoneを返す。
    """
    try:
        ytt = YouTubeTranscriptApi()
        langs = ['ja', 'ja-JP', 'en']
        try:
            transcript_list = ytt.fetch(video_id, languages=['ja','ja-JP','en'])
            data = transcript_list.to_raw_data()
        except NoTranscriptFound:
            tlist = ytt.list(video_id)
            data = tlist.find_generated_transcript(langs).fetch().to_raw_data()
        full_transcript = " ".join([item['text'] for item in data])
        return full_transcript

    except TranscriptsDisabled:
        print(f"動画ID {video_id}: 字幕が無効になっています。")
        return None
    except NoTranscriptFound:
        print(f"動画ID {video_id}: 日本語または英語の字幕が見つかりませんでした。")
        return None
    except Exception as e:
        print(f"トランスクリプトの取得中に予期せぬエラーが発生しました: {e}")
        return None

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
            # コンテナ間通信のため、localhostをサービス名に置換
            api_base_url = api_base_url.replace("localhost", "mock-server")
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
                    "thumbnail_url": item["snippet"]["thumbnails"]["medium"]["url"],
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
    print("--- get_transcript_text テスト ---")
    # 字幕があることが分かっている動画IDでテスト
    test_video_id = "H3KnMyojEQU"
    transcript = get_transcript_text(test_video_id)
    if transcript:
        print(f"動画ID {test_video_id} のトランスクリプトを取得しました。")
        print(transcript[:200] + "...")
    else:
        print(f"動画ID {test_video_id} のトランスクリプトを取得できませんでした。")

    print("\n--- search_videos 開発モード（モックサーバー）でのテスト ---")
    os.environ['API_BASE_URL'] = 'http://localhost:5001'
    mock_videos = search_videos("test keyword")
    if mock_videos:
        print(f"{len(mock_videos)}件の動画を取得しました。")
        print(mock_videos[0])
    
    print("\n--- search_videos 本番モード（YouTube API）でのテスト ---")
    # .envファイルからAPIキーを読み込むためにdotenvが必要
    # from dotenv import load_dotenv
    # load_dotenv()
    if 'API_BASE_URL' in os.environ:
        del os.environ['API_BASE_URL']
    real_videos = search_videos("Python programming")
    if real_videos:
        print(f"{len(real_videos)}件の動画を取得しました。")
        print(real_videos[0])
    else:
        print("動画を取得できませんでした。YOUTUBE_API_KEYが正しく設定されているか確認してください。")
