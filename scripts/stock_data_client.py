import yfinance as yf
import pandas as pd
from polygon_client import PolygonClient
import streamlit as st
try:
    from vnstock import Vnstock
except ImportError:
    Vnstock = None

class StockDataClient:
    def __init__(self):
        self.polygon_client = PolygonClient()
        
    def is_vietnamese_stock(self, ticker):
        """Check if ticker is Vietnamese stock"""
        return ticker.endswith('.VN')
    
    def get_stock_data(self, ticker, days=365):
        """Get stock data from appropriate source"""
        try:
            if self.is_vietnamese_stock(ticker):
                return self._get_vnstock_data(ticker, days)
            else:
                return self._get_polygon_data(ticker, days)
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            return None
    
    def _get_vnstock_data(self, ticker, days):
        """Get data from vnstock for Vietnamese stocks"""
        try:
            if Vnstock is None:
                return self._get_yahoo_data(ticker, days)
                
            # Remove .VN suffix for vnstock
            clean_ticker = ticker.replace('.VN', '')
            
            # Use new vnstock API
            stock = Vnstock().stock(symbol=clean_ticker, source='VCI')
            df = stock.quote.history(start='2023-01-01', end='2024-12-31')
            
            if df is None or df.empty:
                # Fallback to Yahoo Finance
                return self._get_yahoo_data(ticker, days)
                
            # Rename columns to match standard format
            column_mapping = {
                'open': 'Open',
                'high': 'High', 
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume',
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low', 
                'Close': 'Close',
                'Volume': 'Volume'
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            # Ensure we have the right columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in df.columns:
                    df[col] = 0
            
            return df[required_cols].tail(days)
            
        except Exception as e:
            print(f"vnstock error: {e}")
            # Fallback to Yahoo Finance
            return self._get_yahoo_data(ticker, days)
    
    def _get_yahoo_data(self, ticker, days):
        """Get data from Yahoo Finance for Vietnamese stocks"""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=f"{days}d")
            
            if df.empty:
                return None
                
            # Rename columns to match standard format
            df = df.rename(columns={
                'Open': 'Open',
                'High': 'High', 
                'Low': 'Low',
                'Close': 'Close',
                'Volume': 'Volume'
            })
            
            return df
            
        except Exception as e:
            print(f"Yahoo Finance error: {e}")
            return None
    
    def _get_polygon_data(self, ticker, days):
        """Get data from Polygon.io for US stocks"""
        try:
            return self.polygon_client.get_stock_data(ticker, days)
        except Exception as e:
            print(f"Polygon error: {e}")
            return None
