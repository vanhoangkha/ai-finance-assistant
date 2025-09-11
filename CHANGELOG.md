# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- AI Technical Analysis with AWS Bedrock integration
- Top 10 US stocks data integration from Polygon.io
- Professional project structure with organized directories
- Comprehensive error handling and validation
- Docker containerization with Nginx reverse proxy

### Changed
- Reorganized project structure into logical directories
- Updated import paths for better modularity
- Enhanced technical analysis with AI insights
- Improved error messages and user feedback

### Fixed
- Fixed NoneType concatenation errors in AI analysis
- Resolved format specifier issues with None values
- Fixed import path issues after restructuring
- Corrected Docker build context and paths

## [1.0.0] - 2024-09-11

### Added
- Initial release of AI Finance Assistant
- Streamlit-based web interface
- AWS Bedrock integration for AI analysis
- Polygon.io API integration for real-time stock data
- Technical analysis with multiple indicators (RSI, MACD, SMA, Bollinger Bands)
- Stock information and fundamental analysis
- Document summarization and Q&A features
- Chat interface for financial consultation
- Docker deployment configuration
- Nginx reverse proxy setup

### Features
- **Technical Analysis**: Real-time charts with technical indicators
- **AI Assistant**: Advanced stock analysis with AI tools
- **Stock Information**: Comprehensive stock data and metrics
- **Document Analysis**: PDF/text summarization and Q&A
- **Chat Interface**: General financial consultation

### Technical
- Python 3.10+ support
- Streamlit framework
- AWS Bedrock Claude Sonnet integration
- Polygon.io API for market data
- Docker containerization
- Nginx reverse proxy
- Health checks and monitoring
