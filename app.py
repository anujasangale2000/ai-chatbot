import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="AI Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background and text */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stChatMessage {
        padding: 10px !important;
    }
    
    /* Chat message styling */
    .stChatMessage.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 18px;
        padding: 12px 16px !important;
        margin-left: auto;
        margin-right: 0;
        width: fit-content;
        max-width: 70%;
        animation: slideInRight 0.3s ease-out;
    }
    
    .stChatMessage.assistant {
        background: #f0f0f0;
        border-radius: 18px;
        padding: 12px 16px !important;
        margin-right: auto;
        margin-left: 0;
        width: fit-content;
        max-width: 70%;
        animation: slideInLeft 0.3s ease-out, bounce 0.5s ease-out;
    }
    
    /* Animation: Slide in from right (user messages) */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Animation: Slide in from left (bot messages) */
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Animation: Bounce effect */
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    /* Chat input styling */
    .stChatInput {
        border-radius: 25px !important;
        border: 2px solid #667eea !important;
        padding: 10px !important;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">🤖 AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your smart AI assistant - Chat about anything!</div>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Sidebar for user name (optional)
with st.sidebar:
    st.write("### ⚙️ Settings")
    user_name = st.text_input("Your name (optional):", value=st.session_state.user_name or "")
    if user_name:
        st.session_state.user_name = user_name
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here... ✨")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get response from Ollama
    with st.spinner("🤔 Thinking..."):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": user_input,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                assistant_message = response.json()["response"]
            else:
                assistant_message = "Oops! Something went wrong. Make sure Ollama is running!"
        except:
            assistant_message = "❌ Can't connect to Ollama. Is it running in the background?"
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    
    # Display assistant message with animation
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
    
    # Rerun to show smooth animation
    st.rerun()