from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# モックデータが格納されているディレクトリのパス
MOCK_DATA_DIR = os.path.join(os.path.dirname(__file__), 'mock_data')

def load_mock_data(filename):
    """指定されたファイルからJSONモックデータを読み込む"""
    with open(os.path.join(MOCK_DATA_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/youtube/search', methods=['GET'])
def mock_youtube_search():
    """YouTubeの検索結果のモックを返す"""
    data = load_mock_data('mock_youtube_search.json')
    return jsonify(data)

@app.route('/gemini/summarize', methods=['POST'])
def mock_gemini_summarize():
    """Geminiの要約結果のモックを返す"""
    data = load_mock_data('mock_gemini_summary.json')
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
