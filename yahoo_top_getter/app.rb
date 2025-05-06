require "functions_framework"
require "httparty"
require "nokogiri"

FunctionsFramework.http "yahoo_top_get" do |_request|
  # YahooトップページのURL
  url = "https://www.yahoo.co.jp"

  # HTTPリクエストを送信してHTMLを取得
  response = HTTParty.get(url)

  # NokogiriでHTMLを解析
  parsed_html = Nokogiri::HTML(response.body)

  # ページタイトルを取得
  title = parsed_html.at("title")&.text

  # HTMLを整形（インデントを付けて見やすくする）
  formatted_html = parsed_html.to_xhtml(indent: 2)

  # ページタイトルと整形されたHTMLをJSON形式で返す
  { title: title, formatted_html: formatted_html, message: "HTML fetched and formatted successfully" }.to_json
end
