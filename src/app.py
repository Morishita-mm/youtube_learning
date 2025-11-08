import streamlit as st
from modules.youtube_handler import search_videos, get_transcript_text
from modules.gemini_handler import summarize_text
import re

# ページのレイアウトをワイドモードに設定し、画面幅全体に表示領域を広げる
st.set_page_config(layout="wide")

# アプリケーションのタイトル
st.title("YouTube動画学習アシスタント")

# --- セッションデータの初期化 ---
if 'learning_data' not in st.session_state:
    st.session_state.learning_data = {} # {video_id: {"summary": str, "memo": str}}
if 'current_video_id' not in st.session_state:
    st.session_state.current_video_id = None
if 'current_video_title' not in st.session_state:
    st.session_state.current_video_title = ""
if 'search_executed' not in st.session_state:
    st.session_state.search_executed = False
if 'active_videos' not in st.session_state:
    st.session_state.active_videos = [] # List of video dicts: {'video_id', 'title', 'thumbnail_url'}

# --- コールバック関数 ---
def sync_memo():
    """text_areaウィジェットの変更を現在の動画のメモとしてセッションに同期する"""
    if st.session_state.current_video_id and "memo_widget" in st.session_state:
        video_id = st.session_state.current_video_id
        if video_id in st.session_state.learning_data:
            st.session_state.learning_data[video_id]["memo"] = st.session_state.memo_widget

# --- サイドバー ---
st.sidebar.title("動画検索")
search_keyword = st.sidebar.text_input("検索キーワードを入力")
search_button = st.sidebar.button("検索", use_container_width=True)

if search_button:
    st.session_state.search_executed = True
    st.session_state.search_keyword = search_keyword
    with st.spinner("検索中..."):
        st.session_state.search_results = search_videos(search_keyword)
    st.session_state.current_video_id = None

# 検索結果の表示
if st.session_state.search_executed:
    st.sidebar.info(f"「`{st.session_state.get('search_keyword', '')}`」の検索結果:")
    search_results = st.session_state.get('search_results', [])
    if search_results:
        for video in search_results:
            st.sidebar.image(video["thumbnail_url"], use_container_width=True)

            if st.sidebar.button(video["title"], key=video["video_id"], use_container_width=True):
                st.session_state.current_video_id = video["video_id"]
                st.session_state.current_video_title = video["title"]
                if video["video_id"] not in st.session_state.learning_data:
                    st.session_state.learning_data[video["video_id"]] = {"summary": "", "memo": ""}
                st.session_state.memo_widget = st.session_state.learning_data[video["video_id"]]["memo"]
                st.rerun()
            st.sidebar.divider()
    else:
        st.sidebar.info("検索結果がありません。")

# --- メインエリア ---
st.header("学習エリア")

video_id = st.session_state.get('current_video_id')

if video_id:
    current_data = st.session_state.learning_data.get(video_id, {"summary": "", "memo": ""})
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"選択中の動画: {st.session_state.current_video_title}")
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        st.subheader("AIによる要約")
        if st.button("この動画を要約する"):
            with st.spinner("要約を生成中..."):
                transcript = get_transcript_text(video_id)
                if transcript:
                    summary = summarize_text(transcript)
                    if summary:
                        st.session_state.learning_data[video_id]["summary"] = summary
                    else:
                        st.error("要約の生成に失敗しました。")
                else:
                    st.error("この動画の字幕（トランスクリプト）を取得できませんでした。")
        
        if current_data.get("summary"):
            st.markdown("""
                <style>
                    .summary-scrollable-area {
                        max-height: 350px; /* メモ欄と同じ高さに設定 */
                        overflow-y: scroll;
                        border: 1px solid rgba(49, 51, 63, 0.2); /* Streamlitのデフォルトボーダーに合わせる */
                        border-radius: 0.25rem; /* Streamlitのデフォルトの角丸に合わせる */
                        padding: 1rem; /* Streamlitのデフォルトのパディングに合わせる */
                    }
                </style>
            """, unsafe_allow_html=True)
            # st.containerで囲み、その中にスクロール可能なdivを配置
            with st.container():
                st.markdown(f'<div class="summary-scrollable-area">{current_data["summary"]}</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("メモ")
        preview_mode = st.toggle("プレビューモード", key="preview_mode")
        
        if 'preview_mode' in st.session_state and not st.session_state.preview_mode:
             if video_id in st.session_state.learning_data:
                st.session_state.memo_widget = st.session_state.learning_data[video_id]["memo"]

        if preview_mode:
            with st.container(border=True):
                st.markdown(current_data.get("memo", ""))
        else:
            st.text_area(
                "動画を視聴しながらメモを取る",
                height=350,
                key="memo_widget",
                on_change=sync_memo,
                label_visibility="collapsed"
            )

        video_title = st.session_state.get("current_video_title", "Untitled")
        safe_title = re.sub(r'[\\/*?:"<>|]', "-", video_title)
        memo_data = current_data.get("memo", "")
        st.download_button(
            label="メモをダウンロード",
            data=memo_data,
            file_name=f"{safe_title}_memo.md",
            mime="text/markdown",
        )
else:
    st.info("サイドバーから学習したい動画を検索・選択してください。")