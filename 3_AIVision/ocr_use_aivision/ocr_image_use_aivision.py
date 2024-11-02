import os
import json
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# 環境変数からエンドポイントとキーを取得
try:
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# 画像解析クライアントの初期化
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# 画像解析の実行
result = client.analyze(
    image_data=open("./image-001.png", "rb"),
    visual_features=[VisualFeatures.READ]
)

# Json形式で結果を表示
print("result: ", json.dumps(result.as_dict(), indent=4, ensure_ascii=False))

# Jsonをファイルに保存
with open("result.json", "w") as f:
    json.dump(result.as_dict(), f, indent=4, ensure_ascii=False)