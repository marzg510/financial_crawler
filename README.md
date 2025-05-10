# financial_crawler
crawl the financial(motrgage rate) sites

## Google Cloud Console

- https://console.cloud.google.com/welcome

GET URL
```
gcloud run services describe ruby-http-function --region=asia-northeast1  --format=json
```

## Dev Container

- gcloudの質問プロンプトが出てきますが、すべてデフォルト（ENTERを押す）で進めてください。

- 初期化設定
```
gcloud init
gcloud config set project PROJECT_ID
```


## HelloWorld

### デプロイ

```
cd helloworld
gcloud run deploy --source .
```

## Playwright

ビルド＆プッシュ
```
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/playwright-sheets
```

デプロイ
```
gcloud run deploy playwright-sheets
--image gcr.io/YOUR_PROJECT_ID/playwright-sheets
--platform managed
--allow-unauthenticated
```


--set-env-vars GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json


## 以下はRuby版Function

## Yahoo Top Getter

### セットアップ

```
cd yahoo_top_getter
bundle install
```

### 動作確認

- 以下を実行してブラウザからlocalhost:8000にアクセス

```
rerun -- functions-framework-ruby --target=yahoo_top_get
```

### 単体テスト

```
bundle exec rspec spec/unit/
```

### デプロイ

```
gcloud run deploy ruby-yahoo-top-get --base-image ruby33 --region asia-northeast1 \
       --allow-unauthenticated \
       --source . \
       --function yahoo_top_get
```

### 結合テスト

```
bundle exec rspec spec/integration/
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

### 単体テスト

```
bundle exec rspec spec/unit/
```

### デプロイ

```
gcloud run deploy ruby-http-function --base-image ruby33 --region asia-northeast1 \
       --allow-unauthenticated \
       --source . \
       --function hello_get
```

### 結合テスト

```
bundle exec rspec spec/integration/
```