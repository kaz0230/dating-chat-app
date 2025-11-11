"""
性格を考慮したチャットエージェント（シンプル版）
"""
from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

class PersonalityChatAgent:
    def __init__(self, user_personality="INTJ", partner_personality="ENFP"):
        self.user_personality = user_personality
        self.partner_personality = partner_personality
        self.chat_history = []
        
        # VectorStore読み込み
        self.vectorstore_dir = Path("data/vectorstore")
        if not self.vectorstore_dir.exists():
            raise FileNotFoundError(
                f"VectorStoreが見つかりません: {self.vectorstore_dir}\n"
                "先に build_rag.py を実行してください。"
            )
        
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Chroma(
            collection_name="personality_db",
            embedding_function=self.embeddings,
            persist_directory=str(self.vectorstore_dir)
        )
        
        # LLM設定
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        
        # Retriever設定
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        # プロンプトテンプレート
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """あなたは出会い系サイトのチャット補助AIです。
以下の情報を活用して、ユーザーとの会話をサポートしてください：

- ユーザーの性格タイプ: {user_personality}
- 相手の性格タイプ: {partner_personality}

提供される性格診断情報を参考に、以下のサポートを行ってください：
1. 相手の性格特性を考慮した会話アドバイス
2. より良いコミュニケーションのための提案
3. 相手が好む話題や会話スタイルの提示

回答は簡潔で具体的に、フレンドリーなトーンで提供してください。

参考情報:
{context}

会話履歴:
{chat_history}
"""),
            ("human", "{question}")
        ])
    
    def format_docs(self, docs):
        """ドキュメントをフォーマット"""
        return "\n\n".join([f"[{doc.metadata['personality_type']}型]\n{doc.page_content}" for doc in docs])
    
    def format_chat_history(self):
        """会話履歴をフォーマット"""
        if not self.chat_history:
            return "なし"
        history_text = []
        for msg in self.chat_history[-5:]:  # 最新5件のみ
            history_text.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(history_text)
    
    def chat(self, user_message):
        """ユーザーメッセージに応答"""
        try:
            # 関連ドキュメントを検索
            docs = self.retriever.invoke(user_message)
            context = self.format_docs(docs)
            
            # プロンプトを構築
            messages = self.prompt.format_messages(
                user_personality=self.user_personality,
                partner_personality=self.partner_personality,
                context=context,
                chat_history=self.format_chat_history(),
                question=user_message
            )
            
            # LLMで生成
            response = self.llm.invoke(messages)
            answer = response.content
            
            # 会話履歴に追加
            self.chat_history.append({"role": "user", "content": user_message})
            self.chat_history.append({"role": "assistant", "content": answer})
            
            return {
                "answer": answer,
                "source_documents": docs
            }
            
        except Exception as e:
            return {
                "answer": f"エラーが発生しました: {str(e)}",
                "source_documents": []
            }
    
    def get_conversation_suggestions(self):
        """会話の提案を生成"""
        query = f"{self.partner_personality}の性格の人との会話で、どんな話題が良いですか？具体的に3つ提案してください。"
        result = self.chat(query)
        return result["answer"]
    
    def get_personality_insights(self, personality_type=None):
        """性格タイプの洞察を取得"""
        if personality_type is None:
            personality_type = self.partner_personality
        
        query = f"{personality_type}の性格特性について教えてください。"
        docs = self.vectorstore.similarity_search(query, k=2)
        
        insights = []
        for doc in docs:
            insights.append({
                "type": doc.metadata['personality_type'],
                "content": doc.page_content
            })
        
        return insights
    
    def clear_history(self):
        """会話履歴をクリア"""
        self.chat_history = []

if __name__ == "__main__":
    print("=== チャットエージェントテスト ===\n")
    
    agent = PersonalityChatAgent(
        user_personality="INTJ",
        partner_personality="ENFP"
    )
    
    # 会話提案のテスト
    print("【会話提案】")
    suggestions = agent.get_conversation_suggestions()
    print(suggestions)
    
    print("\n" + "="*50 + "\n")
    
    # チャットテスト
    print("【チャットテスト】")
    response = agent.chat("ENFPの人と初めて会話するとき、何に気をつければいいですか？")
    print(f"回答: {response['answer']}")
    
    if response['source_documents']:
        print(f"\n参考にした情報: {len(response['source_documents'])}件")
