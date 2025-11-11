"""
B（女性）シミュレーションエージェント
"""
from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class WomanAgent:
    """B（女性）のシミュレーションエージェント"""
    
    def __init__(self, woman_profile):
        self.profile = woman_profile
        
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
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.8)
        
        # 会話履歴
        self.conversation_history = []
    
    def _get_personality_context(self):
        """性格情報をRAGから取得"""
        query = f"{self.profile.personality_type}の性格特性について"
        docs = self.vectorstore.similarity_search(query, k=2)
        
        context = "\n\n".join([
            f"[{doc.metadata['personality_type']}型の特性]\n{doc.page_content}"
            for doc in docs
        ])
        
        return context
    
    def _format_conversation_history(self):
        """会話履歴をフォーマット"""
        if not self.conversation_history:
            return "（まだ会話が始まっていません）"
        
        history_text = []
        for msg in self.conversation_history[-5:]:  # 最新5件
            speaker = "あなた" if msg['speaker'] == 'B' else "相手の男性"
            history_text.append(f"{speaker}: {msg['message']}")
        
        return "\n".join(history_text)
    
    def generate_message(self, is_first_message=False):
        """B（女性）のメッセージを生成"""
        
        # 性格情報を取得
        personality_context = self._get_personality_context()
        
        # プロンプトテンプレート
        if is_first_message:
            system_message = """あなたは以下のプロフィールを持つ女性として、出会い系サイトで初めての相手にメッセージを送ります。

【あなたのプロフィール】
{profile}

【あなたの性格特性】
{personality_context}

【指示】
上記のプロフィールと性格特性を忠実に反映して、初めての相手への自然で親しみやすいメッセージを生成してください。

重要ポイント:
- {age}歳の女性らしい言葉遣いと視点で書く
- {speaking_style}を意識する
- 自己紹介を簡潔に含める
- 相手のプロフィールを見て興味を持った点に触れる
- 質問を1つ含めて、会話のきっかけを作る
- 2-3文程度の自然な長さ
- 過度に親しくしすぎない、適度な距離感

【メッセージ】"""
        else:
            system_message = """あなたは以下のプロフィールを持つ女性として会話を続けます。

【あなたのプロフィール】
{profile}

【あなたの性格特性】
{personality_context}

【これまでの会話】
{conversation_history}

【指示】
上記のプロフィールと性格特性、会話の流れを考慮して、自然な返信を生成してください。

重要ポイント:
- {age}歳の女性らしい言葉遣いと視点
- {speaking_style}を意識する
- 会話の流れに自然に沿う
- 趣味（{hobbies}）や家族、居住地の話題を適度に含める
- {personality_type}型の性格特性を表現
- 相手に興味を示し、質問も含める（ただし質問攻めにしない）
- 1-3文程度の簡潔で自然な返信

【返信】"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "メッセージを生成してください。")
        ])
        
        # プロンプト変数を準備
        profile_dict = self.profile.to_dict()
        
        messages = prompt.format_messages(
            profile=self.profile.get_prompt_text(),
            personality_context=personality_context,
            conversation_history=self._format_conversation_history(),
            age=profile_dict['age'],
            speaking_style=profile_dict['speaking_style'],
            hobbies=profile_dict['hobbies_text'],
            personality_type=profile_dict['personality_type']
        )
        
        # LLMで生成
        response = self.llm.invoke(messages)
        message = response.content.strip()
        
        # 会話履歴に追加
        self.conversation_history.append({
            "speaker": "B",
            "message": message
        })
        
        return message
    
    def add_user_message(self, message):
        """ユーザー（A: 男性）のメッセージを履歴に追加"""
        self.conversation_history.append({
            "speaker": "A",
            "message": message
        })
    
    def clear_history(self):
        """会話履歴をクリア"""
        self.conversation_history = []
