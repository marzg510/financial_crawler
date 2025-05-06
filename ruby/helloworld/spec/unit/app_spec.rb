require "functions_framework/testing"
require_relative "../../app"

RSpec.describe "HelloGet Function" do
  include FunctionsFramework::Testing

  it "returns Hello World! response" do
    load_temporary("app.rb") do
      request = make_get_request("http://localhost/")
      response = call_http("hello_get", request)
      expect(response).to be_ok
      expect(response.body.join).to eq("Hello World!")
    end
  end
end
