import streamlit as st
import streamlit.components.v1 as components
import libs as glib 
import base

def generate_response(prompt):
    if base.get_num_tokens(prompt) >= 1000000:
        st.error("Conversation length too long. Please keep it under 1000000 tokens.")
        st.button(
            "🗑 Clear Chat History",
            on_click=base.clear_chat_history,
            key="clear_chat_history",
        )
        st.stop()

    # Enhanced prompt for general chat
    enhanced_prompt = f"""
    Context: General financial consultation and market discussion
    User Query: {prompt}
    
    Instructions:
    - Provide comprehensive financial insights
    - Use clear explanations with examples
    - Include actionable recommendations when appropriate
    - Maintain professional yet conversational tone
    - Format response with proper structure (headers, bullets, etc.)
    """
    
    response = glib.call_claude_sonet_stream(enhanced_prompt)
    return response

# Modern CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .stChatMessage {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💰 Finance Chatbot</h1>
    <p>Your AI-powered financial analysis assistant</p>
</div>
""", unsafe_allow_html=True)

# Initialize states
base.init_home_state(None)
base.init_slidebar()

# Welcome section
if len(st.session_state.messages) == 1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Getting Started</h3>
            <p>Ask me about:</p>
            <ul>
                <li>📊 Stock analysis and market trends</li>
                <li>💹 Investment strategies and portfolio advice</li>
                <li>📈 Technical analysis and chart patterns</li>
                <li>💰 Financial planning and risk management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=base.icons[message["role"]]):
        st.write(message["content"])
        if message == st.session_state["messages"][0]:
            if st.button("About Finance Chatbot?"):
                st.info("Finance Chatbot is your AI-powered assistant for financial analysis, market insights, and investment guidance. Ask me anything about stocks, markets, or financial planning!")

# Chat input
if prompt := st.chat_input("Ask me about finance, stocks, or investments..."):
    st.session_state.show_animation = False
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar=base.icons["user"]):
        st.write(prompt)

# Generate response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar=base.icons["assistant"]):
        response = generate_response(prompt)
        full_response = st.write_stream(response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

st.markdown('</div>', unsafe_allow_html=True)

# Quick actions
st.markdown("### 🎯 Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📈 Market Analysis", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Give me a current market analysis"})
        st.rerun()

with col2:
    if st.button("💹 Stock Picks", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Suggest some good stock picks for today"})
        st.rerun()

with col3:
    if st.button("📊 Portfolio Review", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "How should I review my investment portfolio?"})
        st.rerun()

with col4:
    if st.button("💰 Investment Tips", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Give me some investment tips for beginners"})
        st.rerun()
