# financial_crawler
crawl the financial(motrgage rate) sites

## Google Cloud Console

https://console.cloud.google.com/welcome?hl=ja&inv=1&invt=AbwiGQ&project=mortgage-458822


## Dev Container

- gcloudの質問プロンプトが出てきますが、すべてデフォルト（ENTERを押す）で進めてください。

- 初期化設定
```
gcloud init
gcloud config set project mortgage-458822
```

## Hello World

### セットアップ

```
cd helloworld
bundle install
```

### 動作確認

- 以下を実行してブラウザからlocalhost:8000にアクセス

```
functions-framework-ruby --target=hello_get
```

- Hello Worldと表示されることを確認
