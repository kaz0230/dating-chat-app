"""
Personality Chat Simulator - メインアプリケーション
"""
import streamlit as st
from config import (
    AGE_OPTIONS, LOCATION_OPTIONS, FAMILY_OPTIONS,
    ALL_HOBBIES, PERSONALITY_OPTIONS
)
from profile_manager import WomanProfile, ManProfile
from woman_agent import WomanAgent
from hint_generator import HintGenerator

# ページ設定
st.set_page_config(
    page_title="Personality Chat Simulator",
    page_icon="💬",
    layout="wide"
)

# セッション状態の初期化
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_hint" not in st.session_state:
    st.session_state.current_hint = None
if "waiting_for_user" not in st.session_state:
    st.session_state.waiting_for_user = False

# タイトル
st.title("💬 Personality Chat Simulator")
st.markdown("**16 Personalities性格診断を活用したチャット対話シミュレーター**")

# サイドバー
with st.sidebar:
    st.header("⚙️ 設定")
    
    if not st.session_state.setup_complete:
        st.markdown("### 👨 A: あなた（男性）")
        man_personality = st.selectbox(
            "性格タイプ",
            options=list(PERSONALITY_OPTIONS.keys()),
            format_func=lambda x: PERSONALITY_OPTIONS[x],
            key="man_personality_select"
        )
        
        st.markdown("---")
        st.markdown("### 👩 B: 相手（女性）")
        
        # 年齢選択
        age_range = st.selectbox(
            "1️⃣ 年齢",
            options=list(AGE_OPTIONS.keys()),
            format_func=lambda x: AGE_OPTIONS[x]["display"],
            index=4,  # デフォルト: 50代前半
            key="age_select"
        )
        
        # 居住地選択（2段階）
        location_area = st.selectbox(
            "2️⃣ 居住地（エリア）",
            options=list(LOCATION_OPTIONS.keys()),
            index=0,  # デフォルト: 東京23区
            key="location_area_select"
        )
        
        location_detail = st.selectbox(
            "　　└ 詳細",
            options=LOCATION_OPTIONS[location_area],
            index=LOCATION_OPTIONS[location_area].index("杉並区") if "杉並区" in LOCATION_OPTIONS[location_area] else 0,
            key="location_detail_select"
        )
        
        # 家族構成選択
        family_structure = st.selectbox(
            "3️⃣ 家族構成",
            options=FAMILY_OPTIONS,
            index=0,  # デフォルト: 一人暮らし
            key="family_select"
        )
        
        # 趣味・興味選択
        st.markdown("4️⃣ 趣味・興味（複数選択可）")
        selected_hobbies = st.multiselect(
            "1〜5個選択してください",
            options=ALL_HOBBIES,
            default=["料理", "温泉"],
            max_selections=5,
            key="hobbies_select"
        )
        
        # 性格タイプ選択
        woman_personality = st.selectbox(
            "5️⃣ 性格タイプ",
            options=list(PERSONALITY_OPTIONS.keys()),
            format_func=lambda x: PERSONALITY_OPTIONS[x],
            index=1,  # デフォルト: ENFP
            key="woman_personality_select"
        )
        
        st.markdown("---")
        
        # 入力検証
        hobbies_valid = 1 <= len(selected_hobbies) <= 5
        
        if not hobbies_valid:
            st.warning("⚠️ 趣味は1〜5個選択してください")
        
        # 設定完了ボタン
        if st.button("✅ 設定完了 - 会話を開始", disabled=not hobbies_valid, type="primary"):
            # プロフィールを作成
            st.session_state.man_profile = ManProfile(personality_type=man_personality)
            st.session_state.woman_profile = WomanProfile(
                age_range=age_range,
                location_area=location_area,
                location_detail=location_detail,
                family_structure=family_structure,
                hobbies=selected_hobbies,
                personality_type=woman_personality
            )
            
            # エージェントを初期化
            try:
                st.session_state.woman_agent = WomanAgent(st.session_state.woman_profile)
                st.session_state.hint_generator = HintGenerator(
                    st.session_state.man_profile,
                    st.session_state.woman_profile
                )
                st.session_state.setup_complete = True
                st.rerun()
            except FileNotFoundError as e:
                st.error(f"エラー: {e}")
                st.info("先にRAGシステムを構築してください。")
    
    else:
        # 設定完了後
        st.success("✅ 設定完了")
        
        # プロフィール表示
        with st.expander("📋 プロフィール確認", expanded=False):
            st.markdown("**👨 A: あなた（男性）**")
            st.text(st.session_state.man_profile.get_summary())
            
            st.markdown("**👩 B: 相手（女性）**")
            st.text(st.session_state.woman_profile.get_summary())
        
        st.markdown("---")
        
        # 操作ボタン
        if st.button("🔄 リセット", type="secondary"):
            # 全てリセット
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# メインエリア
if not st.session_state.setup_complete:
    # セットアップ画面
    st.info("👈 左のサイドバーでプロフィールを設定してください")
    
    st.markdown("### 📖 使い方")
    st.markdown("""
    1. **あなた（男性）の性格タイプ**を選択
    2. **相手女性のプロフィール**を設定
       - 年齢
       - 居住地
       - 家族構成
       - 趣味・興味（1〜5個）
       - 性格タイプ
    3. 「設定完了」ボタンをクリック
    4. 女性からのメッセージに対して、AIが回答ヒントを提供
    5. ヒントを参考に返信を入力
    """)

else:
    # チャット画面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 チャット")
        
        # 会話開始
        if len(st.session_state.messages) == 0:
            with st.spinner("相手からのメッセージを生成中..."):
                # 女性からの最初のメッセージを生成
                first_message = st.session_state.woman_agent.generate_message(is_first_message=True)
                st.session_state.messages.append({
                    "role": "B",
                    "content": first_message
                })
                st.session_state.waiting_for_user = True
                
                # ヒント生成
                hint = st.session_state.hint_generator.generate_hint(
                    first_message,
                    []
                )
                st.session_state.current_hint = hint
        
        # メッセージ表示
        for message in st.session_state.messages:
            if message["role"] == "B":
                with st.chat_message("assistant", avatar="👩"):
                    st.markdown(f"**相手の女性:**\n\n{message['content']}")
            else:
                with st.chat_message("user", avatar="👨"):
                    st.markdown(f"**あなた:**\n\n{message['content']}")
        
        # ユーザー入力
        if st.session_state.waiting_for_user:
            user_input = st.chat_input("返信を入力してください...")
            
            if user_input:
                # ユーザーのメッセージを追加
                st.session_state.messages.append({
                    "role": "A",
                    "content": user_input
                })
                st.session_state.woman_agent.add_user_message(user_input)
                st.session_state.waiting_for_user = False
                
                # 女性の次のメッセージを生成
                with st.spinner("相手が返信を考えています..."):
                    next_message = st.session_state.woman_agent.generate_message(is_first_message=False)
                    st.session_state.messages.append({
                        "role": "B",
                        "content": next_message
                    })
                    
                    # 新しいヒントを生成
                    hint = st.session_state.hint_generator.generate_hint(
                        next_message,
                        st.session_state.woman_agent.conversation_history
                    )
                    st.session_state.current_hint = hint
                    st.session_state.waiting_for_user = True
                
                st.rerun()
    
    with col2:
        st.header("💡 回答ヒント")
        
        if st.session_state.current_hint and st.session_state.waiting_for_user:
            hint = st.session_state.current_hint
            
            # 推奨回答
            st.subheader("【推奨回答】")
            st.info(hint.get("recommended_response", ""))
            
            st.markdown("---")
            
            # プロフィール考慮ポイント
            st.subheader("【プロフィール考慮ポイント】")
            profile_points = hint.get("profile_points", {})
            
            if "age" in profile_points:
                st.markdown(f"👤 **年齢:** {profile_points['age']}")
            if "location" in profile_points:
                st.markdown(f"📍 **居住地:** {profile_points['location']}")
            if "family" in profile_points:
                st.markdown(f"👨‍👩‍👧 **家族:** {profile_points['family']}")
            if "hobbies" in profile_points:
                st.markdown(f"🎨 **趣味:** {profile_points['hobbies']}")
            
            st.markdown("---")
            
            # 性格考慮ポイント
            st.subheader("【性格考慮ポイント】")
            personality_points = hint.get("personality_points", [])
            for point in personality_points:
                st.markdown(f"🧠 {point}")
            
            st.markdown("---")
            
            # 好まれそうな回答例
            st.subheader("【✅ 好まれそうな回答例】")
            good_example = hint.get("good_example", {})
            if good_example:
                st.success(good_example.get("text", ""))
                with st.expander("💡 理由"):
                    st.write(good_example.get("reason", ""))
            
            st.markdown("---")
            
            # 避けるべき回答例
            st.subheader("【❌ 避けるべき回答例】")
            bad_example = hint.get("bad_example", {})
            if bad_example:
                st.error(bad_example.get("text", ""))
                with st.expander("⚠️ 理由"):
                    st.write(bad_example.get("reason", ""))
        
        elif not st.session_state.waiting_for_user:
            st.info("あなたのメッセージを送信すると、新しいヒントが表示されます")

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Personality Chat Simulator v2.0 | Powered by OpenAI & LangChain</small>
</div>
""", unsafe_allow_html=True)
