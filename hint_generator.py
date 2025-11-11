"""
回答ヒント生成クラス
"""
import json
from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class HintGenerator:
    """回答ヒント生成"""
    
    def __init__(self, man_profile, woman_profile):
        self.man_profile = man_profile
        self.woman_profile = woman_profile
        
        # VectorStore読み込み
        self.vectorstore_dir = Path("data/vectorstore")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = Chroma(
            collection_name="personality_db",
            embedding_function=self.embeddings,
            persist_directory=str(self.vectorstore_dir)
        )
        
        # LLM設定
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    
    def _get_personality_traits(self, personality_type):
        """性格特性をRAGから取得"""
        query = f"{personality_type}の性格特性について"
        docs = self.vectorstore.similarity_search(query, k=2)
        
        traits = "\n".join([doc.page_content[:200] for doc in docs])
        return traits
    
    def generate_hint(self, woman_message, conversation_history):
        """回答ヒントを生成"""
        
        # 性格特性を取得
        man_traits = self._get_personality_traits(self.man_profile.personality_type)
        woman_traits = self._get_personality_traits(self.woman_profile.personality_type)
        
        # 会話履歴のフォーマット
        history_text = "\n".join([
            f"{msg['speaker']}: {msg['message']}"
            for msg in conversation_history[-5:]
        ])
        
        # プロンプトテンプレート
        system_message = """あなたは出会い系サイトのチャット補助AIです。

【男性ユーザー（A: あなた）】
- 性格タイプ: {man_personality}
- 性格特性: 
{man_traits}

【女性相手（B）- 詳細プロフィール】
{woman_profile}

- 性格特性:
{woman_traits}

【女性の最新メッセージ】
{woman_message}

【会話履歴】
{conversation_history}

【タスク】
女性の詳細なプロフィール（年齢、居住地、家族構成、趣味）と性格特性を考慮して、
男性ユーザーに最適な回答アドバイスを提供してください。

以下のJSON形式で生成してください：

{{
  "recommended_response": "女性が好みそうな最適な返信案（1-2文）",
  "profile_points": {{
    "age": "年齢を考慮したポイント（簡潔に）",
    "location": "居住地を考慮したポイント（簡潔に）",
    "family": "家族構成を考慮したポイント（簡潔に）",
    "hobbies": "趣味を考慮したポイント（簡潔に）"
  }},
  "personality_points": [
    "性格タイプの考慮ポイント1",
    "性格タイプの考慮ポイント2"
  ],
  "good_example": {{
    "text": "男性の性格を活かした好まれそうな回答例",
    "reason": "なぜこれが良いか"
  }},
  "bad_example": {{
    "text": "男性の性格で出やすい避けるべき回答例",
    "reason": "なぜこれが悪いか"
  }}
}}

JSONのみを出力してください。他のテキストは含めないでください。"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "回答ヒントを生成してください。")
        ])
        
        woman_profile_dict = self.woman_profile.to_dict()
        
        messages = prompt.format_messages(
            man_personality=self.man_profile.personality_type,
            man_traits=man_traits,
            woman_profile=self.woman_profile.get_prompt_text(),
            woman_traits=woman_traits,
            woman_message=woman_message,
            conversation_history=history_text if history_text else "（初回メッセージ）"
        )
        
        # LLMで生成
        try:
            response = self.llm.invoke(messages)
            response_text = response.content.strip()
            
            # マークダウンのコードブロックを除去
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # JSONをパース
            hint = json.loads(response_text)
            return hint
            
        except json.JSONDecodeError as e:
            # JSONパースエラーの場合はフォールバック
            return {
                "recommended_response": "相手のメッセージに共感を示し、自然な質問で会話を深めましょう。",
                "profile_points": {
                    "age": f"{woman_profile_dict['age']}歳の女性として、落ち着いた対応を",
                    "location": f"{woman_profile_dict['location']}の地域性を意識して",
                    "family": f"{woman_profile_dict['family_structure']}の状況を理解して",
                    "hobbies": f"{woman_profile_dict['hobbies_text']}への興味を示して"
                },
                "personality_points": [
                    f"{woman_profile_dict['personality_type']}型は共感を重視します",
                    "具体的な質問で興味を示しましょう"
                ],
                "good_example": {
                    "text": "素敵ですね！もっと詳しく教えていただけますか？",
                    "reason": "興味と共感を示している"
                },
                "bad_example": {
                    "text": "へー、そうなんですか。",
                    "reason": "興味が感じられない"
                }
            }
