require "rspec"
require "httparty"
require "dotenv/load" # .env ファイルをロード

RSpec.describe "Deployed Function Integration Test" do
  let(:base_url) { ENV["BASE_URL"] }

  it "returns Hello World! response" do
    response = HTTParty.get(base_url)
    expect(response.code).to eq(200)
    expect(response.body).to eq("Hello World!")
  end
end
