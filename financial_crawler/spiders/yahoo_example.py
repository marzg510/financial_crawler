import scrapy
from scrapy_playwright.page import PageMethod
import logging
import os

class YahooExampleSpider(scrapy.Spider):
    name = "yahoo_example"
    allowed_domains = ["yahoo.co.jp"]
    start_urls = ["https://www.yahoo.co.jp"]
    logger = logging.getLogger(__name__)
    seq = 1
    result_path = '/result'

    def start_requests(self):
        self.logger.info('Going to yahoo top page...')
        ss_file = os.path.join(self.result_path, f'yahoo_crawl_result_{self.seq}.png')
        yield scrapy.Request(
            url = self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle"),
                    PageMethod("screenshot", path=ss_file, full_page=True),
                    # PageMethod("click", "#Masthead >> role=link[name=\"ショッピングへ遷移する\"]"),
                ],
            },
            callback=self.parse_top,
        )
    def parse_top(self, response):
        # title tag の値（ページタイトル）を取得
        title = response.xpath('//title/text()').get()
        self.logger.info(f'top page title: {title}')
        # 結果をファイルに保存
        result_file = os.path.join(self.result_path, f'yahoo_crawl_result_{self.seq}.html')
        self.logger.info(f'Saving results to {result_file}...')
        with open(result_file, 'w') as f:
            print(response.text, file=f)
        self.seq += 1
        # yahoo shopping のページに遷移
        url = response.css('#Masthead a[href][aria-label="ショッピングへ遷移する"]').attrib['href']
        ss_file = os.path.join(self.result_path, f'yahoo_crawl_result_{self.seq}.png')
        self.logger.info(f'Going to shopping page "{url}" ...')
        yield scrapy.Request(
            url = url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("screenshot", path=ss_file, full_page=False)
                ],
            },
            callback=self.parse_shopping_page,
        )
    def parse_shopping_page(self, response):
        # title tag の値（ページタイトル）を取得
        title = response.xpath('//title/text()').get()
        self.logger.info(f'shopping page title: {title}')
        # 結果をファイルに保存
        result_file = os.path.join(self.result_path, f'yahoo_crawl_result_{self.seq}.html')
        self.logger.info(f'Saving results to {result_file}...')
        with open(result_file, 'w') as f:
            print(response.text, file=f)
        self.seq += 1
