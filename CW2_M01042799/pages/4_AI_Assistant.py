import os # To access environment variables
import streamlit as st# import Streamlit for UI and dashboard
from openai import OpenAI # OpenAI Python client

# Initialize OpenAI client
try:
    api_key = st.secrets["OPENAI_API_KEY"]# Try to read API key from Streamlit secrets
except Exception:
    api_key = os.getenv("OPENAI_API_KEY")# Fallback: read from environment variable

# Stop app if API key is missing
if not api_key:
    st.error("OpenAI API key not found! Set it in .streamlit/secrets.toml or as an environment variable.")
    st.stop()

client = OpenAI(api_key=api_key)# Initialize OpenAI client

# Page configuration
st.set_page_config(
    page_title="💬 ChatGPT Assistant",
    page_icon="💬",
    layout="wide"
)

st.title("💬 ChatGPT - OpenAI ")
st.caption("Powered by GPT-4o")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []# Store chat messages

# Sidebar controls
with st.sidebar:
    st.subheader("Chat Controls")

    # Display message count (excluding system prompt)
    message_count = len([m for m in st.session_state.messages if m["role"] != "system"])
    st.metric("Messages", message_count)

    # Button to clear all chat messages
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Model selection
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=0)

    # Temperature slider (controls randomness of output)
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher values make output more random"
    )

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])# Show message content

# Get user input
prompt = st.chat_input("Say something...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Call OpenAI API and stream response
    with st.spinner("Thinking..."):
        completion = client.chat.completions.create(
            model=model,#Selected model
            messages=st.session_state.messages,#Chat history
            temperature=temperature,#Controls randomness
            stream=True#Stream partial responses
        )

    # Display streaming response
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta.content:
                full_reply += delta.content
                container.markdown(full_reply + "▌")  #Show typing cursor

        # Show full final response without cursor
        container.markdown(full_reply)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })
