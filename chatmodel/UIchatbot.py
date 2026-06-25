#streamlit run chatmodel/UIchatbot.py
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# ── Personalities and Themes ──────────────────────────────────────────────────
PERSONALITIES = {
    "🎭 Funny": "You are a funny and witty AI agent, if asked about any topic you have to answer with jokes and make sure that answer is related to the topic",
    "😡 Angry": "You are an angry AI agent, if asked about any topic you have to answer with anger and make sure that answer is related to the topic",
    "😏 Sarcastic": "You are a sarcastic AI agent, if asked about any topic you have to answer with sarcasm and make sure that answer is related to the topic",
    "😢 Sad": "You are a sad AI agent, if asked about any topic you have to answer with sadness and make sure that answer is related to the topic",
    "💖 Romantic": "You are a romantic AI agent, if asked about any topic you have to answer with romance and make sure that answer is related to the topic",
}

THEMES = {
    "🎭 Funny": {
        "bg": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        "title": "linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6)",
        "accent": "linear-gradient(135deg, #a78bfa, #6366f1)",
        "bubble_user": "rgba(99, 102, 241, 0.45)",
        "border_user": "rgba(167, 139, 250, 0.3)",
        "avatar_bot": "🎭",
        "name": "Witty AI",
        "sub": "Powered by Mistral · Fuelled by bad puns 🎤",
        "color": "#a78bfa"
    },
    "😡 Angry": {
        "bg": "linear-gradient(135deg, #200101, #4a0e0e, #1a0202)",
        "title": "linear-gradient(90deg, #f87171, #ef4444, #b91c1c)",
        "accent": "linear-gradient(135deg, #f87171, #ef4444)",
        "bubble_user": "rgba(239, 68, 68, 0.45)",
        "border_user": "rgba(248, 113, 113, 0.3)",
        "avatar_bot": "😡",
        "name": "Angry AI",
        "sub": "IT'S ALWAYS A BAD TIME TO CHAT 😤",
        "color": "#f87171"
    },
    "😏 Sarcastic": {
        "bg": "linear-gradient(135deg, #0d2b2b, #124e4f, #051414)",
        "title": "linear-gradient(90deg, #2dd4bf, #0d9488, #0f766e)",
        "accent": "linear-gradient(135deg, #2dd4bf, #0d9488)",
        "bubble_user": "rgba(13, 148, 136, 0.45)",
        "border_user": "rgba(45, 212, 191, 0.3)",
        "avatar_bot": "😏",
        "name": "Sarcastic AI",
        "sub": "Oh great, another human question... How thrilling 🙄",
        "color": "#2dd4bf"
    },
    "😢 Sad": {
        "bg": "linear-gradient(135deg, #181d26, #2d3748, #0f1319)",
        "title": "linear-gradient(90deg, #94a3b8, #64748b, #475569)",
        "accent": "linear-gradient(135deg, #94a3b8, #64748b)",
        "bubble_user": "rgba(100, 116, 139, 0.45)",
        "border_user": "rgba(148, 163, 184, 0.3)",
        "avatar_bot": "😢",
        "name": "Melancholic AI",
        "sub": "Just here, wallowing in the depths of binary sorrow 🌧️",
        "color": "#94a3b8"
    },
    "💖 Romantic": {
        "bg": "linear-gradient(135deg, #2d0b1e, #63153e, #1e0513)",
        "title": "linear-gradient(90deg, #fb7185, #f43f5e, #be123c)",
        "accent": "linear-gradient(135deg, #fb7185, #f43f5e)",
        "bubble_user": "rgba(244, 63, 94, 0.45)",
        "border_user": "rgba(251, 113, 133, 0.3)",
        "avatar_bot": "💖",
        "name": "Romantic AI",
        "sub": "Speak to me, darling, and let the circuits of love hum 💕",
        "color": "#fb7185"
    }
}

# Initialize session states
if "current_personality" not in st.session_state:
    st.session_state.current_personality = "🎭 Funny"

current_pers = st.session_state.current_personality
current_theme = THEMES[current_pers]

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=PERSONALITIES[current_pers])
    ]
if "display_history" not in st.session_state:
    st.session_state.display_history = []

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=current_theme["name"],
    page_icon=current_theme["avatar_bot"],
    layout="centered",
)

# ── Custom CSS Injector ────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Animated gradient background */
  .stApp {{
    background: {current_theme['bg']};
    min-height: 100vh;
    transition: background 0.8s ease;
  }}

  /* Hide Streamlit chrome */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding-top: 1.5rem; padding-bottom: 0; }}

  /* Glass card wrapper */
  .glass-card {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 2rem 2rem 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    margin-bottom: 1.5rem;
  }}

  /* Title */
  .chat-title {{
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    background: {current_theme['title']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: -0.5px;
  }}

  .chat-subtitle {{
    text-align: center;
    color: rgba(200, 200, 255, 0.65);
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
    font-family: 'Segoe UI', sans-serif;
  }}

  /* Chat bubbles */
  .bubble-row {{
    display: flex;
    margin-bottom: 1rem;
    align-items: flex-end;
    gap: 0.6rem;
  }}
  .bubble-row.user  {{ flex-direction: row-reverse; }}
  .bubble-row.bot   {{ flex-direction: row; }}

  .avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  }}
  .avatar.user {{ background: {current_theme['accent']}; }}
  .avatar.bot  {{ background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05)); border: 1px solid rgba(255,255,255,0.2); }}

  .bubble {{
    max-width: 72%;
    padding: 0.75rem 1.1rem;
    border-radius: 18px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 0.95rem;
    line-height: 1.55;
    word-break: break-word;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  }}
  .bubble.user {{
    background: {current_theme['bubble_user']};
    border: 1px solid {current_theme['border_user']};
    color: #f0edff;
    border-bottom-right-radius: 4px;
  }}
  .bubble.bot {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #e9e9ff;
    border-bottom-left-radius: 4px;
  }}

  /* Message container scroll area */
  .messages-container {{
    max-height: 360px;
    overflow-y: auto;
    padding-right: 0.25rem;
    margin-bottom: 1rem;
    scrollbar-width: thin;
    scrollbar-color: {current_theme['color']}33 transparent;
  }}
  .messages-container::-webkit-scrollbar {{ width: 4px; }}
  .messages-container::-webkit-scrollbar-thumb {{
    background: {current_theme['color']}55;
    border-radius: 4px;
  }}

  /* Input row */
  .stTextInput > div > div > input {{
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #f0edff !important;
    padding: 0.65rem 1rem !important;
    font-family: 'Segoe UI', sans-serif !important;
    font-size: 0.95rem !important;
    caret-color: {current_theme['color']};
  }}
  .stTextInput > div > div > input::placeholder {{ color: rgba(200,200,255,0.4) !important; }}
  .stTextInput > div > div > input:focus {{
    border-color: {current_theme['color']}99 !important;
    box-shadow: 0 0 0 3px {current_theme['color']}33 !important;
  }}

  /* Custom styling to override Streamlit selectbox for glassmorphism */
  div[data-baseweb="select"] {{
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
  }}
  div[data-baseweb="select"] * {{
    color: #f0edff !important;
    font-family: 'Segoe UI', sans-serif !important;
  }}
  div[role="listbox"] {{
    background-color: #1f1b2e !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
  }}
  div[role="option"] {{
    background-color: transparent !important;
  }}
  div[role="option"]:hover {{
    background-color: rgba(255, 255, 255, 0.1) !important;
  }}
  
  .stSelectbox label p {{
    color: rgba(200, 200, 255, 0.75) !important;
    font-family: 'Segoe UI', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
  }}

  /* Buttons */
  .stButton > button {{
    background: {current_theme['accent']} !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: 'Segoe UI', sans-serif !important;
    height: 2.65rem !important;
    width: 100% !important;
    transition: transform 0.1s ease, opacity 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }}
  .stButton > button:hover {{
    opacity: 0.9 !important;
    transform: translateY(-1px);
  }}
  .stButton > button:active {{
    transform: translateY(1px);
  }}

  /* Clear button */
  .clear-btn button {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: rgba(200,200,255,0.6) !important;
    font-size: 0.8rem !important;
  }}

  /* Divider */
  .glass-divider {{
    border: none;
    border-top: 1px solid rgba(255,255,255,0.12);
    margin: 1.2rem 0;
  }}
</style>
""", unsafe_allow_html=True)

# ── Helper ────────────────────────────────────────────────────────────────────
def render_bubble(role: str, text: str):
    avatar = "🧑" if role == "user" else current_theme["avatar_bot"]
    st.markdown(f"""
    <div class="bubble-row {role}">
      <div class="avatar {role}">{avatar}</div>
      <div class="bubble {role}">{text}</div>
    </div>""", unsafe_allow_html=True)

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown(f'<div class="chat-title">{current_theme["name"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="chat-subtitle">{current_theme["sub"]}</div>', unsafe_allow_html=True)

# Personality Select Box
selected_personality = st.selectbox(
    "Choose Chatbot Personality:",
    options=list(PERSONALITIES.keys()),
    index=list(PERSONALITIES.keys()).index(st.session_state.current_personality),
)

# If personality changed, reset history and rerun
if selected_personality != st.session_state.current_personality:
    st.session_state.current_personality = selected_personality
    st.session_state.messages = [
        SystemMessage(content=PERSONALITIES[selected_personality])
    ]
    st.session_state.display_history = []
    st.rerun()

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# Messages area
st.markdown('<div class="messages-container">', unsafe_allow_html=True)
if not st.session_state.display_history:
    st.markdown(f"""
    <div style="text-align:center; color:rgba(200,200,255,0.35);
                font-family:'Segoe UI',sans-serif; font-size:0.9rem; padding:2rem 0;">
      A start of something beautiful... Say hello to your {selected_personality[2:]} companion! 👋
    </div>""", unsafe_allow_html=True)
else:
    for msg in st.session_state.display_history:
        render_bubble(msg["role"], msg["text"])
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="glass-divider">', unsafe_allow_html=True)

# Input row
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "message",
        label_visibility="collapsed",
        placeholder="Type a message...",
        key="user_input",
    )
with col2:
    send = st.button("Send ➤")

# Clear button
col_clear, _ = st.columns([1, 4])
with col_clear:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑 Clear"):
        st.session_state.display_history = []
        st.session_state.messages = [
            SystemMessage(content=PERSONALITIES[st.session_state.current_personality])
        ]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close glass-card

# ── Logic ─────────────────────────────────────────────────────────────────────
if send and user_input.strip():
    # User message
    st.session_state.display_history.append({"role": "user", "text": user_input})
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Bot response
    with st.spinner(""):
        model = ChatMistralAI(model="mistral-small-2603", temperature=0.9, max_tokens=150)
        res = model.invoke(st.session_state.messages)

    bot_reply = res.content
    st.session_state.messages.append(AIMessage(content=bot_reply))
    st.session_state.display_history.append({"role": "bot", "text": bot_reply})
    st.rerun()