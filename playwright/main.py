import asyncio
from flask import Flask
from playwright.async_api import async_playwright
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

app = Flask(name)

SPREADSHEET_NAME = "Your Spreadsheet Title"

@app.route("/")
def run():
    asyncio.run(run_main())
    return "データ取得＆書き込み完了"

async def run_main():
# 1. Playwrightでページ取得
async with async_playwright() as p:
browser = await p.chromium.launch()
page = await browser.new_page()
await page.goto("https://www.yahoo.co.jp")
title = await page.title()
await browser.close()