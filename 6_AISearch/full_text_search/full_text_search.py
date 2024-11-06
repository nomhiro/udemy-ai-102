import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    SearchIndex
)
import uuid
import json

SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"]
SEARCH_KEY = os.environ["SEARCH_KEY"]
index_name = "docs-sample"

credential = AzureKeyCredential(SEARCH_KEY)

# インデックスを作成する関数
def create_index():

    # インデックスのスキーマを定義する
    index_client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT, credential=credential)
    fields = [
            SimpleField(name="DocumentId", type=SearchFieldDataType.String, key=True),
            SearchableField(name="DocumentName", type=SearchFieldDataType.String, sortable=True),
            SearchableField(name="Content", type=SearchFieldDataType.String, analyzer_name="ja.lucene"),

            SearchableField(name="Tags", collection=True, type=SearchFieldDataType.String, facetable=True, filterable=True),
        ]

    # スコアリングプロファイルを定義する（今回は使わない）
    scoring_profiles = []
    # サジェスターを定義する
    suggester = [{'name': 'sg', 'source_fields': ['Tags']}]

    # インデックスを作成する
    index = SearchIndex(name=index_name, fields=fields, suggesters=suggester, scoring_profiles=scoring_profiles)
    result = index_client.create_or_update_index(index)
    print(f'{result.name} created')

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

# フルテキスト検索の関数
def full_text_search(search_text: str):
    search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=index_name, credential=credential)
    results = search_client.search(search_text=search_text)
    for result in results:
        print(json.dumps(result, indent=2, ensure_ascii=False))

create_index()

delete_all_documents()
upload_documents('docs')

full_text_search('GraphRAGにはGlobalQueryというモードがあります')