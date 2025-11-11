"""
Personality Chat System - メイン実行スクリプト
"""
import subprocess
import sys
from pathlib import Path

def check_environment():
    print("=== 環境確認 ===\n")
    if not Path(".env").exists():
        print("✗ .envファイルが見つかりません")
        return False
    print("✓ .envファイル: OK")
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/vectorstore").mkdir(parents=True, exist_ok=True)
    print("✓ ディレクトリ: OK")
    return True

def run_scraper():
    print("\n" + "="*60)
    print("Step 1: 性格データを取得中...")
    print("="*60 + "\n")
    try:
        subprocess.run([sys.executable, "personality_scraper.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("\n✗ スクレイピングに失敗しました")
        return False

def run_rag_builder():
    print("\n" + "="*60)
    print("Step 2: RAGシステムを構築中...")
    print("="*60 + "\n")
    try:
        subprocess.run([sys.executable, "build_rag.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("\n✗ RAG構築に失敗しました")
        return False

def run_streamlit():
    print("\n" + "="*60)
    print("Step 3: Webアプリを起動中...")
    print("="*60 + "\n")
    print("🌐 ブラウザで以下のURLが開きます:")
    print("   http://localhost:8501")
    print("\n⏹  終了するには Ctrl+C を押してください\n")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "chat_app.py", "--server.headless", "true"])
    except KeyboardInterrupt:
        print("\n\n✓ アプリを終了しました")

def main():
    print("="*60)
    print(" 🚀 Personality Chat System - セットアップ & 起動")
    print("="*60)
    if not check_environment():
        return
    vectorstore_exists = Path("data/vectorstore").exists() and list(Path("data/vectorstore").glob("*"))
    if not vectorstore_exists:
        print("\n💡 初回セットアップが必要です\n")
        if not run_scraper():
            return
        if not run_rag_builder():
            return
    else:
        print("\n✓ データは既に準備済みです")
    run_streamlit()

if __name__ == "__main__":
    main()
