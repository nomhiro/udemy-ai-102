import os
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

DI_ENDPOINT = os.getenv("DI_ENDPOINT")
DI_KEY = os.getenv("DI_KEY")

try: 
  credential = AzureKeyCredential(DI_KEY)
  document_analysis_client = DocumentIntelligenceClient(DI_ENDPOINT, credential)
  
  file_path = "./di-sample.png"
  
  # ./di-sample-png.pngを読み込み、layoutモデルで解析
  with open(file_path, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
      model_id="prebuilt-layout",
      analyze_request=f,
      content_type="application/octet-stream",
      output_content_format="markdown"
    )
  # json形式で結果を取得
  result = poller.result()
  
  # Markdownの内容をpngファイル名.mdで保存
  with open(f"{file_path}.md", "w") as f:
    f.write(result.content)

except Exception as ex:
  print(f"Error: {ex}")
  