import streamlit as st
import openai
import random
import time
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(
    page_title="Matrix Chatbot",
    page_icon="🤖",
    layout="wide"
)

# OpenAI API key setup
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Matrix rainfall background
matrix_bg = """
<style>
    canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
    .stApp {
        background: rgba(0, 0, 0, 0.7);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: rgba(0, 50, 0, 0.7);
        color: white;
    }
    .chat-message.assistant {
        background-color: rgba(0, 100, 0, 0.7);
        color: #00FF00;
    }
    .chat-message .content {
        margin-left: 10px;
    }
</style>
<canvas id="matrix"></canvas>
<script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    
    // Set canvas dimensions
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Characters to display
    const characters = "01";
    
    // Font size and columns
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    
    // Initialize drops
    const drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }
    
    // Draw function
    function draw() {
        // Set semi-transparent black background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Set text color and font
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        
        // Loop over drops
        for (let i = 0; i < drops.length; i++) {
            // Select random character
            const text = characters.charAt(Math.floor(Math.random() * characters.length));
            
            // Draw character
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            // Increment y coordinate and reset if needed
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    // Animation loop
    setInterval(draw, 33);
</script>
"""

# Function to interact with OpenAI API
def get_openai_response(prompt, api_key, max_tokens=100):
    if not api_key:
        return "Please enter your OpenAI API key in the sidebar."
    
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Keep your responses concise and under 100 words."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar for API key
with st.sidebar:
    st.title("Setup")
    st.session_state.api_key = st.text_input("Enter your OpenAI API key:", type="password", value=st.session_state.api_key)
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This is a Matrix-themed chatbot powered by OpenAI's GPT model.")
    st.markdown("All responses are limited to 100 words or less.")

# Main app layout
st.title("Matrix Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Enter your message...")
if user_prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("The Matrix is processing..."):
            assistant_response = get_openai_response(user_prompt, st.session_state.api_key)
            st.markdown(assistant_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Render Matrix background
html(matrix_bg)
