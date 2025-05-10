require "rspec"
require "httparty"
require "dotenv/load" # .env ファイルをロード
# require "json"

RSpec.describe "Deployed Function Integration Test" do
  let(:base_url) { ENV["BASE_URL"] }

  it "returns Yahoo Japan response" do
    response = HTTParty.get(base_url)
    # ステータスコードの確認
    expect(response.code).to eq(200)

    # レスポンスの JSON を解析
    json_response = JSON.parse(response.body)

    # タイトルの確認
    expect(json_response["title"]).to eq("Yahoo! JAPAN")

    # 整形されたHTMLの確認
    expect(json_response["formatted_html"]).to include("<title>Yahoo! JAPAN</title>")
    expect(json_response["formatted_html"]).to include("<h1>Welcome to Yahoo!</h1>")
  end
end
