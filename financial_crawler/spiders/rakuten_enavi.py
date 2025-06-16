import scrapy
from scrapy_playwright.page import PageMethod
import logging
import os
from scrapy.http import FormRequest
from loginform import fill_login_form

class RakutenEnaviSpider(scrapy.Spider):
    name = "rakuten_enavi"
    allowed_domains = ["rakuten-card.co.jp","login.account.rakuten.com"]
    start_urls = ["https://rakuten-card.co.jp/e-navi/"]
    logger = logging.getLogger(__name__)
    seq = 1
    result_dir = '/result/rakuten_enavi'
    user_id = 'testuser'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def get_result_file_path(self, seq, note=None):
        return os.path.join(self.result_dir, f'{self.name}_{seq}_{note}.html')

    def get_screenshot_file_path(self, seq, note=None):
        return os.path.join(self.result_dir, f'{self.name}_{seq}_{note}.png')
    
    def save_result(self, response, seq, note=None):
        result_file = self.get_result_file_path(seq, note)
        self.logger.debug(f'Saving results to {result_file}...')
        with open(result_file, 'w') as f:
            print(response.text, file=f)

    async def save_screenshot(self, response, seq, note=None):
        page = response.meta["playwright_page"]
        if page:
            screenshot_path = self.get_screenshot_file_path(seq, note)
            self.logger.debug(f'Saving screenshot to {screenshot_path}...')
            try:
                await page.screenshot(path=screenshot_path, full_page=True)
            finally:
                await page.close()

    def start_requests(self):
        self.logger.info('Start Rakuten e-NAVI Spider')
        self.logger.info(f'Result dir: {self.result_dir}')
        self.logger.info('Going to rakuten e-navi top page...')
        yield scrapy.Request(
            url = self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    # PageMethod("fill", "#user_id", self.user_id),
                    # # ボタンのcursorがnot-allowedでなくなるまで待つ
                    # PageMethod(
                    #     "wait_for_function",
                    #     """
                    #     () => {
                    #         const el = document.getElementById('cta001');
                    #         return el && window.getComputedStyle(el).cursor !== 'not-allowed';
                    #     }
                    #     """
                    # ),
                    # PageMethod("click", "#cta001"),
                    PageMethod("wait_for_load_state", "networkidle"),
                ],
            },
            callback=self.parse_top,
        )

    async def parse_top(self, response):
        # title tag の値（ページタイトル）を取得
        title = response.css('title::text').get()
        self.logger.info(f'top page title: {title}')
        button = response.css('#cta001').get()
        self.logger.info(f'button: {button}')
        # 結果をファイルに保存
        self.save_result(response, 1, 'top')
        await self.save_screenshot(response, 1, 'top')
        # ユーザーIDを入力して「次へ」をクリック
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'username': self.user_id,
                # 'password': 'testtest',  # パスワードはここでは入力しない
            },
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle"),
                ],
            },
            callback=self.parse_after_user_id,
        )
        # args, url, method = fill_login_form(response.url, response.body, self.user_id, "")
        # yield scrapy.Request(
        #     # url = self.start_urls[0],
        #     url = response.url,
        #     meta={
        #         "playwright": True,
        #         "playwright_include_page": True,
        #         # "playwright_page_methods": [
        #         #     PageMethod("fill", "#user_id", self.user_id),
        #         #     # ボタンのcursorがnot-allowedでなくなるまで待つ
        #         #     PageMethod(
        #         #         "wait_for_function",
        #         #         """
        #         #         () => {
        #         #             const el = document.getElementById('cta001');
        #         #             return el && window.getComputedStyle(el).cursor !== 'not-allowed';
        #         #         }
        #         #         """
        #         #     ),
        #         #     # ここでクリック
        #         #     PageMethod("click", "#cta001"),
        #         #     PageMethod("wait_for_load_state", "networkidle"),
        #         # ],
        #     },
        #     callback=self.parse_after_user_id,
        # )

    async def parse_after_user_id(self, response):
        # title tag の値（ページタイトル）を取得
        title = response.css('title::text').get()
        self.logger.info(f'after user_id page title: {title}')
        # 結果をファイルに保存
        self.save_result(response, 2, 'after_user_id')
        await self.save_screenshot(response, 2, 'after_user_id')
        # パスワード入力画面へ遷移
        # yield scrapy.Request(
        #     url = response.url,
        #     meta={
        #         "playwright": True,
        #         "playwright_include_page": True,
        #         "playwright_page_methods": [
        #             PageMethod("fill", "#password", "testtest"),
        #             PageMethod("wait_for_load_state", "networkidle"),
        #         ],
        #     },
        #     callback=self.parse_after_password,
        # )