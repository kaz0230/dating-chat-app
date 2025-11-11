"""
プロフィール管理クラス
"""
import random
from config import (
    AGE_OPTIONS, FAMILY_DETAILS, get_speaking_style
)

class WomanProfile:
    """B（女性）のプロフィール"""
    
    def __init__(
        self,
        age_range="50代前半",
        location_area="東京23区",
        location_detail="杉並区",
        family_structure="一人暮らし",
        hobbies=None,
        personality_type="ENFP"
    ):
        # 選択された情報
        self.age_range = age_range
        self.age = self._generate_age(age_range)
        self.location_area = location_area
        self.location_detail = location_detail
        self.family_structure = family_structure
        self.family_detail = self._generate_family_detail(family_structure)
        self.hobbies = hobbies if hobbies else ["料理", "温泉"]
        self.personality_type = personality_type
        
        # 固定情報
        self.gender = "女性"
        self.name = "相手の女性"
        
        # 自動生成される情報
        self.speaking_style = get_speaking_style(self.age)
    
    def _generate_age(self, age_range):
        """年齢範囲から具体的な年齢を生成"""
        if age_range in AGE_OPTIONS:
            return AGE_OPTIONS[age_range]["center"]
        return 50  # デフォルト
    
    def _generate_family_detail(self, family_structure):
        """家族構成から詳細を生成"""
        if family_structure in FAMILY_DETAILS:
            options = FAMILY_DETAILS[family_structure]
            return random.choice(options)
        return ""
    
    def get_location_full(self):
        """完全な居住地を取得"""
        if self.location_area == "東京23区":
            return f"東京都{self.location_detail}"
        else:
            return f"{self.location_area} {self.location_detail}"
    
    def get_hobbies_text(self):
        """趣味をテキスト形式で取得"""
        if len(self.hobbies) <= 2:
            return "、".join(self.hobbies)
        else:
            return "、".join(self.hobbies[:2]) + f"など{len(self.hobbies)}つ"
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            "age": self.age,
            "age_range": self.age_range,
            "location": self.get_location_full(),
            "location_area": self.location_area,
            "location_detail": self.location_detail,
            "family_structure": self.family_structure,
            "family_detail": self.family_detail,
            "hobbies": self.hobbies,
            "hobbies_text": self.get_hobbies_text(),
            "personality_type": self.personality_type,
            "gender": self.gender,
            "speaking_style": self.speaking_style
        }
    
    def get_summary(self):
        """プロフィールサマリー"""
        return f"""{self.age}歳女性、{self.get_location_full()}在住。
{self.family_structure}（{self.family_detail}）。
趣味は{self.get_hobbies_text()}。
性格タイプは{self.personality_type}型。"""
    
    def get_prompt_text(self):
        """プロンプト用のテキスト"""
        return f"""- 年齢: {self.age}歳（{self.age_range}）
- 居住地: {self.get_location_full()}
- 家族: {self.family_structure}（{self.family_detail}）
- 趣味・興味: {", ".join(self.hobbies)}
- 性格タイプ: {self.personality_type}型
- 話し方: {self.speaking_style}"""


class ManProfile:
    """A（男性）のプロフィール"""
    
    def __init__(self, personality_type="INTJ"):
        self.personality_type = personality_type
        self.gender = "男性"
        self.name = "あなた"
    
    def to_dict(self):
        """辞書形式に変換"""
        return {
            "personality_type": self.personality_type,
            "gender": self.gender
        }
    
    def get_summary(self):
        """プロフィールサマリー"""
        return f"性格タイプ: {self.personality_type}型"
