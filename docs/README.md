# Overview Stock-Assistant
This is a simple demo of Amazon Bedrock and Anthropic Claude 3 Sonnet model with langchain and streamlit. For more detail please reference the following link: <br />
- <a href="https://aws.amazon.com/bedrock/" target="_blank">https://aws.amazon.com/bedrock/ </a>
- <a href="https://www.anthropic.com/news/claude-3-family" target="_blank">Claude 3 </a>

# Features
- **Chat**: AI-powered conversation with Claude 3 Sonnet
- **Document Summary**: Summarize documents in Vietnamese
- **Document Q&A**: Ask questions about uploaded documents
- **Technical Analysis**: Stock technical analysis with Polygon.io API
- **Stock Information**: Real-time stock data and information
- **Stock Assistant**: AI stock advisor with market insights

# Data Sources
- **Stock Data**: Polygon.io API (replaces Yahoo Finance)
- **Ticker Reference**: Combined SP500.csv + tickers.csv → all_tickers.txt (1,626 stocks)
- **Market Analysis**: Amazon Bedrock Knowledge Base

# To Setup

## Environment Variables
Create `.env` file:
```
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
POLYGON_API_KEY=your_polygon_api_key
```

## Local Development
```bash
git clone
cd stock-assistant
pip3 install -r requirements.txt
streamlit run main.py --server.port 8501
```

## Docker Compose (Recommended)
```bash
git pull
docker compose up -d
```

Access:
- **Streamlit**: http://localhost:8501
- **Nginx**: http://localhost

# Architecture
![Architecture](./architecture.png)

# API Integration
- **Polygon.io**: Real-time and historical stock data
- **Amazon Bedrock**: Claude 3 Sonnet for AI responses
- **AWS Knowledge Base**: Financial market insights

# Files Structure
- `polygon_client.py`: Polygon.io API integration
- `all_tickers.txt`: Combined stock ticker reference (1,626 stocks)
- `ticker_lookup.py`: Stock symbol search functionality
- `pages/`: Streamlit pages for different features

# Learn more about prompt and Claude 3
<a href="https://docs.anthropic.com/claude/docs/introduction-to-prompt-design" target="_blank">Introduction to prompt design </a>
<a href="https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf">Model Card</a>