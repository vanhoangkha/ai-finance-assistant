import pandas as pd
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import boto3, json
import base
import sys
sys.path.append('scripts')
from stock_data_client import StockDataClient
import ta
import numpy as np

# Modern CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        text-align: center;
    }
    .analysis-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
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
    <h1>📈 Technical Analysis</h1>
    <p>Advanced stock technical analysis and charting</p>
</div>
""", unsafe_allow_html=True)

base.init_slidebar()

# Load all tickers data
def load_tickers():
    """Load tickers from all_tickers.txt"""
    tickers = []
    try:
        with open('/home/ubuntu/stock-assistant-main/all_tickers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 1:
                    symbol = parts[0].strip()
                    name = parts[1].strip() if len(parts) > 1 else symbol
                    country = parts[3].strip() if len(parts) > 3 else "Unknown"
                    tickers.append({"symbol": symbol, "name": name, "country": country})
    except FileNotFoundError:
        # Fallback tickers if file not found
        tickers = [
            {"symbol": "AAPL", "name": "Apple Inc.", "country": "US"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "country": "US"},
            {"symbol": "CTG.VN", "name": "Ngân hàng Công thương VN", "country": "VN"},
            {"symbol": "FPT.VN", "name": "Công ty FPT", "country": "VN"}
        ]
    return tickers

all_tickers = load_tickers()
symbols = [t["symbol"] for t in all_tickers]

# Sidebar controls
st.sidebar.markdown("### 🎛️ Analysis Controls")

# Create ticker options with names - prioritize US stocks
us_tickers = []
vn_tickers = []

for t in all_tickers:
    display_name = f"{t['symbol']} - {t['name']} [{t['country']}]"
    if t['country'] == 'US':
        us_tickers.append(display_name)
    else:
        vn_tickers.append(display_name)

# Combine with US stocks first
ticker_options = us_tickers + vn_tickers

# Default selection - prioritize AAPL
default_index = 0
for i, option in enumerate(ticker_options):
    if option.startswith('AAPL'):
        default_index = i
        break

selected_ticker = st.sidebar.selectbox('Select Stock Symbol', ticker_options, index=default_index)
ticker = selected_ticker.split(' - ')[0]  # Extract symbol from display name

analysis_type = st.sidebar.radio("Analysis Type", ('Technical Analysis', 'Fundamental Analysis'))
time_period = st.sidebar.selectbox('Time Period', ['1M', '3M', '6M', '1Y', '2Y', '5Y'], index=3)

# Convert time period to days
period_days = {'1M': 30, '3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '5Y': 1825}
history_days = period_days[time_period]

def get_stock_data(ticker, history=365):
    """Fetch stock data from appropriate source"""
    try:
        client = StockDataClient()
        df = client.get_stock_data(ticker, days=history)
        
        if df is None or df.empty:
            return None, None
        
        # Get real company info using yfinance
        info = None
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info_data = stock.info
            
            if info_data:
                info = {
                    "longName": info_data.get('longName', f"{ticker} Corporation"),
                    "sector": info_data.get('sector', 'N/A'), 
                    "industry": info_data.get('industry', 'N/A'),
                    "marketCap": info_data.get('marketCap', 0),
                    "trailingPE": info_data.get('trailingPE', 'N/A'),
                    "priceToBook": info_data.get('priceToBook', 'N/A'),
                    "dividendYield": info_data.get('dividendYield', 0),
                    "beta": info_data.get('beta', 'N/A'),
                    "website": info_data.get('website', 'N/A'),
                    "employees": info_data.get('fullTimeEmployees', 'N/A'),
                    "country": info_data.get('country', 'N/A'),
                    "currency": info_data.get('currency', 'USD')
                }
        except Exception as e:
            print(f"Error getting company info: {e}")
            # Fallback to basic info
            info = {
                "longName": f"{ticker}",
                "sector": "N/A", 
                "industry": "N/A",
                "marketCap": 0,
                "trailingPE": "N/A",
                "priceToBook": "N/A",
                "dividendYield": 0,
                "beta": "N/A"
            }
        
        return df, info
        
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None, None

def calculate_technical_indicators(df):
    """Calculate comprehensive technical indicators using TA library"""
    # Convert to numpy arrays for calculations
    high = df['High'].values
    low = df['Low'].values
    close = df['Close'].values
    volume = df['Volume'].values if 'Volume' in df.columns else None
    
    # Moving Averages
    df['SMA_20'] = ta.trend.sma_indicator(close=df['Close'], window=20)
    df['SMA_50'] = ta.trend.sma_indicator(close=df['Close'], window=50)
    df['SMA_200'] = ta.trend.sma_indicator(close=df['Close'], window=200)
    df['EMA_12'] = ta.trend.ema_indicator(close=df['Close'], window=12)
    df['EMA_26'] = ta.trend.ema_indicator(close=df['Close'], window=26)
    df['EMA_50'] = ta.trend.ema_indicator(close=df['Close'], window=50)
    
    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_Upper'] = bb.bollinger_hband()
    df['BB_Middle'] = bb.bollinger_mavg()
    df['BB_Lower'] = bb.bollinger_lband()
    df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
    df['BB_Percent'] = bb.bollinger_pband()
    
    # MACD
    macd = ta.trend.MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Histogram'] = macd.macd_diff()
    
    # RSI
    df['RSI'] = ta.momentum.rsi(close=df['Close'], window=14)
    df['RSI_30'] = ta.momentum.rsi(close=df['Close'], window=30)
    
    # Stochastic
    stoch = ta.momentum.StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'])
    df['STOCH_K'] = stoch.stoch()
    df['STOCH_D'] = stoch.stoch_signal()
    
    # Williams %R
    df['WILLR'] = ta.momentum.williams_r(high=df['High'], low=df['Low'], close=df['Close'])
    
    # ADX
    adx = ta.trend.ADXIndicator(high=df['High'], low=df['Low'], close=df['Close'])
    df['ADX'] = adx.adx()
    df['PLUS_DI'] = adx.adx_pos()
    df['MINUS_DI'] = adx.adx_neg()
    
    # ATR
    df['ATR'] = ta.volatility.average_true_range(high=df['High'], low=df['Low'], close=df['Close'])
    
    # CCI
    df['CCI'] = ta.trend.cci(high=df['High'], low=df['Low'], close=df['Close'])
    
    # ROC
    df['ROC'] = ta.momentum.roc(close=df['Close'], window=10)
    
    # Volume indicators (if volume available)
    if volume is not None and not pd.isna(volume).all():
        df['OBV'] = ta.volume.on_balance_volume(close=df['Close'], volume=df['Volume'])
        df['MFI'] = ta.volume.money_flow_index(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume'])
        df['Volume_SMA'] = ta.trend.sma_indicator(close=df['Volume'], window=20)
    
    # Support & Resistance
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['R1'] = 2 * df['Pivot'] - df['Low']
    df['S1'] = 2 * df['Pivot'] - df['High']
    df['R2'] = df['Pivot'] + (df['High'] - df['Low'])
    df['S2'] = df['Pivot'] - (df['High'] - df['Low'])
    
    return df

def plot_technical_chart(df, ticker):
    """Create comprehensive technical analysis charts"""
    # Create multiple chart tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Price & Overlays", "📊 Momentum", "📉 Volatility", "📦 Volume"])
    
    with tab1:
        # Price Action Chart
        fig1 = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{ticker} - Price Action & Moving Averages', 'MACD', 'ADX Trend Strength'),
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # Candlestick Chart
        fig1.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ), row=1, col=1)
        
        # Moving Averages
        fig1.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='orange')), row=1, col=1)
        fig1.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='red')), row=1, col=1)
        fig1.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], name='EMA 50', line=dict(color='purple')), row=1, col=1)
        
        # Bollinger Bands
        if 'BB_Upper' in df.columns:
            fig1.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper', line=dict(color='gray', dash='dash'), fill=None), row=1, col=1)
            fig1.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower', line=dict(color='gray', dash='dash'), fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1)
        
        # MACD
        fig1.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')), row=2, col=1)
        fig1.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='red')), row=2, col=1)
        if 'MACD_Histogram' in df.columns:
            fig1.add_trace(go.Bar(x=df.index, y=df['MACD_Histogram'], name='MACD Histogram', marker_color='green'), row=2, col=1)
        
        # ADX
        if 'ADX' in df.columns:
            fig1.add_trace(go.Scatter(x=df.index, y=df['ADX'], name='ADX', line=dict(color='purple')), row=3, col=1)
            fig1.add_hline(y=25, line_dash="dash", line_color="orange", row=3, col=1)
        
        fig1.update_layout(height=800, showlegend=True, title_text=f"Price Action Analysis - {ticker}")
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        # Momentum Indicators Chart
        fig2 = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('RSI (14 & 30)', 'Stochastic Oscillator', 'Williams %R', 'Rate of Change'),
            row_heights=[0.25, 0.25, 0.25, 0.25]
        )
        
        # RSI
        fig2.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI 14', line=dict(color='purple')), row=1, col=1)
        if 'RSI_30' in df.columns:
            fig2.add_trace(go.Scatter(x=df.index, y=df['RSI_30'], name='RSI 30', line=dict(color='blue')), row=1, col=1)
        fig2.add_hline(y=70, line_dash="dash", line_color="red", row=1, col=1)
        fig2.add_hline(y=30, line_dash="dash", line_color="green", row=1, col=1)
        
        # Stochastic
        if 'STOCH_K' in df.columns:
            fig2.add_trace(go.Scatter(x=df.index, y=df['STOCH_K'], name='%K', line=dict(color='blue')), row=2, col=1)
            fig2.add_trace(go.Scatter(x=df.index, y=df['STOCH_D'], name='%D', line=dict(color='red')), row=2, col=1)
            fig2.add_hline(y=80, line_dash="dash", line_color="red", row=2, col=1)
            fig2.add_hline(y=20, line_dash="dash", line_color="green", row=2, col=1)
        
        # Williams %R
        if 'WILLR' in df.columns:
            fig2.add_trace(go.Scatter(x=df.index, y=df['WILLR'], name='Williams %R', line=dict(color='orange')), row=3, col=1)
            fig2.add_hline(y=-20, line_dash="dash", line_color="red", row=3, col=1)
            fig2.add_hline(y=-80, line_dash="dash", line_color="green", row=3, col=1)
        
        # Rate of Change
        if 'ROC' in df.columns:
            fig2.add_trace(go.Scatter(x=df.index, y=df['ROC'], name='ROC', line=dict(color='green')), row=4, col=1)
            fig2.add_hline(y=0, line_dash="dash", line_color="gray", row=4, col=1)
        
        fig2.update_layout(height=800, showlegend=True, title_text=f"Momentum Analysis - {ticker}")
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        # Volatility Chart
        fig3 = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{ticker} - Bollinger Bands & Keltner Channels', 'Average True Range (ATR)', 'Bollinger Band Width & %B'),
            row_heights=[0.5, 0.25, 0.25]
        )
        
        # Price with Bollinger Bands and Keltner Channels
        fig3.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close', line=dict(color='black')), row=1, col=1)
        if 'BB_Upper' in df.columns:
            fig3.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper', line=dict(color='blue', dash='dash')), row=1, col=1)
            fig3.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower', line=dict(color='blue', dash='dash')), row=1, col=1)
        
        # ATR
        if 'ATR' in df.columns:
            fig3.add_trace(go.Scatter(x=df.index, y=df['ATR'], name='ATR', line=dict(color='orange')), row=2, col=1)
        
        # Bollinger Band Width and %B
        if 'BB_Width' in df.columns:
            fig3.add_trace(go.Scatter(x=df.index, y=df['BB_Width'], name='BB Width', line=dict(color='green')), row=3, col=1)
        if 'BB_Percent' in df.columns:
            fig3.add_trace(go.Scatter(x=df.index, y=df['BB_Percent'], name='%B', line=dict(color='purple')), row=3, col=1)
            fig3.add_hline(y=1, line_dash="dash", line_color="red", row=3, col=1)
            fig3.add_hline(y=0, line_dash="dash", line_color="green", row=3, col=1)
        
        fig3.update_layout(height=800, showlegend=True, title_text=f"Volatility Analysis - {ticker}")
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab4:
        # Volume Analysis Chart
        if 'Volume' in df.columns and not df['Volume'].isna().all():
            fig4 = make_subplots(
                rows=3, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=(f'{ticker} - Price & Volume', 'On Balance Volume (OBV)', 'Money Flow Index (MFI)'),
                row_heights=[0.4, 0.3, 0.3]
            )
            
            # Price and Volume
            fig4.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close', line=dict(color='blue')), row=1, col=1)
            fig4.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='lightblue', yaxis='y2'), row=1, col=1)
            
            # OBV
            if 'OBV' in df.columns:
                fig4.add_trace(go.Scatter(x=df.index, y=df['OBV'], name='OBV', line=dict(color='green')), row=2, col=1)
            
            # MFI
            if 'MFI' in df.columns:
                fig4.add_trace(go.Scatter(x=df.index, y=df['MFI'], name='MFI', line=dict(color='purple')), row=3, col=1)
                fig4.add_hline(y=80, line_dash="dash", line_color="red", row=3, col=1)
                fig4.add_hline(y=20, line_dash="dash", line_color="green", row=3, col=1)
            
            # Remove CMF section as it's not calculated
            fig4.update_layout(height=600, showlegend=True, title_text=f"Volume Analysis - {ticker}")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("📦 Volume data not available for this ticker")
    
    return None

# Main content
if ticker:
    df, stock_info = get_stock_data(ticker, history_days)
    
    if df is not None and not df.empty:
        # Calculate indicators
        df = calculate_technical_indicators(df)
        
        # Current price metrics
        current_price = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2]
        price_change = current_price - prev_close
        price_change_pct = (price_change / prev_close) * 100
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>${current_price:.2f}</h3>
                <p>Current Price</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            color = "green" if price_change >= 0 else "red"
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: {color}">{price_change:+.2f}</h3>
                <p>Price Change</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: {color}">{price_change_pct:+.2f}%</h3>
                <p>% Change</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            volume = df['Volume'].iloc[-1]
            st.markdown(f"""
            <div class="metric-card">
                <h3>{volume:,.0f}</h3>
                <p>Volume</p>
            </div>
            """, unsafe_allow_html=True)
        
        if analysis_type == 'Technical Analysis':
            # Technical Analysis Section
            st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
            st.markdown("### 📊 Technical Analysis Dashboard")
            
            # Display comprehensive technical charts
            plot_technical_chart(df, ticker)
            
            # Technical indicators summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 📈 Moving Averages")
                sma_20 = df['SMA_20'].iloc[-1]
                sma_50 = df['SMA_50'].iloc[-1]
                
                if current_price > sma_20:
                    st.success(f"✅ Price above SMA 20: ${sma_20:.2f}")
                    sma_20_signal = "BULLISH"
                else:
                    st.warning(f"⚠️ Price below SMA 20: ${sma_20:.2f}")
                    sma_20_signal = "BEARISH"
                
                if current_price > sma_50:
                    st.success(f"✅ Price above SMA 50: ${sma_50:.2f}")
                    sma_50_signal = "BULLISH"
                else:
                    st.warning(f"⚠️ Price below SMA 50: ${sma_50:.2f}")
                    sma_50_signal = "BEARISH"
                
                # Golden Cross / Death Cross
                if sma_20 > sma_50:
                    st.info("🟡 Golden Cross Pattern")
                else:
                    st.error("🔴 Death Cross Pattern")
            
            with col2:
                st.markdown("#### 📊 Momentum Indicators")
                rsi = df['RSI'].iloc[-1]
                macd = df['MACD'].iloc[-1]
                macd_signal = df['MACD_Signal'].iloc[-1]
                
                # RSI Analysis
                if rsi > 70:
                    st.warning(f"🔴 RSI: {rsi:.2f} (Overbought)")
                    rsi_signal = "SELL"
                elif rsi < 30:
                    st.success(f"🟢 RSI: {rsi:.2f} (Oversold)")
                    rsi_signal = "BUY"
                else:
                    st.info(f"🟡 RSI: {rsi:.2f} (Neutral)")
                    rsi_signal = "HOLD"
                
                # MACD Analysis
                if macd > macd_signal:
                    st.success(f"🟢 MACD: {macd:.4f} (Bullish)")
                    macd_signal_trend = "BULLISH"
                else:
                    st.warning(f"🔴 MACD: {macd:.4f} (Bearish)")
                    macd_signal_trend = "BEARISH"
            
            with col3:
                st.markdown("#### 🎯 Trading Signals")
                
                # Overall Signal Calculation
                signals = []
                if sma_20_signal == "BULLISH": signals.append(1)
                else: signals.append(-1)
                
                if sma_50_signal == "BULLISH": signals.append(1)
                else: signals.append(-1)
                
                if rsi_signal == "BUY": signals.append(1)
                elif rsi_signal == "SELL": signals.append(-1)
                else: signals.append(0)
                
                if macd_signal_trend == "BULLISH": signals.append(1)
                else: signals.append(-1)
                
                overall_score = sum(signals)
                
                if overall_score >= 2:
                    st.success("🚀 **STRONG BUY**")
                    st.success(f"Signal Score: {overall_score}/4")
                elif overall_score == 1:
                    st.info("📈 **BUY**")
                    st.info(f"Signal Score: {overall_score}/4")
                elif overall_score == 0:
                    st.warning("⏸️ **HOLD**")
                    st.warning(f"Signal Score: {overall_score}/4")
                elif overall_score == -1:
                    st.warning("📉 **SELL**")
                    st.warning(f"Signal Score: {overall_score}/4")
                else:
                    st.error("💥 **STRONG SELL**")
                    st.error(f"Signal Score: {overall_score}/4")
                
                # Support & Resistance Levels
                st.markdown("#### 📏 Key Levels")
                recent_high = df['High'].tail(20).max()
                recent_low = df['Low'].tail(20).min()
                
                st.write(f"**Resistance**: ${recent_high:.2f}")
                st.write(f"**Support**: ${recent_low:.2f}")
                
                # Price distance from levels
                resistance_distance = ((recent_high - current_price) / current_price) * 100
                support_distance = ((current_price - recent_low) / current_price) * 100
                
                st.write(f"Distance to Resistance: {resistance_distance:.1f}%")
                st.write(f"Distance from Support: {support_distance:.1f}%")
            
            # AI Analysis Section using Bedrock
            st.markdown("### 🤖 AI Technical Analysis")
            
            # Safe formatting for indicators
            rsi_str = f"{rsi:.2f}" if rsi is not None else "N/A"
            macd_str = f"{macd:.4f}" if macd is not None else "N/A"
            macd_signal_str = f"{macd_signal:.4f}" if macd_signal is not None else "N/A"
            sma20_str = f"${sma_20:.2f}" if sma_20 is not None else "N/A"
            sma50_str = f"${sma_50:.2f}" if sma_50 is not None else "N/A"
            
            # Create AI analysis prompt
            ai_prompt = f"""
            Analyze the technical indicators for {ticker} and provide professional trading insights:
            
            CURRENT DATA:
            • Price: ${current_price:.2f}
            • RSI: {rsi_str}
            • MACD: {macd_str} (Signal: {macd_signal_str})
            • SMA20: {sma20_str} | SMA50: {sma50_str}
            • Support: ${recent_low:.2f} | Resistance: ${recent_high:.2f}
            • Signal Score: {overall_score}/4
            
            ANALYSIS FRAMEWORK:
            1. TREND ANALYSIS: Evaluate price trend and momentum
            2. INDICATOR CONFLUENCE: How indicators align or diverge
            3. RISK ASSESSMENT: Key support/resistance levels
            4. ENTRY/EXIT STRATEGY: Optimal timing and price levels
            5. MARKET OUTLOOK: Short-term and medium-term perspective
            
            Provide a comprehensive technical analysis in ENGLISH with specific price targets and risk management advice.
            Use professional financial terminology and provide actionable insights for traders.
            """
            
            if st.button("🔍 Generate AI Analysis", use_container_width=True):
                with st.spinner("🤖 AI đang phân tích kỹ thuật..."):
                    try:
                        import libs as glib
                        response = glib.call_claude_sonet_stream(ai_prompt)
                        
                        st.markdown("#### 🎯 Phân Tích Kỹ Thuật AI")
                        analysis_placeholder = st.empty()
                        full_analysis = ""
                        
                        for chunk in response:
                            full_analysis += chunk
                            analysis_placeholder.markdown(full_analysis)
                            
                    except Exception as e:
                        st.error(f"Lỗi khi tạo phân tích AI: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Fundamental Analysis Section
            st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
            st.markdown("### 💼 Fundamental Analysis")
            
            if stock_info:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 🏢 Company Information")
                    st.write(f"**Company:** {stock_info.get('longName', 'N/A')}")
                    st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
                    st.write(f"**Industry:** {stock_info.get('industry', 'N/A')}")
                    st.write(f"**Country:** {stock_info.get('country', 'N/A')}")
                    if stock_info.get('employees') != 'N/A' and stock_info.get('employees'):
                        st.write(f"**Employees:** {stock_info.get('employees'):,}")
                
                with col2:
                    st.markdown("#### 📊 Key Ratios")
                    pe_ratio = stock_info.get('trailingPE', 'N/A')
                    if pe_ratio != 'N/A' and pe_ratio:
                        st.write(f"**P/E Ratio:** {pe_ratio:.2f}")
                    else:
                        st.write("**P/E Ratio:** N/A")
                    
                    pb_ratio = stock_info.get('priceToBook', 'N/A')
                    if pb_ratio != 'N/A' and pb_ratio:
                        st.write(f"**P/B Ratio:** {pb_ratio:.2f}")
                    else:
                        st.write("**P/B Ratio:** N/A")
                    
                    div_yield = stock_info.get('dividendYield', 0)
                    if div_yield and div_yield > 0:
                        st.write(f"**Dividend Yield:** {div_yield*100:.2f}%")
                    else:
                        st.write("**Dividend Yield:** N/A")
                    
                    beta = stock_info.get('beta', 'N/A')
                    if beta != 'N/A' and beta:
                        st.write(f"**Beta:** {beta:.2f}")
                    else:
                        st.write("**Beta:** N/A")
                
                with col3:
                    st.markdown("#### 💰 Market Data")
                    market_cap = stock_info.get('marketCap', 0)
                    if market_cap and market_cap > 0:
                        if market_cap >= 1e12:
                            st.write(f"**Market Cap:** ${market_cap/1e12:.2f}T")
                        elif market_cap >= 1e9:
                            st.write(f"**Market Cap:** ${market_cap/1e9:.2f}B")
                        elif market_cap >= 1e6:
                            st.write(f"**Market Cap:** ${market_cap/1e6:.2f}M")
                        else:
                            st.write(f"**Market Cap:** ${market_cap:,.0f}")
                    else:
                        st.write("**Market Cap:** N/A")
                    
                    st.write(f"**Currency:** {stock_info.get('currency', 'USD')}")
                    
                    website = stock_info.get('website', 'N/A')
                    if website != 'N/A' and website:
                        st.write(f"**Website:** [{website}]({website})")
                    
                    # Price analysis
                    if df is not None and not df.empty:
                        current_price = df['Close'].iloc[-1]
                        high_52w = df['High'].tail(252).max() if len(df) >= 252 else df['High'].max()
                        low_52w = df['Low'].tail(252).min() if len(df) >= 252 else df['Low'].min()
                        
                        st.markdown("#### 📈 Price Analysis")
                        st.write(f"**Current Price:** ${current_price:.2f}")
                        st.write(f"**52W High:** ${high_52w:.2f}")
                        st.write(f"**52W Low:** ${low_52w:.2f}")
                        
                        # Distance from highs/lows
                        pct_from_high = ((current_price - high_52w) / high_52w) * 100
                        pct_from_low = ((current_price - low_52w) / low_52w) * 100
                        
                        if pct_from_high >= -5:
                            st.success(f"📈 Near 52W High ({pct_from_high:+.1f}%)")
                        elif pct_from_low <= 5:
                            st.error(f"📉 Near 52W Low ({pct_from_low:+.1f}%)")
                        else:
                            st.info(f"📊 {pct_from_high:+.1f}% from High, {pct_from_low:+.1f}% from Low")
            else:
                st.warning("⚠️ Fundamental data not available for this ticker")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.error(f"Unable to fetch data for {ticker}. Please try another symbol.")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Use the sidebar to change analysis parameters and explore different stocks!")
