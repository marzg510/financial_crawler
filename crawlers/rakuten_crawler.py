"""
A Rakuten Crawler.
"""
import os
import asyncio
from playwright.async_api import async_playwright
import sys
import tracemalloc

tracemalloc.start()

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
RESULT_PATH = os.getenv("RESULT_PATH", "/result")
USER_ID = os.getenv("RAKUTEN_ID")
USER_PASSWORD = os.getenv("RAKUTEN_PASSWORD")

# Define main script
async def main(user_id, user_password, result_path="/result"):
    """Program that crawls Rakuten Household data.
    This script uses Playwright to navigate to some pages.
    It also saves the results in a specified directory.
    It is designed to run as a Cloud Run Job Task.

    Args:
        result_path: output directory path where results will be saved.
    """
    print(f"Starting Rakuten Crawling Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")
    print(f"Result path: {result_path}")

    await crawl(user_id, user_password, result_path)

    print(f"Completed Task #{TASK_INDEX}.")

async def crawl(user_id, user_password, result_path):
    try:
        async with async_playwright() as p:
            # Sequence No
            seq = 1
            # Chromium (Web Browser)のインスタンスを作成する
            browser = await p.chromium.launch(headless=True)

            # 新しいページを作成する
            page = await browser.new_page()

            # ログインページにアクセス
            print('Going to Login page...')
            await page.goto('https://www.yahoo.co.jp/')

            # title tag の値（ページタイトル）を取得し辞書に格納
            title_top = await page.title()
            print('top page title: ', title_top)
            # 結果をファイルに保存
            result_file = os.path.join(result_path, f'yahoo_crawl_result_{seq}.html')
            print(f'Saving results to {result_file}...')
            with open(result_file, 'w') as f:
                print(await page.content(), file=f)
            seq += 1

            # Browser を閉じる
            await browser.close()

    except Exception as e:
        print(f'Exception occured! : {e}')

# Start script
if __name__ == "__main__":
    try:
        asyncio.run(main(USER_ID, USER_PASSWORD, RESULT_PATH))
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print("message", message, "severity", "ERROR")
        sys.exit(1)  # Retry Job Task by exiting the process
