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
    result = client.recognize_linked_entities(documents = documents)[0]
    
    print("Linked Entities:\n")
    for entity in result.entities:
        print("\tName: ", entity.name, "\tId: ", entity.data_source_entity_id, "\tUrl: ", entity.url,
        "\n\tData Source: ", entity.data_source)
        print("\tMatches:")
        for match in entity.matches:
            print("\t\tText:", match.text)
            print("\t\tConfidence Score: {0:.2f}".format(match.confidence_score))
            print("\t\tOffset: {}".format(match.offset))
            print("\t\tLength: {}".format(match.length))


except Exception as err:
    print("Encountered exception. {}".format(err))
