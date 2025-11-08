# YouTube動画学習アシスタント

## 概要

このアプリケーションは、StreamlitとGoogle Gemini API、YouTube Data APIを組み合わせて開発された、YouTube動画の学習を効率化するためのアシスタントです。ユーザーはYouTube動画のURLを入力するだけで、動画を視聴しながらメモを取り、AIによる自動要約を生成することができます。動画ごとにメモと要約が保存されるため、複数の動画を並行して学習する際にも便利です。

## 機能

*   **YouTube動画URLからの読み込み**: YouTube動画のURLを入力するだけで、動画をアプリケーション内に読み込みます。
*   **動画再生**: アプリケーション内でYouTube動画を直接再生できます。
*   **AIによる動画要約**: 読み込んだ動画のトランスクリプト（字幕）を基に、Google Gemini APIが動画内容を自動で要約します。要約結果は編集不可で表示されます。
*   **動画ごとのメモ**: 動画を視聴しながらMarkdown形式でメモを取ることができます。メモは動画ごとに自動で保存され、別の動画に切り替えても内容が失われることはありません。
*   **メモのプレビュー**: 記入中のメモをリアルタイムでMarkdown形式でプレビューできます。
*   **メモのダウンロード**: 作成したメモはMarkdownファイルとしてローカルにダウンロードできます。

## スクリーンショット

![アプリケーションのスクリーンショット](/UI_sample/screenshot.png)
*サイドバーに動画検索と作業中動画リスト、メインエリアに動画再生、AI要約、メモ機能が表示されます。*

## 技術スタック

*   **フレームワーク**: Streamlit
*   **言語**: Python
*   **動画API**: YouTube Data API v3
*   **AI / LLM**: Google Gemini API
*   **字幕取得**: youtube-transcript-api

## セットアップ (ローカル環境)

1.  **リポジトリのクローン**:
    ```bash
    git clone https://github.com/Morishita-mm/youtube_learning.git
    cd youtube_learning
    ```

2.  **`.env`ファイルの作成**:
    `youtube_learning`ディレクトリの直下に`.env`ファイルを作成し、以下の内容を記述します。`YOUR_YOUTUBE_API_KEY`と`YOUR_GEMINI_API_KEY`は、それぞれGoogle Cloud Platformで取得したAPIキーに置き換えてください。
    ```
    YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY"
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    *   YouTube Data API v3の有効化が必要です。
    *   Generative Language API (または Vertex AI API / Gemini API) の有効化が必要です。

3.  **Docker Composeで起動**:
    ```bash
    docker-compose up --build -d
    ```
    これにより、必要なPythonライブラリがインストールされ、アプリケーションがコンテナ内で起動します。

4.  **アプリケーションへのアクセス**:
    ブラウザで `http://localhost:8501` にアクセスしてください。

## 使用方法

1.  **動画の読み込み**: サイドバーの「YouTube動画URLを入力」欄にYouTube動画のURLを入力し、「動画を読み込む」ボタンをクリックします。
2.  **動画の選択**: 読み込み結果に表示された動画のタイトルをクリックすると、メインエリアに動画が表示されます。
3.  **AI要約の生成**: 「この動画を要約する」ボタンをクリックすると、AIが動画の要約を生成します。
4.  **メモの記入**: メモ欄に自由にメモを記入できます。
5.  **メモのプレビュー**: 「プレビューモード」のトグルをオンにすると、記入したメモのMarkdownプレビューが表示されます。
6.  **動画の切り替え**: サイドバーの別の動画を選択して作業を切り替えることができます。メモや要約は動画ごとに自動で保存・復元されます。
7.  **メモのダウンロード**: 「メモをダウンロード」ボタンをクリックすると、現在のメモ内容がMarkdownファイルとしてダウンロードされます。

## デプロイ (Streamlit Community Cloud)

このアプリケーションはStreamlit Community Cloudにデプロイ可能です。

1.  GitHubリポジトリにコードをプッシュします。
2.  Streamlit Community Cloudにログインし、「New app」からリポジトリ、ブランチ、`src/app.py`のパスを指定します。
3.  「Secrets」に`YOUTUBE_API_KEY`と`GEMINI_API_KEY`を設定します。

## 今後の展望

*   メモの保存先オプションの追加（ローカルファイル以外にクラウドストレージなど）
*   複数動画の一括管理機能の強化
*   ユーザー認証機能の導入
*   要約の言語選択機能
