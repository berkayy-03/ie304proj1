import streamlit as st
from openai import OpenAI
from knowledge_base import SYSTEM_PROMPT

st.set_page_config(
    page_title="METU IE Summer Practice Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #f5f7fa; }
    .header-card {
        background: linear-gradient(135deg, #003366 0%, #0055a5 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,51,102,0.25);
    }
    .header-card h1 { font-size: 1.6rem; margin: 0 0 6px 0; font-weight: 700; }
    .header-card p  { font-size: 0.95rem; margin: 0; opacity: 0.88; }
    .chat-message {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
        align-items: flex-start;
    }
    .chat-message .avatar {
        width: 38px; height: 38px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .user-avatar   { background: #0055a5; }
    .bot-avatar    { background: #003366; }
    .chat-message .bubble {
        max-width: 85%;
        padding: 12px 16px;
        border-radius: 14px;
        line-height: 1.55;
        font-size: 0.95rem;
    }
    .user-bubble {
        background: #0055a5;
        color: white;
        border-bottom-right-radius: 4px;
        margin-left: auto;
    }
    .bot-bubble {
        background: white;
        color: #1a1a2e;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .user-row { flex-direction: row-reverse; }
    [data-testid="stSidebar"] { background-color: #f0f4f8; }
    .stButton > button {
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        padding: 4px 12px !important;
        border: 1px solid #0055a5 !important;
        color: #0055a5 !important;
        background: transparent !important;
    }
    .stButton > button:hover {
        background: #0055a5 !important;
        color: white !important;
    }
    .info-box {
        background: #e8f0fe;
        border-left: 4px solid #0055a5;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 0.88rem;
        color: #003366;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


def get_response(user_input, history):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("GROQ_API_KEY not found in Streamlit secrets.")
        st.stop()

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    # Build messages: system + last 6 exchanges + new message
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            max_tokens=1024,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def render_message(role, content):
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-row">
            <div class="avatar user-avatar">👤</div>
            <div class="bubble user-bubble">{content}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message">
            <div class="avatar bot-avatar">🎓</div>
            <div class="bubble bot-bubble">{content}</div>
        </div>""", unsafe_allow_html=True)


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_question" not in st.session_state:
    st.session_state.quick_question = None
if "pending_response" not in st.session_state:
    st.session_state.pending_response = False

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About")
    st.markdown("""
    This chatbot helps METU IE students with questions about:
    - **IE 300** Summer Practice
    - **IE 400** Summer Practice
    - SGK Insurance applications
    - Required documents & forms
    - Company opportunities
    - Deadlines & procedures
    """)
    st.divider()
    st.markdown("### 🔗 Official Links")
    st.markdown("- [SP Website](https://sp-ie.metu.edu.tr/en)")
    st.markdown("- [OCW System](https://ocw.metu.edu.tr)")
    st.markdown("- Email: ie-staj@metu.edu.tr")
    st.divider()
    st.markdown("### 💡 Quick Questions")

    quick_qs = [
        "What are IE 300 prerequisites?",
        "How do I apply for SGK insurance?",
        "What is the report deadline?",
        "Which companies are accepted for IE 400?",
        "Can IE 300 be done online?",
        "What documents do I need?",
    ]
    for q in quick_qs:
        if st.button(q, key=f"btn_{q}"):
            st.session_state.quick_question = q
            st.session_state.pending_response = True

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main
st.markdown("""
<div class="header-card">
    <h1>🎓 METU IE Summer Practice Assistant</h1>
    <p>Your virtual guide for IE 300 & IE 400 Summer Practices</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="info-box">
        👋 <strong>Welcome!</strong> I can answer questions about METU IE Summer Practices
        (IE 300 & IE 400), including requirements, documents, insurance, deadlines, and
        company opportunities. Ask me anything or use the quick questions in the sidebar!
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

if st.session_state.quick_question and st.session_state.pending_response:
    user_input = st.session_state.quick_question
    st.session_state.quick_question = None
    st.session_state.pending_response = False
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_message("user", user_input)
    with st.spinner("Thinking..."):
        reply = get_response(user_input, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": reply})
    render_message("assistant", reply)

if user_input := st.chat_input("Ask about IE 300 / IE 400 Summer Practice..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_message("user", user_input)
    with st.spinner("Thinking..."):
        reply = get_response(user_input, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": reply})
    render_message("assistant", reply)
