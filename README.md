# 🚀 AI Finance Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A comprehensive AI-powered financial analysis platform built with Streamlit and AWS Bedrock, providing real-time stock analysis, technical indicators, and AI-driven insights.

## ✨ Features

### 💬 AI Chat Interface
- General financial consultation with AWS Bedrock Claude Sonnet
- Natural language processing for financial queries
- Context-aware responses with market insights

### 📈 Advanced Technical Analysis
- Real-time stock charts with interactive indicators
- RSI, MACD, Moving Averages, Bollinger Bands
- **AI-powered technical analysis** with professional insights
- Support/Resistance level identification
- Trading signals and recommendations

### 💹 Comprehensive Stock Information
- Real-time stock data from Polygon.io
- Company fundamentals and financial ratios
- Market performance analysis
- Top 10 US stocks integration

### 🤖 Intelligent AI Assistant
- Advanced stock analysis with AI tools
- Real-time price fetching and market summaries
- Professional trading insights and recommendations

### 📄 Document Intelligence
- PDF/text document summarization
- Document Q&A with AI
- URL content analysis and insights

## 🏗️ Architecture

```
ai-finance-assistant/
├── 📱 app.py                 # Main Streamlit application
├── 🧠 base.py                # Core functions and configurations
├── 📊 libs.py                # AWS Bedrock and utility libraries
├── 📄 pages/                 # Streamlit pages
├── 📊 data/                  # Stock data and CSV files
├── 🔧 scripts/              # Utility scripts and API clients
├── ⚙️ config/               # Configuration and Docker files
└── 📚 docs/                 # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- AWS Account with Bedrock access
- Polygon.io API key
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/vanhoangkha/ai-finance-assistant.git
cd ai-finance-assistant
```

2. **Set up environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

3. **Install dependencies**
```bash
# Production
pip install -r requirements.txt

# Development
pip install -r requirements-dev.txt
```

### Running the Application

#### Option 1: Local Development
```bash
streamlit run app.py
```

#### Option 2: Docker (Recommended)
```bash
# Build and run
make docker-run

# Or manually
docker compose -f config/docker-compose.yml up -d
```

#### Option 3: Using Makefile
```bash
# See all available commands
make help

# Run locally
make run

# Run with Docker
make docker-run
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# AWS Configuration
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Polygon.io API
POLYGON_API_KEY=your_polygon_api_key

# Optional Settings
STREAMLIT_SERVER_PORT=8501
DEBUG=false
```

### Required APIs

1. **AWS Bedrock**: For AI analysis and chat functionality
   - Enable Claude Sonnet model access
   - Configure IAM permissions

2. **Polygon.io**: For real-time stock data
   - Free tier available with rate limits
   - Paid plans for higher limits

## 📊 Data Management

### Fetch Latest Stock Data
```bash
# Fetch top 10 US stocks data
python scripts/fetch_top10_stocks.py

# Update ticker list
python scripts/update_top10_tickers.py

# Or use Makefile
make fetch-data
make update-tickers
```

### Supported Stocks

**Top 10 US Stocks** (prioritized):
- AAPL (Apple Inc.)
- GOOGL (Alphabet Inc.)
- MSFT (Microsoft Corporation)
- AMZN (Amazon.com Inc.)
- TSLA (Tesla Inc.)
- META (Meta Platforms Inc.)
- NVDA (NVIDIA Corporation)

## 🐳 Docker Deployment

### Development
```bash
docker compose -f config/docker-compose.yml up -d
```

### Production
```bash
# Build optimized image
docker compose -f config/docker-compose.yml build --no-cache

# Run with resource limits
docker compose -f config/docker-compose.yml up -d
```

### Health Monitoring
```bash
# Check container status
docker compose -f config/docker-compose.yml ps

# View logs
docker compose -f config/docker-compose.yml logs -f
```

## 🧪 Development

### Setup Development Environment
```bash
# Install development dependencies
make install-dev

# Set up pre-commit hooks
make dev-setup

# Run in development mode
make dev-run
```

### Code Quality
```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test
```

### Project Structure
- **Modular Design**: Separated concerns with clear boundaries
- **Error Handling**: Comprehensive error handling and validation
- **Type Safety**: Type hints and validation where applicable
- **Documentation**: Inline documentation and docstrings

## 📱 Usage

1. **Access the application**: http://localhost:8501
2. **Select analysis type**: Technical Analysis or Stock Information
3. **Choose stock symbol**: From dropdown or search
4. **Generate AI insights**: Click "Generate AI Analysis"
5. **Explore features**: Chat, document analysis, and more

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run quality checks: `make lint test`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AWS Bedrock** for AI capabilities
- **Polygon.io** for market data
- **Streamlit** for the web framework
- **Technical Analysis Library** for indicators

## 📞 Support

- 📧 Email: contact@ai-finance-assistant.com
- 🐛 Issues: [GitHub Issues](https://github.com/vanhoangkha/ai-finance-assistant/issues)
- 📖 Documentation: [Wiki](https://github.com/vanhoangkha/ai-finance-assistant/wiki)

---

**⚠️ Disclaimer**: This tool is for educational and informational purposes only. Not financial advice. Always consult with qualified financial professionals before making investment decisions.

**Built with ❤️ using Streamlit, AWS Bedrock, and Polygon.io**
