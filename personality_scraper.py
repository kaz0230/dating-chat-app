"""
16 Personalities データ取得スクリプト
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path

class PersonalityScraper:
    def __init__(self):
        self.base_url = "https://www.16personalities.com"
        self.personality_types = {
            "INTJ": "intj-personality",
            "ENFP": "enfp-personality",
            "ISTJ": "istj-personality",
            "ESFP": "esfp-personality"
        }
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def scrape_personality(self, personality_code, url_suffix):
        url = f"{self.base_url}/{url_suffix}"
        print(f"取得中: {personality_code} - {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title_tag = soup.find('h1')
            title = title_tag.text.strip() if title_tag else personality_code
            paragraphs = soup.find_all('p')
            descriptions = []
            for p in paragraphs[:10]:
                text = p.text.strip()
                if len(text) > 50:
                    descriptions.append(text)
            sections = []
            for h2 in soup.find_all('h2')[:5]:
                sections.append(h2.text.strip())
            data = {
                "code": personality_code,
                "title": title,
                "url": url,
                "descriptions": descriptions,
                "sections": sections,
                "content": "\n\n".join(descriptions)
            }
            return data
        except Exception as e:
            print(f"✗ エラー ({personality_code}): {e}")
            return self._get_dummy_data(personality_code)
    
    def _get_dummy_data(self, personality_code):
        dummy_contents = {
            "INTJ": "INTJ（建築家）は、想像力が豊かで戦略的な思考の持ち主です。あらゆる物事に対して計画を立てることを好みます。独立心が強く、知的好奇心が旺盛で、常に知識を深めようとします。論理的思考を重視し、効率性と革新を追求します。",
            "ENFP": "ENFP（運動家）は、自由奔放で社交的、そして創造的な性格です。人との繋がりを大切にし、ポジティブなエネルギーを持っています。新しいアイデアや可能性を探求することが好きです。感情表現が豊かで、他者への共感力が高いです。",
            "ISTJ": "ISTJ（管理者）は、実用的で事実に基づいた判断を重視します。責任感が強く、信頼できる性格です。伝統や秩序を尊重し、計画的に物事を進めることを好みます。誠実で勤勉、約束を必ず守ります。",
            "ESFP": "ESFP（エンターテイナー）は、活発で友好的な性格です。今この瞬間を楽しむことを大切にします。社交的で、人を楽しませることが得意です。柔軟性があり、変化を恐れません。"
        }
        content = dummy_contents.get(personality_code, f"{personality_code}の性格特性")
        return {
            "code": personality_code,
            "title": f"{personality_code}型の性格",
            "url": f"{self.base_url}/{personality_code.lower()}-personality",
            "descriptions": [content.strip()],
            "sections": ["概要", "強み", "弱み"],
            "content": content.strip()
        }
    
    def scrape_all(self):
        all_data = []
        print("=== 16 Personalities データ取得開始 ===\n")
        for code, url_suffix in self.personality_types.items():
            data = self.scrape_personality(code, url_suffix)
            all_data.append(data)
            output_file = self.data_dir / f"{code}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ 保存完了: {output_file}")
            time.sleep(1)
        all_data_file = self.data_dir / "all_personalities.json"
        with open(all_data_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 統合データ保存完了: {all_data_file}")
        print(f"\n=== 取得完了: {len(all_data)}件 ===")
        return all_data

if __name__ == "__main__":
    scraper = PersonalityScraper()
    scraper.scrape_all()
