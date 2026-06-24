import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mistral Chat",
    page_icon="🌀",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0d0f14;
    color: #e2e4ea;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }

/* ── Main container ── */
.main .block-container {
    max-width: 760px;
    padding: 2rem 1.5rem 6rem;
}

/* ── Title ── */
.chat-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 500;
    color: #7c6dfa;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.chat-subtitle {
    font-size: 0.78rem;
    color: #555a70;
    margin-bottom: 2rem;
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
    align-items: flex-start;
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    font-family: 'JetBrains Mono', monospace;
}
.avatar.user { background: #7c6dfa22; color: #7c6dfa; border: 1px solid #7c6dfa44; }
.avatar.ai   { background: #1e2030; color: #9ba3c2; border: 1px solid #2a2d40; }

.bubble {
    max-width: 78%;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    font-size: 0.92rem;
    line-height: 1.6;
    word-break: break-word;
}
.bubble.user {
    background: #7c6dfa18;
    border: 1px solid #7c6dfa30;
    color: #d4d8f0;
    border-top-right-radius: 4px;
}
.bubble.ai {
    background: #1a1d2a;
    border: 1px solid #2a2d40;
    color: #c8ccde;
    border-top-left-radius: 4px;
}

/* ── Typing indicator ── */
.typing-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #7c6dfa;
    animation: blink 1.2s infinite;
    margin: 0 2px;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink {
    0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
    40%           { opacity: 1;   transform: scale(1); }
}

/* ── Input area ── */
[data-testid="stChatInput"] > div {
    background: #141720 !important;
    border: 1px solid #2a2d40 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #e2e4ea !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
}
[data-testid="stChatInput"] button { color: #7c6dfa !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0b0d11;
    border-right: 1px solid #1e2030;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p { color: #6b7090 !important; font-size: 0.82rem !important; }
[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"] { color: #7c6dfa !important; }
[data-testid="stSidebar"] h2 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #7c6dfa;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Clear button ── */
.stButton > button {
    background: transparent;
    border: 1px solid #2a2d40;
    color: #6b7090;
    border-radius: 8px;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.2s;
}
.stButton > button:hover {
    border-color: #7c6dfa55;
    color: #9b8efa;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #3a3d52;
}
.empty-state .icon { font-size: 2.5rem; margin-bottom: 1rem; }
.empty-state p { font-size: 0.88rem; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙ Settings")
    st.divider()

    temperature = st.slider("Temperature", 0.0, 1.0, 0.9, 0.05,
                            help="Higher = more creative. Lower = more focused.")
    max_tokens = st.slider("Max tokens", 50, 1000, 300, 50,
                           help="Maximum length of each reply.")
    model_name = st.selectbox("Model", [
        "mistral-small-2603",
        "mistral-medium-2505",
        "mistral-large-2411",
    ])

    st.divider()
    if st.button("🗑 Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<p style='margin-top:2rem'>Powered by Mistral via LangChain</p>",
                unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-title">🌀 Mistral Chat</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">mistral-small · langchain · streamlit</div>',
            unsafe_allow_html=True)

# ── Render history ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🌀</div>
        <p>No messages yet.<br>Type something below to start a conversation.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        avatar_label = "you" if role == "user" else "ai"
        avatar_char  = "U"  if role == "user" else "M"
        st.markdown(f"""
        <div class="msg-row {avatar_label}">
            <div class="avatar {avatar_label}">{avatar_char}</div>
            <div class="bubble {avatar_label}">{content}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Message Mistral…"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user bubble immediately
    st.markdown(f"""
    <div class="msg-row user">
        <div class="avatar user">U</div>
        <div class="bubble user">{prompt}</div>
    </div>
    """, unsafe_allow_html=True)

    # Typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="msg-row ai">
        <div class="avatar ai">M</div>
        <div class="bubble ai">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Call model
    model = ChatMistralAI(model=model_name, temperature=temperature, max_tokens=max_tokens)
    response = model.invoke(prompt)
    reply = response.content

    # Replace typing indicator with actual reply
    typing_placeholder.markdown(f"""
    <div class="msg-row ai">
        <div class="avatar ai">M</div>
        <div class="bubble ai">{reply}</div>
    </div>
    """, unsafe_allow_html=True)

    # Persist
    st.session_state.messages.append({"role": "assistant", "content": reply})