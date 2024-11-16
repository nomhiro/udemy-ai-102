import os
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

# Convert m4a to wav
audio = AudioSegment.from_file("audio_sample.m4a", format="m4a")
audio.export("./audio_sample.wav", format="wav")

SPEECH_KEY = os.environ.get('SPEECH_KEY')
SPEECH_REGION = os.environ.get('SPEECH_REGION')

try:
    # SpeechConfigを作成
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language="ja-JP"

    # AudioConfigを作成　wavファイルを指定
    audio_config = speechsdk.audio.AudioConfig(filename="audio_sample.wav")
    # SpeechRecognizerを作成
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 音声認識を実行
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # 結果を表示
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))

except Exception as err:
    print("Encountered exception. {}".format(err))
    