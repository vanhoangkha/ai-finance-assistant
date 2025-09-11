import pandas as pd

# Đọc SP500.csv (Vietnamese stocks)
sp500 = pd.read_csv('SP500.csv')
sp500.columns = sp500.columns.str.strip()
sp500['Symbol'] = sp500['Symbol'].str.strip()

# Đọc tickers.csv (Vietnamese stocks)
tickers = pd.read_csv('tickers.csv')

# Tạo danh sách hợp nhất
all_tickers = []

print("=== VIETNAMESE STOCKS ===")
# Thêm từ SP500 (Vietnamese stocks with .VN)
for _, row in sp500.iterrows():
    symbol = row['Symbol']  # Giữ nguyên .VN
    name = row['Name'].strip()
    sector = row['Sector'].strip()
    all_tickers.append(f"{symbol}|{name}|{sector}|VN")
    print(f"{symbol} - {name}")

# Thêm từ tickers (Vietnamese stocks)
for _, row in tickers.iterrows():
    symbol = row['company_ticker'] + '.VN'  # Thêm .VN
    name = row['company_name']
    all_tickers.append(f"{symbol}|{name}|Vietnam|VN")

print(f"\n=== US STOCKS (Sample) ===")
# Thêm một số cổ phiếu Mỹ phổ biến
us_stocks = [
    "AAPL|Apple Inc.|Technology|US",
    "GOOGL|Alphabet Inc.|Technology|US", 
    "MSFT|Microsoft Corporation|Technology|US",
    "AMZN|Amazon.com Inc.|Consumer Discretionary|US",
    "TSLA|Tesla Inc.|Consumer Discretionary|US",
    "META|Meta Platforms Inc.|Technology|US",
    "NVDA|NVIDIA Corporation|Technology|US",
    "JPM|JPMorgan Chase & Co.|Financial Services|US",
    "JNJ|Johnson & Johnson|Healthcare|US",
    "V|Visa Inc.|Financial Services|US"
]

for stock in us_stocks:
    all_tickers.append(stock)
    symbol = stock.split('|')[0]
    name = stock.split('|')[1]
    print(f"{symbol} - {name}")

# Ghi ra file
with open('all_tickers.txt', 'w', encoding='utf-8') as f:
    for ticker in all_tickers:
        f.write(ticker + '\n')

print(f"\n✅ Đã tạo all_tickers.txt với {len(all_tickers)} mã cổ phiếu")
print("Format: SYMBOL|COMPANY_NAME|SECTOR|COUNTRY")
