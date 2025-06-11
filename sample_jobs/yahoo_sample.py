"""
A sample Yahoo Crawler.
"""
import logging
import os
from playwright.sync_api import sync_playwright
import json
import sys
import time

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 3000)
RESULT_PATH = os.getenv("RESULT_PATH", "/result")

# Define main script
def main(sleep_ms=3000, result_path="/result"):
    """Program that crawls Yahoo's top page and shopping page.
    This script uses Playwright to navigate to some pages,
    retrieves the page titles, and prints them to the console.
    It also saves the results in a specified directory.
    It is designed to run as a Cloud Run Job Task.

    Args:
        sleep_ms: number of milliseconds to sleep
    """
    print(f"Starting Yahoo Crawling Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")
    print(f"Result path: {result_path}, Sleep time: {sleep_ms} ms")

    exec_playwright(sleep_ms, result_path)

    print(f"Completed Task #{TASK_INDEX}.")

def exec_playwright(sleep_ms, result_path):
    try:
        with sync_playwright() as p:
            # Sequence No
            seq = 1
            # Chromium (Web Browser)のインスタンスを作成する
            browser = p.chromium.launch(headless=True)

            # 新しいページを作成する
            page = browser.new_page()
            logging.info('page: %s', page)

            # page.goto() で Yahoo のサイトにアクセス
            print('Going to top page...')
            page.goto('https://www.yahoo.co.jp/')

            # title tag の値（ページタイトル）を取得し辞書に格納
            title_top = page.title()
            print('top page title: ', title_top)
            # 結果をファイルに保存
            result_file = os.path.join(result_path, f'yahoo_crawl_result_{seq}.html')
            print(f'Saving results to {result_file}...')
            with open(result_file, 'w') as f:
                print(page.content(), file=f)
            seq += 1

            # 遷移前に待つ
            print(f'Sleeping for {sleep_ms} ms before navigating to next page...')
            time.sleep(float(sleep_ms) / 1000)  # Convert to seconds

            # yahoo shopping のページに遷移
            print('Going to shopping page...')
            page.locator("#Masthead").get_by_role("link", name="ショッピングへ遷移する").click()
            page.wait_for_load_state()  # ページ遷移後のロード完了を待機
            title_shopping = page.title()
            print('shopping page title: ', title_shopping)
            # 結果をファイルに保存
            result_file = os.path.join(result_path, f'yahoo_crawl_result_{seq}.html')
            print(f'Saving results to {result_file}...')
            with open(result_file, 'w') as f:
                print(page.content(), file=f)
            seq += 1

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
        print(f'Exception occured! : {e}')
        return {'message': str(e)}, 500

# Start script
if __name__ == "__main__":
    try:
        main(SLEEP_MS, RESULT_PATH)
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process
