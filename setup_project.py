import os
from pathlib import Path

def create_directory_structure():
    directories = [
        "data/raw",
        "data/processed",
        "data/vectorstore",
        "src/scraper",
        "src/rag",
        "src/agent",
        "src/models",
        "src/ui",
        "src/utils",
        "notebooks",
        "tests",
        "config"
    ]
    
    print("📁 ディレクトリを作成中...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    print("\n✨ ディレクトリ構造の作成完了！")

def create_init_files():
    init_locations = [
        "src/__init__.py",
        "src/scraper/__init__.py",
        "src/rag/__init__.py",
        "src/agent/__init__.py",
        "src/models/__init__.py",
        "src/ui/__init__.py",
        "src/utils/__init__.py",
    ]
    
    print("\n📝 __init__.pyファイルを作成中...")
    for init_file in init_locations:
        Path(init_file).touch(exist_ok=True)
        print(f"   ✅ {init_file}")
    
    print("\n✨ __init__.pyファイルの作成完了！")

def main():
    print("=" * 60)
    print("🚀 Personality Chat System - プロジェクトセットアップ")
    print("=" * 60)
    
    create_directory_structure()
    create_init_files()
    
    print("\n" + "=" * 60)
    print("✅ セットアップ完了！")
    print("=" * 60)

if __name__ == "__main__":
    main()
