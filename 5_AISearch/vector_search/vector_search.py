import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI   # 追加
import uuid
import json

SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"]
SEARCH_KEY = os.environ["SEARCH_KEY"]
index_name = "docs-sample-vectorindex"   # インデックス名を変更

AOAI_ENDPOINT = os.environ["AOAI_ENDPOINT"]   # 追加
AOAI_KEY = os.environ["AOAI_KEY"]   # 追加
aoai_api_version = "2024-06-01"
embedding_model_name = "text-embedding-3-large"  # 追加

credential = AzureKeyCredential(SEARCH_KEY)

# OpenAIでベクトルを取得する関数
def get_embeddings(text: str) -> list:
    aoai = AzureOpenAI(azure_endpoint=AOAI_ENDPOINT, api_key=AOAI_KEY, api_version=aoai_api_version)
    response = aoai.embeddings.create(input=text, model=embedding_model_name)
    return response.data[0].embedding

# ドキュメントフォルダ内のファイル群をインデックスに登録する関数
def upload_documents(path: str):
    search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=index_name, credential=credential)
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                document = {
                    "DocumentId": str(uuid.uuid4()),
                    "DocumentName": file,
                    "Content": content,
                    "ContentVector": get_embeddings(content),   # ベクトルを取得
                    "Tags": os.path.relpath(root, path).split(os.sep) + [os.path.splitext(file)[0]]  # root以外の複数のフォルダ名とファイル名をタグとして登録
                }
                search_client.upload_documents(documents=[document])
                print(f'Uploaded {file}')

# すべてのドキュメントを削除する関数
def delete_all_documents():
    search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=index_name, credential=credential)
    results = search_client.search(search_text="*")
    documents_to_delete = [{"DocumentId": doc["DocumentId"]} for doc in results]
    if documents_to_delete:
        search_client.delete_documents(documents=documents_to_delete)
        print(f'{len(documents_to_delete)} 件のドキュメントを削除しました')
    else:
        print('削除するドキュメントが見つかりませんでした')

# ベクトル検索の関数
def vector_search(search_text: str):
    search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=index_name, credential=credential)
    vector_query = VectorizedQuery(vector=get_embeddings(search_text), k_nearest_neighbors=3, fields="ContentVector")

    results = search_client.search(
        vector_queries=[vector_query]
    )

    for result in results:
        print(json.dumps(result, indent=2, ensure_ascii=False))

delete_all_documents()
upload_documents('docs')

vector_search('GraphRAGにはGlobalQueryというモードがあります')