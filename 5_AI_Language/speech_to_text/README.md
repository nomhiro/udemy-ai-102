必要なオーディオライブラリがOSにインストールされている必要があります。

### Linux環境の場合
以下のコマンドをターミナルで実行して、必要なライブラリをインストールします。

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### WindowsOSの場合
ffmpegをインストールする手順は以下の通りです。
- FFmpegの公式サイトからWindows用のビルドをダウンロードします。
  https://ffmpeg.org/download.html
- ダウンロードしたZIPファイルを解凍します。
- 解凍したフォルダを任意の場所に移動します（例: C:\ffmpeg）。
- 環境変数にffmpegのパスを追加します。