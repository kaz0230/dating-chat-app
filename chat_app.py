"""
Personality Chat System - Streamlit Web UI
"""
import streamlit as st
from chat_agent import PersonalityChatAgent

st.set_page_config(page_title="Personality Chat Assistant", page_icon="💬", layout="wide")
st.title("💬 Personality Chat Assistant")
st.markdown("**16 Personalities性格診断を活用したチャット補助システム**")

st.sidebar.header("⚙️ 設定")
personality_types = ["INTJ", "ENFP", "ISTJ", "ESFP"]
user_personality = st.sidebar.selectbox("あなたの性格タイプ", personality_types, index=0)
partner_personality = st.sidebar.selectbox("相手の性格タイプ", personality_types, index=1)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 機能")
st.sidebar.markdown("- 相手の性格を考慮した会話アドバイス\n- 性格特性に基づくコミュニケーション提案\n- リアルタイムチャットサポート")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state or st.session_state.get("user_personality") != user_personality or st.session_state.get("partner_personality") != partner_personality:
    try:
        st.session_state.agent = PersonalityChatAgent(user_personality=user_personality, partner_personality=partner_personality)
        st.session_state.user_personality = user_personality
        st.session_state.partner_personality = partner_personality
    except FileNotFoundError as e:
        st.error(f"エラー: {e}")
        st.info("先にデータを準備してください。ターミナルで以下を実行:")
        st.code("python personality_scraper.py\npython build_rag.py")
        st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.header("チャット")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("メッセージを入力してください..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("考え中..."):
                response = st.session_state.agent.chat(prompt)
                st.markdown(response["answer"])
                if response["source_documents"]:
                    with st.expander("📚 参考にした情報"):
                        for i, doc in enumerate(response["source_documents"], 1):
                            st.markdown(f"**{i}. {doc.metadata['personality_type']}型の情報**")
                            st.text(doc.page_content[:200] + "...")
                            st.markdown("---")
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

with col2:
    st.header("性格分析")
    st.subheader(f"🎯 {partner_personality}型の特徴")
    with st.spinner("分析中..."):
        insights = st.session_state.agent.get_personality_insights(partner_personality)
        for insight in insights:
            with st.expander(f"{insight['type']}型", expanded=True):
                st.write(insight['content'])
    st.markdown("---")
    if st.button("💡 会話のヒントを取得"):
        with st.spinner("提案を生成中..."):
            suggestions = st.session_state.agent.get_conversation_suggestions()
            st.success("**会話のヒント**")
            st.info(suggestions)
    if st.button("🔄 会話履歴をリセット"):
        st.session_state.messages = []
        st.session_state.agent.clear_history()
        st.rerun()

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'><small>Personality Chat System v1.0 | Powered by OpenAI & LangChain</small></div>", unsafe_allow_html=True)
