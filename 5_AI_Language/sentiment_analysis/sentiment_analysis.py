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
