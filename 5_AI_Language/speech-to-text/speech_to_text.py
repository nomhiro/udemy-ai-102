import os
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

# m4aファイルをwavファイルに変換
audio = AudioSegment.from_file("./audio_sample.m4a", format="m4a")
audio.export("./audio_sample.wav", format="wav")

# 環境数を読み込む
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

try:
  # SpeechConfigオブジェクトを作成
  speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
  speech_config.speech_recognition_language="ja-JP"
  
  # AudioConfigオブジェクトを作成 wavファイルを指定
  audio_config = speechsdk.audio.AudioConfig(filename="audio_sample.wav")
  # SpeechRecognizerオブジェクトを作成
  speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
  
  # 音声テキスト変換を実行
  result = speech_recognizer.recognize_once_async().get()
  
  # 結果を表示
  if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))

except Exception as err:
  print("Unexpected error: {}".format(err))