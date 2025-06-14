"""
A sample Google Crawler.
"""
import logging
import os
from playwright.sync_api import sync_playwright
import json
import random
import sys
import time

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 3000)
FAIL_RATE = os.getenv("FAIL_RATE", 0)

# Define main script
def main(sleep_ms=3000):
    print(f"Starting Google Crawling Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")

    exec_playwright(sleep_ms)

    print(f"Completed Task #{TASK_INDEX}.")

def exec_playwright(sleep_ms):
    # playwrightの実装
    try:
        with sync_playwright() as p:
            # Chromium (Web Browser)のインスタンスを作成する
            browser = p.chromium.launch(headless=True)

            # 新しいページを作成する
            page = browser.new_page()
            logging.info('page: %s', page)

            # page.goto() で Yahoo のサイトにアクセス
            print('Going to top page...')
            page.goto('https://www.google.co.jp/')

            # title tag の値（ページタイトル）を取得し辞書に格納
            title_top = page.title()
            print('top page title: ', title_top)

            # Browser を閉じる
            browser.close()

        return {
            'top':{
                'title': title_top
            },
        }, 200
    except Exception as e:
        print(f'Exception occured! : {e}')
        return {'message': str(e)}, 500

# Start script
if __name__ == "__main__":
    try:
        main(SLEEP_MS)
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process
