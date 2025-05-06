require "rspec"
require "functions_framework/testing"
require "httparty"
require "nokogiri"
require_relative "../../app"

RSpec.describe "YahooTopGet Function" do
  include FunctionsFramework::Testing

  let(:mock_html) do
    <<-HTML
      <html>
        <head>
          <title>Yahoo! JAPAN</title>
        </head>
        <body>
          <h1>Welcome to Yahoo!</h1>
        </body>
      </html>
    HTML
  end

  before do
    # HTTParty のモックを設定
    allow(HTTParty).to receive(:get).and_return(double(body: mock_html))
  end

  it "returns the correct title and formatted HTML" do
    load_temporary("app.rb") do
      request = make_get_request("http://example.com/")
      response = call_http("yahoo_top_get", request)

      # ステータスコードの確認
      expect(response.status).to eq(200)

      # レスポンスの JSON を解析
      json_response = JSON.parse(response.body.join)

      # タイトルの確認
      expect(json_response["title"]).to eq("Yahoo! JAPAN")

      # 整形されたHTMLの確認
      expect(json_response["formatted_html"]).to include("<title>Yahoo! JAPAN</title>")
      expect(json_response["formatted_html"]).to include("<h1>Welcome to Yahoo!</h1>")
    end
  end
end
