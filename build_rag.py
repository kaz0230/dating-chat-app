"""
RAGシステム構築スクリプト
"""
import json
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class PersonalityRAG:
    def __init__(self):
        self.data_dir = Path("data/raw")
        self.vectorstore_dir = Path("data/vectorstore")
        self.vectorstore_dir.mkdir(parents=True, exist_ok=True)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, 
            chunk_overlap=50, 
            length_function=len
        )
    
    def load_personality_data(self):
        all_data_file = self.data_dir / "all_personalities.json"
        if not all_data_file.exists():
            raise FileNotFoundError(
                f"データファイルが見つかりません: {all_data_file}\n"
                "先に personality_scraper.py を実行してください。"
            )
        with open(all_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ データ読み込み完了: {len(data)}件")
        return data
    
    def create_documents(self, personality_data):
        documents = []
        for person in personality_data:
            chunks = self.text_splitter.split_text(person['content'])
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk, 
                    metadata={
                        "personality_type": person['code'], 
                        "title": person['title'], 
                        "chunk_id": i, 
                        "source": person['url']
                    }
                )
                documents.append(doc)
        print(f"✓ ドキュメント作成完了: {len(documents)}個")
        return documents
    
    def build_vectorstore(self, documents):
        print("ベクトルDB構築中...")
        vectorstore = Chroma.from_documents(
            documents=documents, 
            embedding=self.embeddings, 
            collection_name="personality_db", 
            persist_directory=str(self.vectorstore_dir)
        )
        print(f"✓ VectorStore構築完了: {self.vectorstore_dir}")
        return vectorstore
    
    def test_search(self, vectorstore, query="INTJの特徴は？", k=3):
        print(f"\n=== 検索テスト ===")
        print(f"クエリ: {query}")
        print(f"取得件数: {k}\n")
        results = vectorstore.similarity_search(query, k=k)
        for i, doc in enumerate(results, 1):
            print(f"--- 結果 {i} ---")
            print(f"性格タイプ: {doc.metadata['personality_type']}")
            print(f"内容: {doc.page_content[:200]}...")
            print()
    
    def build(self):
        print("=== RAGシステム構築開始 ===\n")
        personality_data = self.load_personality_data()
        documents = self.create_documents(personality_data)
        vectorstore = self.build_vectorstore(documents)
        self.test_search(vectorstore)
        print("\n=== RAGシステム構築完了 ===")
        return vectorstore

if __name__ == "__main__":
    rag = PersonalityRAG()
    rag.build()
