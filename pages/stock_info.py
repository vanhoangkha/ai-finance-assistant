import streamlit as st
import streamlit.components.v1 as components
import libs as glib 
import base

def generate_response(prompt):
    if base.get_num_tokens(prompt) >= 1000000:
        st.error("Conversation length too long. Please keep it under 1000000 tokens.")
        st.button(
            "🗑 Clear Chat History",
            on_click=base.clear_stock_advisor,
            key="clear_chat_history",
        )
        st.stop()

    # Enhanced prompt for stock information
    enhanced_prompt = f"""
    Context: Stock Information & Market Data Analysis
    
    Task: Provide detailed stock information and market insights for user queries
    
    Analysis Framework:
    1. COMPANY OVERVIEW: Business model, sector, competitive position
    2. FINANCIAL METRICS: Key ratios, revenue trends, profitability  
    3. MARKET PERFORMANCE: Price action, volume, volatility analysis
    4. VALUATION: Fair value assessment, comparison to peers
    5. RISK FACTORS: Company-specific and market risks
    6. INVESTMENT THESIS: Bull/bear cases with supporting evidence
    
    Response Requirements:
    - Use clear headers and bullet points
    - Include specific numbers and percentages when available
    - Provide both technical and fundamental perspectives
    - End with actionable insights or recommendations
    - Maintain professional yet accessible tone
    
    User Question: {prompt}
    """
    
    response = glib.call_claude_sonet_stream(enhanced_prompt)
    return response

# Modern CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: #333;
    }
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #ff9a9e;
    }
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .quick-query {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        cursor: pointer;
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
    <h1>💹 Stock Information Hub</h1>
    <p>Get detailed information about any stock or company</p>
</div>
""", unsafe_allow_html=True)

base.init_stock_advisor()
base.init_slidebar()

# Quick stock lookup section
st.markdown("### 🔍 Quick Stock Lookup")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, MSFT)", placeholder="AAPL")

with col2:
    query_type = st.selectbox("Information Type", [
        "Company Overview",
        "Financial Performance", 
        "Recent News",
        "Analyst Ratings",
        "Dividend Information",
        "Technical Analysis"
    ])

with col3:
    if st.button("🔍 Search", use_container_width=True):
        if stock_symbol:
            query = f"Provide {query_type.lower()} for {stock_symbol.upper()}"
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

# Popular stocks section
st.markdown("### 📈 Popular Stocks")
popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX"]

cols = st.columns(4)
for i, stock in enumerate(popular_stocks):
    with cols[i % 4]:
        if st.button(f"📊 {stock}", use_container_width=True):
            query = f"Give me a comprehensive overview of {stock} including current price, recent performance, and key metrics"
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

# Chat interface
st.markdown("### 💬 Stock Information Chat")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=base.icons[message["role"]]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask about any stock, company, or market information..."):
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

# Quick queries section
st.markdown("### ⚡ Quick Queries")
quick_queries = [
    "What are the top performing stocks today?",
    "Show me dividend aristocrats",
    "Which tech stocks are undervalued?",
    "What are the best growth stocks?",
    "Explain P/E ratios",
    "How to read financial statements?"
]

cols = st.columns(3)
for i, query in enumerate(quick_queries):
    with cols[i % 3]:
        if st.button(query, key=f"quick_{i}"):
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

# Information cards
st.markdown("### 📚 Stock Analysis Guide")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>📊 Fundamental Analysis</h4>
        <p>Learn about P/E ratios, revenue growth, debt levels, and other key financial metrics that determine a company's intrinsic value.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>📈 Technical Analysis</h4>
        <p>Understand chart patterns, moving averages, RSI, MACD, and other technical indicators for timing your trades.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>📰 Market News</h4>
        <p>Stay updated with earnings reports, analyst upgrades/downgrades, and market-moving news that affects stock prices.</p>
    </div>
    """, unsafe_allow_html=True)
