import streamlit as st
from modules.youtube_handler import search_videos, get_transcript_text
from modules.gemini_handler import summarize_text

# ページのレイアウトをワイドモードに設定し、画面幅全体に表示領域を広げる
st.set_page_config(layout="wide")

# アプリケーションのタイトル
st.title("YouTube動画学習アシスタント")

# --- サイドバー ---
st.sidebar.title("動画検索")
search_keyword = st.sidebar.text_input("検索キーワードを入力")
search_button = st.sidebar.button("検索")

# 検索ボタンが押されたら、その状態をセッションに保存
if search_button:
    st.session_state.search_executed = True
    st.session_state.search_keyword = search_keyword
    # APIを呼び出して結果をセッションに保存
    with st.spinner("検索中..."):
        st.session_state.search_results = search_videos(search_keyword)
    
    # 新しい検索が始まったら、選択された動画とメモ、要約をリセット
    if 'selected_video' in st.session_state:
        del st.session_state['selected_video']
        del st.session_state['selected_video_title']
    if 'memo_input' in st.session_state:
        del st.session_state['memo_input']
    if 'summary' in st.session_state:
        del st.session_state['summary']


# 検索が実行された後であれば、検索結果を表示
if 'search_executed' in st.session_state and st.session_state.search_executed:
    st.sidebar.write(f"「{st.session_state.search_keyword}」の検索結果:")
    
    search_results = st.session_state.get('search_results', [])
    if search_results:
        for video in search_results:
            st.sidebar.image(video["thumbnail_url"], width=120)
            if st.sidebar.button(video["title"], key=video["video_id"]):
                st.session_state['selected_video'] = video["video_id"]
                st.session_state['selected_video_title'] = video["title"]
                # メモ入力と要約をリセット
                st.session_state.memo_input = ""
                st.session_state.summary = ""
                # メインエリアを更新するために再実行
                st.rerun()
    else:
        st.sidebar.info("検索結果がありません。")


# --- メインエリア ---
st.header("学習エリア")

if 'selected_video' in st.session_state:
    # 画面を2つの列に分割
    col1, col2 = st.columns(2)

    with col1:
        # --- 動画再生 ---
        st.subheader(f"選択中の動画: {st.session_state['selected_video_title']}")
        video_id = st.session_state['selected_video']
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        # --- AI要約 ---
        st.subheader("AIによる要約")
        
        # 要約のセッション状態を初期化
        if 'summary' not in st.session_state:
            st.session_state.summary = ""

        if st.button("この動画を要約する"):
            with st.spinner("要約を生成中..."):
                transcript = get_transcript_text(video_id)
                if transcript:
                    summary = summarize_text(transcript)
                    if summary:
                        st.session_state.summary = summary
                    else:
                        st.error("要約の生成に失敗しました。")
                else:
                    st.error("この動画の字幕（トランスクリプト）を取得できませんでした。")

        # 要約が生成されていれば、編集不可で表示
        if st.session_state.summary:
            st.markdown(
                st.session_state.summary,
                unsafe_allow_html=True
            )

    with col2:
        # --- メモ機能 ---
        st.subheader("メモ")
        
        # st.text_areaのkeyに対応するセッション変数を安全に初期化
        if 'memo_input' not in st.session_state:
            st.session_state.memo_input = ""
            
        st.text_area("動画を視聴しながらメモを取る", height=350, key="memo_input")
        
        if st.button("メモを保存"):
            # TODO: メモ保存処理を実装 (st.session_state.memo_input を使う)
            st.success("メモを保存しました。")

else:
    st.info("サイドバーから学習したい動画を検索・選択してください。")
