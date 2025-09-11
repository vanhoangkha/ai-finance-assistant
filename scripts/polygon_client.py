import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class PolygonClient:
    def __init__(self):
        self.api_key = os.getenv('POLYGON_API_KEY', 'VrfSOcc5LpOqortTXVDZuxqP6QWhVfVJ')
        self.base_url = 'https://api.polygon.io'
    
    def get_stock_data(self, symbol, days=30):
        """Get stock data for the specified number of days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/1/day/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
        params = {'apikey': self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                df = pd.DataFrame(data['results'])
                df['Date'] = pd.to_datetime(df['t'], unit='ms')
                df = df.rename(columns={
                    'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume'
                })
                df.set_index('Date', inplace=True)
                return df[['Open', 'High', 'Low', 'Close', 'Volume']]
        return pd.DataFrame()
    
    def get_current_price(self, symbol):
        """Get current stock price"""
        url = f"{self.base_url}/v2/last/trade/{symbol}"
        params = {'apikey': self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                return data['results']['p']
        return None
