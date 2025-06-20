# financial_crawler

crawl the financial(mortgage rate) sites


## 環境構築

1. Google Cloudのプロジェクトを作成
2. APIを有効化(#45)
3. サービスアカウントを作成してキーをダウンロードし、プロジェクトrootにimport-job-account.jsonとして保存

## Google Cloud Console

- https://console.cloud.google.com/welcome

## ローカル開発・テスト

### コンテナのビルド

```shell
docker image build -t financial-crawler-local:latest .
```

### スクリプトのローカル実行、デバッグ

```shell
docker run --rm -v ${PWD}:/app -v ${PWD}/result:/result -it financial-crawler-local python3 sample_jobs/yahoo_sample.py
docker run --rm -v ${PWD}:/app -v ${PWD}/result:/result -it financial-crawler-local scrapy crawl yahoo_example -L INFO
```

## Cloud Run Jobs

### ビルド

```shell
gcloud builds submit --tag asia-northeast1-docker.pkg.dev/mortgage-458822/cloud-run-source-deploy/financial-crawler-job-image .
```

### デプロイ

#### Scrapy

```shell
gcloud run jobs deploy yahoo-scrapy-example \
    --command=scrapy,crawl \
    --args=yahoo_example \
    --image asia-northeast1-docker.pkg.dev/mortgage-458822/cloud-run-source-deploy/financial-crawler-job-image \
    --clear-volumes \
    --add-volume name=gcs1,type=cloud-storage,bucket=financial_crawler \
    --add-volume-mount volume=gcs1,mount-path=/result \
    --execute-now \
    --region asia-northeast1
```

#### Python

```shell
gcloud run jobs deploy yahoo-sample \
    --command=python3 \
    --args=sample_jobs/yahoo_sample.py \
    --set-env-vars SLEEP_MS=1000 \
    --image asia-northeast1-docker.pkg.dev/mortgage-458822/cloud-run-source-deploy/financial-crawler-job-image \
    --clear-volumes \
    --add-volume name=gcs1,type=cloud-storage,bucket=financial_crawler \
    --add-volume-mount volume=gcs1,mount-path=/result \
    --execute-now \
    --region asia-northeast1
```

### 実行

```shell
gcloud run jobs execute file-save-sample --region asia-northeast1
```

### 確認

```shell
gcloud run jobs executions describe test-main-sample-crawler-2r72g --region asia-northeast1
```

## Cloud Run

### Deploy

- https://cloud.google.com/code/docs/vscode/deploy-service?hl=ja

- Command

```bash
gcloud run deploy financial-crawler --project PROJECTID --image gcr.io/PROJECTID/financial-crawler --client-name "Cloud Code for VS Code" --client-version 2.31.1 --platform managed --region asia-northeast1 --allow-unauthenticated --port 8080 --cpu 1 --memory 512Mi --concurrency 80 --timeout 300 --clear-env-vars
```

## GET URL

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