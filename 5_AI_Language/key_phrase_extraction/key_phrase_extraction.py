import os
import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# 環境変数からキーとエンドポイントを取得
language_key = os.environ.get('LANGUAGE_KEY')
language_endpoint = os.environ.get('LANGUAGE_ENDPOINT')

# テキスト分析クライアントの作成
ta_credential = AzureKeyCredential(language_key)
client = TextAnalyticsClient(
        endpoint=language_endpoint, 
        credential=ta_credential)

try:
    # ./docs.mdファイルを読み込み、documentsリストに格納
    with open('./docs.md', 'r') as f:
        documents = [f.read()]
    
    # テキスト分析APIを使用してキーフレーズを抽出
    response = client.extract_key_phrases(documents = documents, language="ja")[0]
    
    if not response.is_error:
        print("\tKey Phrases:")
        for phrase in response.key_phrases:
            print("\t\t", phrase)
    else:
        print(response.id, response.error)

    # responseをJson構造でresult.jsonに保存
    # 必要な情報を抽出してJSON構造に変換
    result = {
        "key_phrases": response.key_phrases
    }
    with open('./result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))


except Exception as err:
    print("Encountered exception. {}".format(err))
