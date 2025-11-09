# 出会い系サイト向けチャットプログラム 仕様書

## 1. システム概要

### 1.1 目的
50歳以上の男女向け出会い系サイトのチャットシステム

### 1.2 技術スタック
- **バックエンド**: Python
- **データベース**: 🔷[LLM提案] PostgreSQL または MySQL
- **リアルタイム通信**: 🔷[LLM提案] WebSocket (Socket.IO推奨)
- **将来拡張**: LangChain、RAG、LangGraph、AIエージェント連携

---

## 2. ユーザー要件

### 2.1 対象ユーザー
- 年齢層: 50歳以上
- UI/UXの配慮事項:
  - 🔷[LLM提案] 大きめのフォントサイズ (最低16px以上)
  - 🔷[LLM提案] 明確でわかりやすいボタンデザイン
  - 🔷[LLM提案] シンプルな画面構成
  - 🔷[LLM提案] 高コントラスト配色

---

## 3. 機能仕様

### 3.1 ユーザー登録機能

#### 3.1.1 初期登録
**画面**: ユーザー登録画面

**入力項目**:
- メールアドレス (会員IDとして使用)
- 🔷[LLM提案] パスワード (セキュリティ要件: 8文字以上、英数字記号含む)
- 🔷[LLM提案] パスワード確認

**処理フロー**:
1. メールアドレス形式のバリデーション
2. 🔷[LLM提案] メールアドレス重複チェック
3. 🔷[LLM提案] 認証メール送信
4. 🔷[LLM提案] メールリンククリックで本登録完了
5. ユーザーテーブルへの登録

**DB項目 (usersテーブル)**:
```
- user_id (UUID, PRIMARY KEY)
- email (VARCHAR, UNIQUE, NOT NULL)
- password_hash (VARCHAR, NOT NULL)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- is_verified (BOOLEAN, DEFAULT FALSE)
- last_login (TIMESTAMP)
```

---

### 3.2 会員プロフィール登録機能

#### 3.2.1 プロフィール項目

**必須項目**:
1. 会員ID (メールアドレス) - 自動設定
2. ニックネーム (20文字以内)
3. 🔷[LLM提案] 性別 (男性/女性/その他)
4. 生年月日
5. 職業 (ドロップダウン選択 + 自由入力)
6. 住所 (都道府県のみ)
7. 自己紹介文 (200文字以内)
8. アイコン画像 (推奨サイズ: 200x200px)

**🔷[LLM提案] 任意項目**:
9. 身長 (cm)
10. 体型 (選択式: スリム/普通/がっちり/ぽっちゃり)
11. 喫煙 (吸わない/吸う/時々吸う)
12. 飲酒 (飲まない/飲む/時々飲む)
13. 趣味・興味 (タグ選択式、最大10個)
14. 希望する相手の年齢層 (範囲指定)
15. 希望する相手の居住地 (複数都道府県選択可)

**DB項目 (profilesテーブル)**:
```
- profile_id (UUID, PRIMARY KEY)
- user_id (UUID, FOREIGN KEY)
- nickname (VARCHAR(20), NOT NULL)
- gender (ENUM, NOT NULL)
- birth_date (DATE, NOT NULL)
- occupation (VARCHAR(100))
- prefecture (VARCHAR(20))
- self_introduction (TEXT(200))
- icon_image_url (VARCHAR)
- height (INT)
- body_type (ENUM)
- smoking (ENUM)
- drinking (ENUM)
- hobbies (JSON)
- preferred_age_min (INT)
- preferred_age_max (INT)
- preferred_prefectures (JSON)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

---

### 3.3 チャット相手一覧機能

#### 3.3.1 表示仕様
**画面**: チャット相手一覧画面

**表示条件**:
- 男性ユーザー: 女性プロフィール一覧を表示
- 女性ユーザー: 男性プロフィール一覧を表示
- 🔷[LLM提案] 自分のプロフィール設定に基づくフィルタリング機能

**一覧表示項目**:
- アイコン画像 (未登録時はデフォルト画像)
- ニックネーム
- 🔷[LLM提案] 年齢
- 🔷[LLM提案] 居住地(都道府県)
- 🔷[LLM提案] オンライン状態インジケーター (緑: オンライン、灰色: オフライン)
- 🔷[LLM提案] 最終ログイン時刻 (24時間以内の場合表示)

**ソート・フィルター機能** 🔷[LLM提案]:
- 新着順
- 年齢順
- 最終ログイン順
- 居住地フィルター
- 年齢範囲フィルター

**ページネーション**: 🔷[LLM提案] 20件/ページ

**インタラクション**:
- アイコン画像クリック → ユーザー詳細画面へ遷移

---

### 3.4 ユーザー詳細画面

#### 3.4.1 表示内容
**画面**: ユーザー詳細画面

**表示項目**:
- 全プロフィール情報
- 🔷[LLM提案] プロフィール閲覧日時の記録

**アクション**:
1. **対話リクエストボタン**
   - クリックでチャット相手にリクエスト通知
   - 🔷[LLM提案] リクエスト送信済みの場合は「リクエスト送信済み」表示
   
2. 🔷[LLM提案] **ブロックボタン**
   - 特定ユーザーをブロック
   - ブロックしたユーザーは一覧に表示されない
   
3. 🔷[LLM提案] **通報ボタン**
   - 不適切なユーザーを運営に通報

**DB項目 (profile_viewsテーブル)** 🔷[LLM提案]:
```
- view_id (UUID, PRIMARY KEY)
- viewer_user_id (UUID, FOREIGN KEY)
- viewed_user_id (UUID, FOREIGN KEY)
- viewed_at (TIMESTAMP)
```

**DB項目 (chat_requestsテーブル)**:
```
- request_id (UUID, PRIMARY KEY)
- requester_user_id (UUID, FOREIGN KEY)
- recipient_user_id (UUID, FOREIGN KEY)
- status (ENUM: pending/accepted/rejected)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

**DB項目 (blocked_usersテーブル)** 🔷[LLM提案]:
```
- block_id (UUID, PRIMARY KEY)
- blocker_user_id (UUID, FOREIGN KEY)
- blocked_user_id (UUID, FOREIGN KEY)
- created_at (TIMESTAMP)
```

---

### 3.5 マイページ機能

#### 3.5.1 マイページメニュー
**画面**: マイページ

**リンク項目**:

1. **プロフィール閲覧者一覧**
   - 自分のプロフィールを見たユーザー一覧
   - 表示: アイコン画像、ニックネーム、閲覧日時 🔷[LLM提案]
   - クリック → ユーザー詳細画面へ遷移

2. **チャットリクエスト受信一覧**
   - 対話リクエストを送ってきたユーザー一覧
   - 表示: アイコン画像、ニックネーム、リクエスト日時 🔷[LLM提案]
   - クリック → ユーザー詳細画面へ遷移(特別版)
   - **ユーザー詳細画面に「チャットを始める」ボタン表示**
   - ボタンクリック → チャット画面へ遷移

3. **プロフィール編集**
   - 会員プロフィール登録/修正ページへ遷移

4. 🔷[LLM提案] **チャット履歴一覧**
   - 過去にチャットしたユーザー一覧
   - 最終メッセージ日時、未読件数表示
   - クリック → チャット画面へ遷移

5. 🔷[LLM提案] **お気に入りリスト**
   - お気に入り登録したユーザー一覧

6. 🔷[LLM提案] **ブロックリスト管理**
   - ブロックしたユーザーの管理・解除

7. 🔷[LLM提案] **通知設定**
   - メール通知ON/OFF
   - プッシュ通知設定

8. 🔷[LLM提案] **アカウント設定**
   - パスワード変更
   - メールアドレス変更
   - アカウント削除

---

### 3.6 チャット画面

#### 3.6.1 画面構成
**画面**: チャット画面 (LINEライク)

**レイアウト**:
```
+----------------------------------+
|   ← [相手のニックネーム] 🔷[オンライン状態]  |
+----------------------------------+
|                                  |
|  [相手のメッセージ]               |
|  └ 10:30                         |
|                                  |
|              [自分のメッセージ]    |
|                         10:31 ┘  |
|                                  |
|  [相手のメッセージ]               |
|  └ 10:32                         |
|                                  |
+----------------------------------+
| [メッセージ入力欄]        [送信📤] |
+----------------------------------+
```

**機能要件**:

1. **メッセージ表示**
   - 自分のメッセージ: 右寄せ、背景色(例: 青系)
   - 相手のメッセージ: 左寄せ、背景色(例: 灰色系)
   - タイムスタンプ表示(時:分)
   - 🔷[LLM提案] 既読/未読表示
   - 🔷[LLM提案] 日付セパレーター(日付が変わったら表示)

2. **メッセージ入力**
   - 入力欄: テキストエリア(複数行対応) 🔷[LLM提案]
   - 送信ボタン: 紙飛行機アイコン📤
   - 🔷[LLM提案] Enterキーで送信、Shift+Enterで改行
   - 🔷[LLM提案] 文字数カウンター表示(最大1000文字)

3. **リアルタイム通信**
   - WebSocketによるリアルタイムメッセージング 🔷[LLM提案]
   - 🔷[LLM提案] 相手が入力中インジケーター表示「...」
   - 🔷[LLM提案] 自動スクロール(新メッセージ受信時)

4. **追加機能** 🔷[LLM提案]
   - 画像送信機能
   - スタンプ機能(年齢層に合わせたもの)
   - メッセージ削除機能(自分のメッセージのみ)

**DB項目 (messagesテーブル)**:
```
- message_id (UUID, PRIMARY KEY)
- chat_room_id (UUID, FOREIGN KEY)
- sender_user_id (UUID, FOREIGN KEY)
- message_text (TEXT(1000))
- message_type (ENUM: text/image/stamp)
- image_url (VARCHAR, NULL)
- is_read (BOOLEAN, DEFAULT FALSE)
- read_at (TIMESTAMP, NULL)
- created_at (TIMESTAMP)
- deleted_at (TIMESTAMP, NULL)
```

**DB項目 (chat_roomsテーブル)** 🔷[LLM提案]:
```
- chat_room_id (UUID, PRIMARY KEY)
- user1_id (UUID, FOREIGN KEY)
- user2_id (UUID, FOREIGN KEY)
- created_at (TIMESTAMP)
- last_message_at (TIMESTAMP)
```

---

## 4. セキュリティ要件 🔷[LLM提案]

### 4.1 認証・認可
- JWT (JSON Web Token) による認証
- セッション管理
- CSRF対策
- XSS対策

### 4.2 データ保護
- パスワードのハッシュ化 (bcrypt推奨)
- HTTPS通信必須
- 個人情報の暗号化

### 4.3 プライバシー保護
- プロフィール公開範囲設定
- 位置情報の厳密な管理(都道府県レベルまで)
- メッセージの暗号化通信

### 4.4 不正利用対策
- レート制限(API呼び出し回数制限)
- スパム対策
- 通報システム
- 自動監視システム(AI連携予定)

---

## 5. 非機能要件 🔷[LLM提案]

### 5.1 パフォーマンス
- ページ読み込み時間: 3秒以内
- メッセージ送信遅延: 1秒以内
- 同時接続ユーザー数: 1000人以上

### 5.2 スケーラビリティ
- 水平スケーリング対応
- データベースレプリケーション
- CDN活用(画像配信)

### 5.3 可用性
- 稼働率: 99.9%以上
- バックアップ: 日次自動バックアップ
- 災害復旧計画

---

## 6. 将来拡張計画

### 6.1 AI連携機能
以下の技術との連携を想定:
- **LangChain**: 自然言語処理
- **RAG**: コンテキスト保持会話
- **LangGraph**: 複雑な会話フロー管理
- **AIエージェント**: 
  - 🔷[LLM提案] AIマッチング支援
  - 🔷[LLM提案] 会話サポート(話題提案)
  - 🔷[LLM提案] プロフィール最適化提案
  - 🔷[LLM提案] 不適切コンテンツの自動検出

### 6.2 追加機能案 🔷[LLM提案]
- ビデオ通話機能
- グループチャット
- イベント機能(オフ会など)
- ポイント制課金システム
- マッチング度アルゴリズム

---

## 7. 開発フェーズ

### Phase 1: MVP (最小限の機能)
- ユーザー登録・認証
- プロフィール登録
- 一覧表示
- 基本チャット機能

### Phase 2: 機能拡充
- リアルタイムチャット
- 通知機能
- プロフィール閲覧履歴
- ブロック・通報機能

### Phase 3: AI連携
- LangChain統合
- RAG実装
- AIマッチング機能

---

## 8. 技術アーキテクチャ 🔷[LLM提案]

### 8.1 推奨構成
```
フロントエンド: React / Vue.js
バックエンド: FastAPI (Python)
データベース: PostgreSQL
リアルタイム通信: Socket.IO
キャッシュ: Redis
ファイルストレージ: AWS S3 / Google Cloud Storage
デプロイ: Docker + Kubernetes
```

### 8.2 ディレクトリ構成例
```
project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── websocket/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
└── docker-compose.yml
```

---

## 9. データベース ER図概要 🔷[LLM提案]

```
users (1) ---- (1) profiles
  |
  |─── (N) profile_views (N) ───|
  |                              |
  |─── (N) chat_requests (N) ───|
  |                              |
  |─── (N) blocked_users (N) ───|
  |                              |
  |─── (N) chat_rooms (N) ──────|
        |
        └─── (N) messages
```

---

## 10. 補足事項

### 10.1 アクセシビリティ 🔷[LLM提案]
50歳以上のユーザー向けに以下を考慮:
- フォントサイズ調整機能
- 高コントラストモード
- 音声読み上げ対応
- キーボードナビゲーション

### 10.2 法的対応 🔷[LLM提案]
- 利用規約
- プライバシーポリシー
- 特定商取引法に基づく表記
- 年齢確認機能(18歳未満利用不可)

---

**凡例**: 🔷[LLM提案] = AIによる提案項目

**作成日**: 2025年11月9日
**バージョン**: 1.0
