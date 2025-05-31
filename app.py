"""
A sample Hello World server.
"""
import logging
import os
from playwright.sync_api import sync_playwright
from flask import Flask, jsonify, render_template

# pylint: disable=C0103
app = Flask(__name__)
app.json.ensure_ascii = False  # 日本語を含む文字列をそのまま出力するため


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!, marzg!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

@app.route('/exec', methods=['GET'])
def exec_playwright():
    # playwrightの実装
    try:
        with sync_playwright() as p:
            # Chromium (Web Browser)のインスタンスを作成する
            browser = p.chromium.launch(headless=True)

            # 新しいページを作成する
            page = browser.new_page()
            logging.info('page: %s', page)
            print('page: ', page)

            # page.goto() で Yahoo のサイトにアクセス
            page.goto('https://www.yahoo.co.jp/')

            # title tag の値（ページタイトル）を取得し辞書に格納
            title_top = page.title()

            # yahoo shopping のページに遷移
            page.locator("#Masthead").get_by_role("link", name="ショッピングへ遷移する").click()
            page.wait_for_load_state()  # ページ遷移後のロード完了を待機
            title_shopping = page.title()

            # Browser を閉じる
            browser.close()

        return {
            'top':{
                'title': title_top
            },
            'shopping':{
                'title': title_shopping
            }
        }, 200
    except Exception as e:
        return {'message': str(e)}, 500

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
