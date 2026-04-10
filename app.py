import streamlit as st
import google.generativeai as genai
from knowledge_base import SYSTEM_PROMPT

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="METU IE Summer Practice Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #f5f7fa; }

    /* Header card */
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

    /* Chat messages */
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
    .user-row  { flex-direction: row-reverse; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #f0f4f8; }

    /* Input box */
    .stChatInput > div { border-radius: 12px !important; }

    /* Quick question buttons */
    .stButton > button {
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        padding: 4px 12px !important;
        border: 1px solid #0055a5 !important;
        color: #0055a5 !important;
        background: transparent !important;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: #0055a5 !important;
        color: white !important;
    }

    /* Info box */
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

# ── Helpers ────────────────────────────────────────────────────────────────────

def get_model():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found in Streamlit secrets. Please add it.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )


def render_message(role: str, content: str):
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


def stream_response(model, history: list, user_input: str) -> str:
    gemini_history = []
    for msg in history[:-1]:
        gemini_history.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [msg["content"]]
        })

    chat = model.start_chat(history=gemini_history)
    full_text = ""
    placeholder = st.empty()

    for chunk in chat.send_message(user_input, stream=True):
        if chunk.text:
            full_text += chunk.text
            placeholder.markdown(f"""
            <div class="chat-message">
                <div class="avatar bot-avatar">🎓</div>
                <div class="bubble bot-bubble">{full_text}▌</div>
            </div>""", unsafe_allow_html=True)

    placeholder.markdown(f"""
    <div class="chat-message">
        <div class="avatar bot-avatar">🎓</div>
        <div class="bubble bot-bubble">{full_text}</div>
    </div>""", unsafe_allow_html=True)

    return full_text


# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None

# ── Sidebar ────────────────────────────────────────────────────────────────────
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

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Main area ──────────────────────────────────────────────────────────────────
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

# Render existing conversation
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

# Handle quick question from sidebar
if st.session_state.quick_question:
    user_input = st.session_state.quick_question
    st.session_state.quick_question = None

    st.session_state.messages.append({"role": "user", "content": user_input})
    render_message("user", user_input)

    model = get_model()
    response = stream_response(model, st.session_state.messages, user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Chat input
if user_input := st.chat_input("Ask about IE 300 / IE 400 Summer Practice..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_message("user", user_input)

    model = get_model()
    response = stream_response(model, st.session_state.messages, user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
