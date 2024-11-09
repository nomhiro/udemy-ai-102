import os
import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# 環境変数からキーとエンドポイントを取得
language_endpoint = os.getenv("LANGUAGE_ENDPOINT")
language_key = os.getenv("LANGUAGE_KEY")

ta_credential = AzureKeyCredential(language_key)
ta_client = TextAnalyticsClient(
  endpoint=language_endpoint,
  credential=ta_credential
)

try:
  # ./docs.mdファイルを読み込み、documentsリストに格納
  with open('./docs.md', 'r') as f:
    documents = [f.read()]
  
  # テキスト分析APIを使用してキーフレーズを抽出
  result = ta_client.recognize_linked_entities(documents = documents)[0]
  
  # Json形式で出力するためのリストを作成
  output = []
  # エンティティごとに情報を取得し、outputリストに格納
  for entity in result.entities:
    entity_info = {
      "Name": entity.name,
      "Id": entity.data_source_entity_id,
      "Url": entity.url,
      "Data Source": entity.data_source,
      "Matches": []
    }
    # エンティティにマッチした単語情報を取得
    for match in entity.matches:
      match_info = {
        "Text": match.text,
        "Confidence Score": round(match.confidence_score, 2),
        "Offset": match.offset,
        "Length": match.length
      }
      entity_info["Matches"].append(match_info)
    output.append(entity_info)
  
  # result.jsonに結果を書き込み
  with open('./result.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

except Exception as err:
  print("Encountered exception. {}".format(err))
