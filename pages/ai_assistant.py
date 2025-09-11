import streamlit as st
import boto3
from langchain_aws import ChatBedrock
import json
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
import pandas as pd
import os
from polygon_client import PolygonClient
from bs4 import BeautifulSoup
import re
import requests
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain import hub
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import base

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
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .tool-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
    <h1>🤖 AI Stock Assistant</h1>
    <p>Advanced AI agent with real-time market data and analysis tools</p>
</div>
""", unsafe_allow_html=True)

load_dotenv()

# Initialize AWS Bedrock
def init_bedrock():
    try:
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        )
        
        model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        model_kwargs = {
            "max_tokens": 2048,
            "temperature": 0.0,
            "top_k": 250,
            "top_p": 1,
            "stop_sequences": ["\n\nHuman"],
        }
        
        return ChatBedrock(
            client=bedrock_runtime,
            model_id=model_id,
            model_kwargs=model_kwargs,
        )
    except Exception as e:
        st.error(f"Error initializing Bedrock: {str(e)}")
        return None

# Stock data tools
def get_stock_price(symbol):
    """Get current stock price and basic info using Polygon.io"""
    try:
        client = PolygonClient()
        df = client.get_stock_data(symbol, days=5)
        
        if df is None or df.empty:
            return f"📊 **{symbol.upper()}**\n\n❌ No current price data available."
        
        # Get current price
        current_price = df['Close'].iloc[-1]
        volume = df['Volume'].iloc[-1] if 'Volume' in df.columns else 0
        
        company_name = symbol.upper()
        market_cap = 0
        
        # Calculate change if possible
        if len(df) > 1:
            prev_price = df['Close'].iloc[-2]
            change = current_price - prev_price
            change_pct = (change / prev_price) * 100
            change_indicator = "📈" if change >= 0 else "📉"
        else:
            change = 0
            change_pct = 0
            change_indicator = "📊"
        
        return f"""
{change_indicator} **{symbol.upper()} - {company_name}**

💰 **Current Price**: ${current_price:.2f}
📊 **Change**: ${change:+.2f} ({change_pct:+.2f}%)
🏢 **Market Cap**: ${market_cap:,.0f}
📈 **Volume**: {volume:,.0f}
📅 **Data from**: {df.index[-1].strftime('%Y-%m-%d') if hasattr(df.index[-1], 'strftime') else 'Recent'}

*Powered by Polygon.io*
        """
        
    except Exception as e:
        return f"""
📊 **{symbol.upper()} Stock Lookup**

❌ **Error**: Unable to fetch real-time data
🔧 **Reason**: {str(e)[:100]}...

💡 **Try**: 
- Different stock symbol (AAPL, MSFT, GOOGL)
- Check if market is open
- Try again in a few moments
        """

def get_stock_news(symbol):
    """Get recent news for a stock - simplified version"""
    try:
        return f"📰 **Recent News for {symbol.upper()}**\n\nNews functionality temporarily unavailable. Please check financial news websites for the latest updates on {symbol.upper()}."
        
    except Exception as e:
        return f"Unable to fetch news for {symbol.upper()}: {str(e)}"

def get_market_summary():
    """Get overall market summary - simplified version"""
    try:
        return f"📊 **Market Summary**\n\nMarket data functionality temporarily unavailable. Please check financial news websites for current market conditions."
        
    except Exception as e:
        return f"Market data temporarily unavailable: {str(e)}"

def analyze_stock_performance(symbol, period="1mo"):
    """Analyze stock performance over a period"""
    try:
        client = PolygonClient()
        days_map = {"1mo": 30, "3mo": 90, "6mo": 180, "1y": 365}
        days = days_map.get(period, 30)
        
        df = client.get_stock_data(symbol, days=days)
        
        if not df.empty:
            start_price = df['Close'].iloc[0]
            end_price = df['Close'].iloc[-1]
            total_return = ((end_price - start_price) / start_price) * 100
            
            # Calculate volatility
            returns = df['Close'].pct_change().dropna()
            volatility = returns.std() * (252 ** 0.5) * 100  # Annualized volatility
            
            # Calculate moving averages
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            
            analysis = f"""
            Performance Analysis for {symbol.upper()} ({period}):
            
            Total Return: {total_return:.2f}%
            Annualized Volatility: {volatility:.2f}%
            Current Price: ${end_price:.2f}
            Period High: ${df['High'].max():.2f}
            Period Low: ${df['Low'].min():.2f}
            Average Volume: {df['Volume'].mean():,.0f}
            
            Technical Indicators:
            20-day MA: ${df['MA20'].iloc[-1]:.2f}
            50-day MA: ${df['MA50'].iloc[-1]:.2f}
            """
            
            return analysis
        else:
            return f"Could not fetch historical data for {symbol}"
    except Exception as e:
        return f"Error analyzing {symbol}: {str(e)}"

# Initialize tools
tools = [
    Tool(
        name="Get Stock Price",
        func=get_stock_price,
        description="Get current stock price and basic information for a given stock symbol"
    ),
    Tool(
        name="Get Stock News",
        func=get_stock_news,
        description="Get recent news articles for a specific stock symbol"
    ),
    Tool(
        name="Market Summary",
        func=get_market_summary,
        description="Get overall market summary including major indices"
    ),
    Tool(
        name="Analyze Stock Performance",
        func=analyze_stock_performance,
        description="Analyze stock performance and technical indicators for a given symbol"
    )
]

# Initialize session state
base.init_stock_advisor()
base.init_slidebar()

# Agent capabilities section
st.markdown("### 🛠️ Agent Capabilities")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="agent-card">
        <h4>📊 Real-time Data</h4>
        <p>Live stock prices, market indices, and trading volumes</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h4>📰 News Analysis</h4>
        <p>Latest financial news and market-moving events</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <h4>📈 Technical Analysis</h4>
        <p>Moving averages, volatility, and performance metrics</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="agent-card">
        <h4>🎯 Smart Insights</h4>
        <p>AI-powered analysis and investment recommendations</p>
    </div>
    """, unsafe_allow_html=True)

# Sample queries
st.markdown("### 💡 Try These Queries")
sample_queries = [
    "What's the current price of Apple (AAPL) and recent news?",
    "Analyze Tesla's performance over the last month",
    "Give me a market summary for today",
    "Compare Microsoft and Google stock performance",
    "What are the best performing tech stocks this week?",
    "Explain the current market trends"
]

cols = st.columns(3)
for i, query in enumerate(sample_queries):
    with cols[i % 3]:
        if st.button(query, key=f"sample_{i}"):
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

# Chat interface
st.markdown("### 💬 Chat with AI Agent")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=base.icons[message["role"]]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about stocks, market analysis, or investment advice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar=base.icons["user"]):
        st.write(prompt)

# Generate response with agent
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar=base.icons["assistant"]):
        st_callback = StreamlitCallbackHandler(st.container())
        
        # Get the user's prompt with safety check
        user_prompt = ""
        if st.session_state.messages and len(st.session_state.messages) > 0:
            last_message = st.session_state.messages[-1]
            if last_message and "content" in last_message:
                user_prompt = last_message["content"] or ""
        
        if not user_prompt:
            st.error("Please enter a valid question.")
            st.stop()
        
        # Initialize LLM and agent
        llm = init_bedrock()
        if llm:
            try:
                # Simple tool execution without complex agent
                if user_prompt and "price" in user_prompt.lower() and any(word in user_prompt.upper() for word in ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]):
                    # Extract symbol and get price
                    for symbol in ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]:
                        if symbol in user_prompt.upper():
                            response = get_stock_price(symbol)
                            break
                elif user_prompt and "news" in user_prompt.lower():
                    response = "Please specify a stock symbol for news lookup."
                elif user_prompt and "market" in user_prompt.lower():
                    response = get_market_summary()
                else:
                    # Enhanced prompt for AI assistant
                    enhanced_prompt = f"""
                    Context: AI Stock Assistant - Advanced Market Analysis & Investment Guidance
                    
                    Role: You are an expert AI stock assistant with deep knowledge of:
                    - Real-time market analysis and trends
                    - Company fundamentals and technical analysis  
                    - Portfolio optimization and risk management
                    - Economic indicators and market sentiment
                    
                    Task: Provide comprehensive stock market assistance
                    
                    Analysis Approach:
                    1. MARKET CONTEXT: Current market conditions and trends
                    2. STOCK ANALYSIS: Fundamental and technical evaluation
                    3. RISK ASSESSMENT: Identify potential risks and opportunities
                    4. STRATEGIC RECOMMENDATIONS: Actionable investment insights
                    5. PORTFOLIO IMPACT: How this fits into broader investment strategy
                    
                    Response Style:
                    - Professional yet accessible language
                    - Data-driven insights with specific examples
                    - Clear structure with headers and bullet points
                    - Balanced perspective showing multiple viewpoints
                    - Practical next steps for the investor
                    
                    User Query: {user_prompt if user_prompt else "General market inquiry"}
                    """
                    
                    # Use regular Bedrock for general queries
                    import libs as glib
                    response_stream = glib.call_claude_sonet_stream(enhanced_prompt)
                    response = ""
                    for chunk in response_stream:
                        response += chunk
                
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"I encountered an error: {str(e)}. Please try rephrasing your question."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            error_msg = "Unable to initialize AI model. Please check your AWS configuration."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🔧 **Powered by:** AWS Bedrock Claude 3.5 Sonnet | Yahoo Finance API | LangChain Agents")
