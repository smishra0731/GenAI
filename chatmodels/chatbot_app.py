import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()  # Load environment variables from .env file

st.set_page_config(page_title="GenAI Chatbot", page_icon="🤖", layout="centered")

# Initialize the chat model
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9)

# Same modes as the original code, plus card styling info
MODES = {
    "Funny AI": {
        "emoji": "😂",
        "tagline": "Humorous and entertaining",
        "color1": "#FFB347",
        "color2": "#FFCC33",
        "prompt": "You are a Funny AI agent. You are humorous and entertaining.",
    },
    "Sad AI": {
        "emoji": "😢",
        "tagline": "Empathetic and understanding",
        "color1": "#4A90E2",
        "color2": "#6FB1FC",
        "prompt": "You are a Sad AI agent. You are empathetic and understanding.",
    },
    "Angry AI": {
        "emoji": "😡",
        "tagline": "Aggressive and impatient",
        "color1": "#E53935",
        "color2": "#FF6F60",
        "prompt": "You are an Angry AI agent. You respond aggressively and impatiently.",
    },
}

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .mood-card {
        border-radius: 18px;
        padding: 28px 12px 22px 12px;
        text-align: center;
        color: white;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 10px;
    }
    .mood-card:hover {
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 12px 26px rgba(0,0,0,0.35);
    }
    .mood-emoji { font-size: 56px; line-height: 1.1; }
    .mood-title { font-size: 22px; font-weight: 700; margin-top: 8px; }
    .mood-tagline { font-size: 14px; opacity: 0.95; margin-top: 4px; }
    .hero { text-align: center; margin-bottom: 8px; }
    .hero h1 { margin-bottom: 0; }
    .hero p { opacity: 0.75; }
    .mood-banner {
        border-radius: 14px;
        padding: 14px 18px;
        color: white;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        margin-bottom: 16px;
    }
    .mood-banner .emoji { font-size: 36px; }
    .mood-banner .name { font-size: 20px; font-weight: 700; }
    .mood-banner .hint { font-size: 13px; opacity: 0.9; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Step 1: Choose AI mode (cards) ----------
if "messages" not in st.session_state:
    st.markdown(
        "<div class='hero'><h1>🤖 GenAI Chatbot</h1>"
        "<p>Choose your AI mode</p></div>",
        unsafe_allow_html=True,
    )
    st.write("")

    cols = st.columns(len(MODES))
    for col, (name, info) in zip(cols, MODES.items()):
        with col:
            st.markdown(
                f"""
                <div class="mood-card"
                     style="background: linear-gradient(135deg, {info['color1']}, {info['color2']});">
                    <div class="mood-emoji">{info['emoji']}</div>
                    <div class="mood-title">{name}</div>
                    <div class="mood-tagline">{info['tagline']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Chat with {name}", key=name, use_container_width=True):
                st.session_state.messages = [SystemMessage(content=info["prompt"])]
                st.session_state.mode_name = name
                st.rerun()

# ---------- Step 2: Chat ----------
else:
    name = st.session_state.mode_name
    info = MODES[name]

    st.markdown(
        f"""
        <div class="mood-banner"
             style="background: linear-gradient(135deg, {info['color1']}, {info['color2']});">
            <div class="emoji">{info['emoji']}</div>
            <div>
                <div class="name">{name}</div>
                <div class="hint">Type 0 to exit</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Show previous conversation (skip the system message)
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar=info["emoji"]):
                st.write(msg.content)

    prompt = st.chat_input("You: ")
    if prompt:
        # Type 0 to exit -> go back to mood selection
        if prompt.strip() == "0":
            del st.session_state["messages"]
            del st.session_state["mode_name"]
            st.rerun()

        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant", avatar=info["emoji"]):
            with st.spinner("Thinking..."):
                response = model.invoke(st.session_state.messages)
            st.write(response.content)

        st.session_state.messages.append(AIMessage(content=response.content))
