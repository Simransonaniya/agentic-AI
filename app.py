import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Groq AI Chatbot", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    h1 { color: #ffffff; text-align: center; font-family: 'Segoe UI', sans-serif; }
    .subtitle { text-align: center; color: #8b949e; font-size: 14px; margin-bottom: 30px; }
    .stButton > button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 8px;
        width: 100%;
    }
    .stButton > button:hover { background-color: #f55036; color: white; border-color: #f55036; }
    .token-badge {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        color: #8b949e;
        display: inline-block;
        margin: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Get your free key at https://console.groq.com",
    )

    st.divider()

    model_choice = st.selectbox(
        "Model",
        options=[
            "llama3-8b-8192",
            "gemma2-9b-it",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "openai/gpt-oss-20b",
        ],
        index=0,
        help="llama3-8b = fastest & free | gemma2 = balanced | llama-4 = most capable",
    )

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, friendly, and knowledgeable AI assistant. Answer clearly and concisely.",
        height=120,
    )

    max_tokens = st.slider("Max Response Tokens", 256, 4096, 1024, step=128)

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.rerun()

    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0

    st.markdown(
        f'<div class="token-badge">🔢 Tokens used: {st.session_state.total_tokens:,}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("<small style='color:#8b949e'>Built with Streamlit + Groq API ⚡</small>", unsafe_allow_html=True)


# ── Main UI ──────────────────────────────────────────────────────────────────
st.markdown("# ⚡ Groq AI Chatbot")
st.markdown('<p class="subtitle">Powered by Groq · Free & Blazing Fast · Ask me anything!</p>', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Type your message here…")

if user_input:
    # Validate API key
    if not api_key_input or not api_key_input.startswith("gsk_"):
        st.error("⚠️ Please enter a valid Groq API key in the sidebar.")
        st.stop()

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build message history for API
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    client = Groq(api_key=api_key_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "system", "content": system_prompt}] + api_messages,
                max_tokens=max_tokens,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)
            st.session_state.total_tokens += len(full_response.split()) * 2

        except Exception as e:
            full_response = f"❌ Error: {str(e)}"
            placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})