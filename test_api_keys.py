import os
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    print("\n🔍 OpenAI API テスト...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=10
        )
        print("✅ OpenAI API: 正常に動作しています")
        return True
    except Exception as e:
        print(f"❌ OpenAI API: エラー - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🔑 Personality Chat System - API動作確認")
    print("=" * 60)
    
    print("\n📋 環境変数の確認...")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY: 設定済み ({api_key[:20]}...)")
    else:
        print("❌ OPENAI_API_KEY: 未設定")
    
    test_openai()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
