#!/usr/bin/env python3
"""
Update all_tickers.txt with top 10 US stocks at the beginning
"""

# Top 10 US stocks with verified data
TOP_10_STOCKS = [
    "AAPL|Apple Inc.|Technology|US",
    "GOOGL|Alphabet Inc.|Technology|US", 
    "MSFT|Microsoft Corporation|Technology|US",
    "AMZN|Amazon.com Inc.|Consumer Discretionary|US",
    "TSLA|Tesla Inc.|Consumer Discretionary|US",
    "META|Meta Platforms Inc.|Technology|US",
    "NVDA|NVIDIA Corporation|Technology|US"
]

def update_tickers():
    """Update all_tickers.txt with top 10 stocks at the beginning"""
    
    # Read existing tickers
    try:
        with open('all_tickers.txt', 'r') as f:
            existing_tickers = f.read().strip().split('\n')
    except FileNotFoundError:
        existing_tickers = []
    
    # Remove duplicates if they exist in the file
    filtered_tickers = []
    top_symbols = [stock.split('|')[0] for stock in TOP_10_STOCKS]
    
    for ticker in existing_tickers:
        if ticker and '|' in ticker:
            symbol = ticker.split('|')[0]
            if symbol not in top_symbols:
                filtered_tickers.append(ticker)
    
    # Combine: Top 10 first, then others
    new_tickers = TOP_10_STOCKS + filtered_tickers
    
    # Write updated file
    with open('all_tickers.txt', 'w') as f:
        f.write('\n'.join(new_tickers))
    
    print(f"✅ Updated all_tickers.txt")
    print(f"📊 Top 10 stocks added at the beginning")
    print(f"📈 Total tickers: {len(new_tickers)}")
    print(f"🔥 Top 10 US stocks:")
    for i, stock in enumerate(TOP_10_STOCKS, 1):
        symbol, name = stock.split('|')[:2]
        print(f"  {i:2d}. {symbol} - {name}")

if __name__ == "__main__":
    update_tickers()
