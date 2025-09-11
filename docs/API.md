# API Documentation

## Overview

AI Finance Assistant provides several APIs for financial data analysis and AI-powered insights.

## Stock Data API

### Get Stock Price
```python
from scripts.stock_data_client import StockDataClient

client = StockDataClient()
data = client.get_stock_data("AAPL", days=30)
```

### Parameters
- `symbol` (str): Stock ticker symbol
- `days` (int): Number of days of historical data

### Response
Returns pandas DataFrame with columns:
- `Open`: Opening price
- `High`: Highest price
- `Low`: Lowest price
- `Close`: Closing price
- `Volume`: Trading volume

## AI Analysis API

### Technical Analysis
```python
import libs as glib

prompt = "Analyze AAPL technical indicators..."
response = glib.call_claude_sonet_stream(prompt)
```

### Parameters
- `prompt` (str): Analysis request prompt

### Response
Returns streaming text response with AI analysis.

## Error Handling

All APIs return appropriate error messages:
- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Invalid API keys
- `429`: Rate Limited - Too many requests
- `500`: Internal Server Error

## Rate Limits

- Polygon API: 5 requests per minute (free tier)
- AWS Bedrock: 1000 requests per hour

## Authentication

Set environment variables:
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
POLYGON_API_KEY=your_polygon_key
```
