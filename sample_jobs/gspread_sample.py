"""
A sample Google Spreadsheet Writer.
"""
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 3000)
RESULT_PATH = os.getenv("RESULT_PATH", "/result")

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証情報の設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('import-job-account.json', scope)

# クライアントの作成
client = gspread.authorize(creds)

# スプレッドシートの取得
spreadsheet = client.open_by_key('1OdWwns4n9J54UgTQj4Jm1k6o8cQ9xBGu_nKOSs16r3E')
print(("Spreadsheet title:", spreadsheet.title))

# ワークシートの取得
# worksheet = spreadsheet.sheet1

# シート名で指定
worksheet = spreadsheet.worksheet("Plane")

# インデックス番号で指定（1番目のシート）
# worksheet = spreadsheet.get_worksheet(0)

print(("Worksheet title:", worksheet.title))

# 全データの取得
data = worksheet.get_all_values()
print(data)

# 特定のセルの値を取得
cell_value = worksheet.acell('A1').value
print(f"A1セルの値: {cell_value}")

# 特定の範囲の値を取得
range_values = worksheet.get('A1:B2')
print(f"A1:B2の値: {range_values}")

# 特定のセルに値を書き込む
worksheet.update_acell('D1', 'Hello World')

# 特定の範囲に値を書き込む
worksheet.update(range_name='D2:E2', values=[['Foo', 'Bar']])

# 新しい行を追加
# worksheet.append_row(['New', 'Row', 'Data'])