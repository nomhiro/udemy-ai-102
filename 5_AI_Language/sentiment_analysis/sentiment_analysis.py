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
  with open("./doc.md", "r") as f:
    documents = [f.read()]
  
  # テキスト分析APIで感情分析
  result = ta_client.analyze_sentiment(documents=documents, show_opinion_mining=True)
  # doc_result = [doc for doc in result if not doc.is_error]
  
  positive_mined_opinions = []
  mixed_mined_opinions = []
  negative_mined_opinions = []

  for document in result:
    print(f"Document Sentiment: {format(document.sentiment)}")
    output = {
      "document_sentiment": document.sentiment,
      "overall_scores": {
        "positive": document.confidence_scores.positive,
        "neutral": document.confidence_scores.neutral,
        "negative": document.confidence_scores.negative
      },
      "sentences": []
    }
    for sentence in document.sentences:
      sentence_data = {
        "text": sentence.text,
        "sentiment": sentence.sentiment,
        "scores": {
          "positive": sentence.confidence_scores.positive,
          "neutral": sentence.confidence_scores.neutral,
          "negative": sentence.confidence_scores.negative
        },
        "mined_opinions": []
      }
      for mined_opinion in sentence.mined_opinions:
        target = mined_opinion.target
        target_data = {
          "sentiment": target.sentiment,
          "text": target.text,
          "scores": {
            "positive": target.confidence_scores.positive,
            "negative": target.confidence_scores.negative
          },
          "assessments": []
        }
        for assessment in mined_opinion.assessments:
          assessment_data = {
            "sentiment": assessment.sentiment,
            "text": assessment.text,
            "scores": {
              "positive": assessment.confidence_scores.positive,
              "negative": assessment.confidence_scores.negative
            }
          }
          target_data["assessments"].append(assessment_data)
        sentence_data["mined_opinions"].append(target_data)
      output["sentences"].append(sentence_data)

  with open('./result.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(output, indent=2, ensure_ascii=False))
  

except Exception as ex:
  print("Error:", ex)