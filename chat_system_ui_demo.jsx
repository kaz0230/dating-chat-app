import React, { useState } from 'react';
import { MessageCircle, Heart, User, Home, Settings, Send, Image, Search, Filter, Bell, Shield, LogOut } from 'lucide-react';

const ChatSystemDemo = () => {
  const [activeScreen, setActiveScreen] = useState('login');
  const [messages, setMessages] = useState([
    { id: 1, sender: 'other', text: 'こんにちは!プロフィール拝見しました。', time: '10:30' },
    { id: 2, sender: 'me', text: 'ありがとうございます!よろしくお願いします。', time: '10:31' },
    { id: 3, sender: 'other', text: 'お住まいはどちらですか?', time: '10:32' },
  ]);
  const [newMessage, setNewMessage] = useState('');

  // サンプルユーザーデータ
  const sampleUsers = [
    { id: 1, name: 'さくら', age: 55, location: '東京都', online: true, avatar: '🌸' },
    { id: 2, name: 'ひまわり', age: 52, location: '神奈川県', online: false, avatar: '🌻' },
    { id: 3, name: 'ゆり', age: 58, location: '千葉県', online: true, avatar: '🌺' },
    { id: 4, name: 'あやめ', age: 60, location: '埼玉県', online: false, avatar: '🌷' },
    { id: 5, name: 'すみれ', age: 54, location: '大阪府', online: true, avatar: '🌼' },
  ];

  const profileViewers = [
    { id: 1, name: 'さくら', age: 55, avatar: '🌸', viewedAt: '2時間前' },
    { id: 2, name: 'すみれ', age: 54, avatar: '🌼', viewedAt: '5時間前' },
  ];

  const chatRequests = [
    { id: 1, name: 'ひまわり', age: 52, avatar: '🌻', requestedAt: '1日前' },
    { id: 3, name: 'ゆり', age: 58, avatar: '🌺', requestedAt: '3日前' },
  ];

  const sendMessage = () => {
    if (newMessage.trim()) {
      setMessages([...messages, {
        id: messages.length + 1,
        sender: 'me',
        text: newMessage,
        time: new Date().toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' })
      }]);
      setNewMessage('');
    }
  };

  // ナビゲーションバー
  const NavBar = ({ title }) => (
    <div className="bg-pink-500 text-white p-4 shadow-md">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <h1 className="text-2xl font-bold">{title}</h1>
        <div className="flex gap-3">
          <Bell className="w-7 h-7 cursor-pointer hover:scale-110 transition" />
          <User className="w-7 h-7 cursor-pointer hover:scale-110 transition" />
        </div>
      </div>
    </div>
  );

  // 画面選択メニュー
  const ScreenSelector = () => (
    <div className="bg-gray-100 p-4 border-b-2">
      <div className="max-w-4xl mx-auto">
        <h3 className="text-lg font-bold mb-3">画面を選択:</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {[
            { id: 'login', label: 'ログイン画面' },
            { id: 'register', label: 'ユーザー登録' },
            { id: 'profile', label: 'プロフィール登録' },
            { id: 'list', label: 'お相手一覧' },
            { id: 'detail', label: 'お相手詳細' },
            { id: 'mypage', label: 'マイページ' },
            { id: 'chat', label: 'チャット画面' },
          ].map(screen => (
            <button
              key={screen.id}
              onClick={() => setActiveScreen(screen.id)}
              className={`p-3 rounded-lg font-bold text-base transition ${
                activeScreen === screen.id
                  ? 'bg-pink-500 text-white'
                  : 'bg-white hover:bg-pink-100'
              }`}
            >
              {screen.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );

  // 1. ログイン画面
  const LoginScreen = () => (
    <div className="min-h-screen bg-gradient-to-b from-pink-100 to-white flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <Heart className="w-20 h-20 text-pink-500 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-800 mb-2">ハートフルマッチ</h1>
          <p className="text-lg text-gray-600">素敵な出会いがここに</p>
        </div>
        
        <div className="space-y-5">
          <div>
            <label className="block text-lg font-bold text-gray-700 mb-2">メールアドレス</label>
            <input
              type="email"
              className="w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
              placeholder="example@email.com"
            />
          </div>
          
          <div>
            <label className="block text-lg font-bold text-gray-700 mb-2">パスワード</label>
            <input
              type="password"
              className="w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
              placeholder="パスワードを入力"
            />
          </div>
          
          <button className="w-full bg-pink-500 hover:bg-pink-600 text-white font-bold text-xl py-4 rounded-lg transition shadow-lg">
            ログイン
          </button>
          
          <div className="text-center">
            <a href="#" className="text-pink-500 text-lg hover:underline">パスワードを忘れた方</a>
          </div>
          
          <hr className="my-6" />
          
          <button
            onClick={() => setActiveScreen('register')}
            className="w-full bg-white border-2 border-pink-500 text-pink-500 hover:bg-pink-50 font-bold text-xl py-4 rounded-lg transition"
          >
            新規会員登録
          </button>
        </div>
      </div>
    </div>
  );

  // 2. ユーザー登録画面
  const RegisterScreen = () => (
    <div className="min-h-screen bg-gray-50">
      <NavBar title="会員登録" />
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">新規会員登録</h2>
          
          <div className="space-y-5">
            <div>
              <label className="block text-lg font-bold text-gray-700 mb-2">メールアドレス<span className="text-red-500">*</span></label>
              <input
                type="email"
                className="w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                placeholder="example@email.com"
              />
              <p className="text-sm text-gray-500 mt-1">このメールアドレスが会員IDになります</p>
            </div>
            
            <div>
              <label className="block text-lg font-bold text-gray-700 mb-2">パスワード<span className="text-red-500">*</span></label>
              <input
                type="password"
                className="w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                placeholder="8文字以上の英数字"
              />
              <p className="text-sm text-gray-500 mt-1">8文字以上、英数字を含めてください</p>
            </div>
            
            <div>
              <label className="block text-lg font-bold text-gray-700 mb-2">パスワード確認<span className="text-red-500">*</span></label>
              <input
                type="password"
                className="w-full p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                placeholder="もう一度入力してください"
              />
            </div>
            
            <div className="bg-pink-50 p-4 rounded-lg border border-pink-200">
              <p className="text-base text-gray-700">
                登録ボタンを押すと、確認メールが送信されます。<br />
                メール内のリンクをクリックして登録を完了してください。
              </p>
            </div>
            
            <button className="w-full bg-pink-500 hover:bg-pink-600 text-white font-bold text-xl py-4 rounded-lg transition shadow-lg">
              登録する
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  // 3. プロフィール登録画面
  const ProfileScreen = () => (
    <div className="min-h-screen bg-gray-50">
      <NavBar title="プロフィール登録" />
      <div className="max-w-3xl mx-auto p-6">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">プロフィールを作成</h2>
          
          <div className="space-y-6">
            {/* アイコン画像 */}
            <div className="text-center">
              <div className="w-32 h-32 bg-gray-200 rounded-full mx-auto mb-3 flex items-center justify-center text-6xl">
                👤
              </div>
              <button className="bg-pink-500 hover:bg-pink-600 text-white font-bold px-6 py-3 rounded-lg text-lg">
                写真をアップロード
              </button>
              <p className="text-sm text-gray-500 mt-2">推奨サイズ: 200x200px</p>
            </div>
            
            <hr />
            
            {/* 基本情報 */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="block text-lg font-bold text-gray-700 mb-2">ニックネーム<span className="text-red-500">*</span></label>
                <input
                  type="text"
                  className="w-full p-3 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  placeholder="20文字以内"
                  maxLength="20"
                />
              </div>
              
              <div>
                <label className="block text-lg font-bold text-gray-700 mb-2">性別<span className="text-red-500">*</span></label>
                <select className="w-full p-3 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none">
                  <option>選択してください</option>
                  <option>男性</option>
                  <option>女性</option>
                  <option>その他</option>
                </select>
              </div>
              
              <div>
                <label className="block text-lg font-bold text-gray-700 mb-2">生年月日<span className="text-red-500">*</span></label>
                <input
                  type="date"
                  className="w-full p-3 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                />
              </div>
              
              <div>
                <label className="block text-lg font-bold text-gray-700 mb-2">職業<span className="text-red-500">*</span></label>
                <select className="w-full p-3 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none">
                  <option>選択してください</option>
                  <option>会社員</option>
                  <option>公務員</option>
                  <option>自営業</option>
                  <option>退職済み</option>
                  <option>その他</option>
                </select>
              </div>
              
              <div>
                <label className="block text-lg font-bold text-gray-700 mb-2">お住まい<span className="text-red-500">*</span></label>
                <select className="w-full p-3 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none">
                  <option>選択してください</option>
                  <option>東京都</option>
                  <option>神奈川県</option>
                  <option>千葉県</option>
                  <option>埼玉県</option>
                  <option>大阪府</option>
                  {/* 他の都道府県 */}
                </select>
              </div>
              
              <div>
                <label className="block text-lg font-bold text-gray-700 mb-2">身長</label>
                <input
                  type="number"
                  className="w-full p-3 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                  placeholder="cm"
                />
              </div>
            </div>
            
            {/* 自己紹介 */}
            <div>
              <label className="block text-lg font-bold text-gray-700 mb-2">自己紹介<span className="text-red-500">*</span></label>
              <textarea
                className="w-full p-3 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none h-32"
                placeholder="あなたの魅力をアピールしてください(200文字以内)"
                maxLength="200"
              ></textarea>
              <p className="text-sm text-gray-500 mt-1 text-right">0/200文字</p>
            </div>
            
            <button className="w-full bg-pink-500 hover:bg-pink-600 text-white font-bold text-xl py-4 rounded-lg transition shadow-lg">
              プロフィールを保存
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  // 4. お相手一覧画面
  const ListScreen = () => (
    <div className="min-h-screen bg-gray-50">
      <NavBar title="お相手を探す" />
      
      {/* 検索・フィルター */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-4xl mx-auto p-4">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                className="w-full p-3 pl-12 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
                placeholder="ニックネームで検索"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-6 h-6" />
            </div>
            <button className="bg-pink-500 hover:bg-pink-600 text-white font-bold px-6 py-3 rounded-lg flex items-center gap-2 text-lg">
              <Filter className="w-5 h-5" />
              絞り込み
            </button>
          </div>
        </div>
      </div>
      
      {/* ユーザー一覧 */}
      <div className="max-w-4xl mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {sampleUsers.map(user => (
            <div
              key={user.id}
              onClick={() => setActiveScreen('detail')}
              className="bg-white rounded-xl shadow-md hover:shadow-xl transition cursor-pointer p-5"
            >
              <div className="flex items-center gap-4">
                <div className="relative">
                  <div className="w-24 h-24 bg-gradient-to-br from-pink-200 to-purple-200 rounded-full flex items-center justify-center text-5xl">
                    {user.avatar}
                  </div>
                  {user.online && (
                    <div className="absolute bottom-0 right-0 w-6 h-6 bg-green-500 border-4 border-white rounded-full"></div>
                  )}
                </div>
                
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-800 mb-1">{user.name}</h3>
                  <p className="text-lg text-gray-600">{user.age}歳 • {user.location}</p>
                  <div className="flex items-center gap-2 mt-2">
                    {user.online ? (
                      <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">オンライン</span>
                    ) : (
                      <span className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm">オフライン</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* ページネーション */}
        <div className="flex justify-center gap-2 mt-8">
          <button className="px-5 py-3 bg-white border-2 border-gray-300 rounded-lg font-bold text-lg hover:bg-gray-50">前へ</button>
          <button className="px-5 py-3 bg-pink-500 text-white rounded-lg font-bold text-lg">1</button>
          <button className="px-5 py-3 bg-white border-2 border-gray-300 rounded-lg font-bold text-lg hover:bg-gray-50">2</button>
          <button className="px-5 py-3 bg-white border-2 border-gray-300 rounded-lg font-bold text-lg hover:bg-gray-50">3</button>
          <button className="px-5 py-3 bg-white border-2 border-gray-300 rounded-lg font-bold text-lg hover:bg-gray-50">次へ</button>
        </div>
      </div>
    </div>
  );

  // 5. お相手詳細画面
  const DetailScreen = () => (
    <div className="min-h-screen bg-gray-50">
      <NavBar title="プロフィール詳細" />
      
      <div className="max-w-3xl mx-auto p-6">
        <div className="bg-white rounded-xl shadow-lg p-8">
          {/* プロフィール画像とメイン情報 */}
          <div className="text-center mb-8">
            <div className="w-40 h-40 bg-gradient-to-br from-pink-200 to-purple-200 rounded-full flex items-center justify-center text-8xl mx-auto mb-4">
              🌸
            </div>
            <div className="flex items-center justify-center gap-2 mb-2">
              <h2 className="text-3xl font-bold text-gray-800">さくら</h2>
              <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-base font-bold">オンライン</span>
            </div>
            <p className="text-xl text-gray-600">55歳 • 東京都</p>
          </div>
          
          {/* 詳細情報 */}
          <div className="space-y-5 mb-8">
            <div className="border-l-4 border-pink-500 pl-4">
              <h3 className="text-lg font-bold text-gray-700 mb-1">職業</h3>
              <p className="text-xl text-gray-800">会社員</p>
            </div>
            
            <div className="border-l-4 border-pink-500 pl-4">
              <h3 className="text-lg font-bold text-gray-700 mb-1">身長</h3>
              <p className="text-xl text-gray-800">160cm</p>
            </div>
            
            <div className="border-l-4 border-pink-500 pl-4">
              <h3 className="text-lg font-bold text-gray-700 mb-1">趣味</h3>
              <div className="flex flex-wrap gap-2 mt-2">
                <span className="bg-pink-100 text-pink-700 px-4 py-2 rounded-full text-base font-bold">旅行</span>
                <span className="bg-pink-100 text-pink-700 px-4 py-2 rounded-full text-base font-bold">料理</span>
                <span className="bg-pink-100 text-pink-700 px-4 py-2 rounded-full text-base font-bold">読書</span>
              </div>
            </div>
            
            <div className="border-l-4 border-pink-500 pl-4">
              <h3 className="text-lg font-bold text-gray-700 mb-2">自己紹介</h3>
              <p className="text-lg text-gray-800 leading-relaxed">
                はじめまして!趣味は旅行と料理です。週末は美味しいものを食べに出かけるのが好きです。
                一緒に楽しい時間を過ごせる方と出会えたら嬉しいです。よろしくお願いします。
              </p>
            </div>
          </div>
          
          {/* アクションボタン */}
          <div className="space-y-3">
            <button className="w-full bg-pink-500 hover:bg-pink-600 text-white font-bold text-xl py-4 rounded-lg transition shadow-lg flex items-center justify-center gap-2">
              <Heart className="w-6 h-6" />
              対話リクエストを送る
            </button>
            
            <div className="grid grid-cols-2 gap-3">
              <button className="bg-white border-2 border-gray-300 hover:bg-gray-50 text-gray-700 font-bold text-lg py-3 rounded-lg transition">
                お気に入り登録
              </button>
              <button className="bg-white border-2 border-red-300 hover:bg-red-50 text-red-600 font-bold text-lg py-3 rounded-lg transition flex items-center justify-center gap-2">
                <Shield className="w-5 h-5" />
                通報
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // 6. マイページ
  const MyPageScreen = () => (
    <div className="min-h-screen bg-gray-50">
      <NavBar title="マイページ" />
      
      <div className="max-w-4xl mx-auto p-6">
        {/* プロフィールカード */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex items-center gap-4">
            <div className="w-24 h-24 bg-gradient-to-br from-blue-200 to-purple-200 rounded-full flex items-center justify-center text-5xl">
              👤
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-800 mb-1">太郎</h2>
              <p className="text-lg text-gray-600">58歳 • 東京都</p>
            </div>
            <button
              onClick={() => setActiveScreen('profile')}
              className="bg-pink-500 hover:bg-pink-600 text-white font-bold px-6 py-3 rounded-lg text-lg"
            >
              プロフィール編集
            </button>
          </div>
        </div>
        
        {/* メニューグリッド */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* プロフィール閲覧者一覧 */}
          <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 cursor-pointer">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-800">プロフィール閲覧者</h3>
              <span className="bg-pink-500 text-white px-3 py-1 rounded-full text-base font-bold">{profileViewers.length}</span>
            </div>
            <div className="space-y-3">
              {profileViewers.slice(0, 2).map(user => (
                <div key={user.id} className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg">
                  <div className="w-14 h-14 bg-gradient-to-br from-pink-200 to-purple-200 rounded-full flex items-center justify-center text-3xl">
                    {user.avatar}
                  </div>
                  <div className="flex-1">
                    <p className="font-bold text-lg">{user.name}</p>
                    <p className="text-sm text-gray-500">{user.viewedAt}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* チャットリクエスト */}
          <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 cursor-pointer">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-800">チャットリクエスト</h3>
              <span className="bg-pink-500 text-white px-3 py-1 rounded-full text-base font-bold">{chatRequests.length}</span>
            </div>
            <div className="space-y-3">
              {chatRequests.slice(0, 2).map(user => (
                <div key={user.id} className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg">
                  <div className="w-14 h-14 bg-gradient-to-br from-pink-200 to-purple-200 rounded-full flex items-center justify-center text-3xl">
                    {user.avatar}
                  </div>
                  <div className="flex-1">
                    <p className="font-bold text-lg">{user.name}</p>
                    <p className="text-sm text-gray-500">{user.requestedAt}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* チャット履歴 */}
          <div
            onClick={() => setActiveScreen('chat')}
            className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 cursor-pointer"
          >
            <div className="flex items-center gap-4 mb-2">
              <MessageCircle className="w-10 h-10 text-pink-500" />
              <h3 className="text-xl font-bold text-gray-800">チャット履歴</h3>
            </div>
            <p className="text-base text-gray-600">過去の会話を確認できます</p>
          </div>
          
          {/* お気に入り */}
          <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 cursor-pointer">
            <div className="flex items-center gap-4 mb-2">
              <Heart className="w-10 h-10 text-pink-500" />
              <h3 className="text-xl font-bold text-gray-800">お気に入り</h3>
            </div>
            <p className="text-base text-gray-600">お気に入りの方を管理</p>
          </div>
          
          {/* 設定 */}
          <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 cursor-pointer">
            <div className="flex items-center gap-4 mb-2">
              <Settings className="w-10 h-10 text-pink-500" />
              <h3 className="text-xl font-bold text-gray-800">設定</h3>
            </div>
            <p className="text-base text-gray-600">通知・プライバシー設定</p>
          </div>
          
          {/* ログアウト */}
          <div
            onClick={() => setActiveScreen('login')}
            className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 cursor-pointer"
          >
            <div className="flex items-center gap-4 mb-2">
              <LogOut className="w-10 h-10 text-gray-500" />
              <h3 className="text-xl font-bold text-gray-800">ログアウト</h3>
            </div>
            <p className="text-base text-gray-600">安全にログアウト</p>
          </div>
        </div>
      </div>
    </div>
  );

  // 7. チャット画面
  const ChatScreen = () => (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* チャットヘッダー */}
      <div className="bg-pink-500 text-white p-4 shadow-md">
        <div className="max-w-4xl mx-auto flex items-center gap-4">
          <button
            onClick={() => setActiveScreen('mypage')}
            className="text-white hover:bg-pink-600 rounded-lg p-2"
          >
            ←
          </button>
          <div className="w-12 h-12 bg-gradient-to-br from-pink-200 to-purple-200 rounded-full flex items-center justify-center text-2xl">
            🌸
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold">さくら</h3>
            <p className="text-sm flex items-center gap-1">
              <span className="w-2 h-2 bg-green-400 rounded-full"></span>
              オンライン
            </p>
          </div>
        </div>
      </div>
      
      {/* メッセージエリア */}
      <div className="flex-1 overflow-y-auto p-4 bg-pink-50">
        <div className="max-w-4xl mx-auto space-y-4">
          {/* 日付セパレーター */}
          <div className="text-center">
            <span className="bg-white px-4 py-2 rounded-full text-sm text-gray-600 shadow">
              2025年11月9日
            </span>
          </div>
          
          {messages.map(msg => (
            <div key={msg.id} className={`flex ${msg.sender === 'me' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-md ${msg.sender === 'me' ? 'order-2' : 'order-1'}`}>
                <div className={`rounded-2xl p-4 shadow ${
                  msg.sender === 'me'
                    ? 'bg-pink-500 text-white rounded-br-none'
                    : 'bg-white text-gray-800 rounded-bl-none'
                }`}>
                  <p className="text-lg leading-relaxed">{msg.text}</p>
                </div>
                <p className={`text-xs text-gray-500 mt-1 ${msg.sender === 'me' ? 'text-right' : 'text-left'}`}>
                  {msg.time} {msg.sender === 'me' && '✓✓'}
                </p>
              </div>
            </div>
          ))}
          
          {/* 入力中インジケーター */}
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl rounded-bl-none p-4 shadow">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* 入力エリア */}
      <div className="bg-white border-t-2 border-gray-200 p-4">
        <div className="max-w-4xl mx-auto flex gap-3">
          <button className="bg-gray-100 hover:bg-gray-200 p-3 rounded-lg transition">
            <Image className="w-6 h-6 text-gray-600" />
          </button>
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            className="flex-1 p-4 text-lg border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none"
            placeholder="メッセージを入力..."
          />
          <button
            onClick={sendMessage}
            className="bg-pink-500 hover:bg-pink-600 text-white p-4 rounded-lg transition shadow-lg"
          >
            <Send className="w-6 h-6" />
          </button>
        </div>
        <p className="text-center text-sm text-gray-500 mt-2">
          {newMessage.length}/1000文字
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <ScreenSelector />
      
      {activeScreen === 'login' && <LoginScreen />}
      {activeScreen === 'register' && <RegisterScreen />}
      {activeScreen === 'profile' && <ProfileScreen />}
      {activeScreen === 'list' && <ListScreen />}
      {activeScreen === 'detail' && <DetailScreen />}
      {activeScreen === 'mypage' && <MyPageScreen />}
      {activeScreen === 'chat' && <ChatScreen />}
    </div>
  );
};

export default ChatSystemDemo;
