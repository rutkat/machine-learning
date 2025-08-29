# data_collector.py - GameFi token data collection
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

class GameFiDataCollector:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        
    def fetch_token_metrics(self, token_address, days=30):
        """
        Fetch comprehensive token metrics for GameFi analysis
        Returns: Dictionary with price, volume, and supply data
        """
        # Price and volume data from CoinGecko
        price_data = self._get_price_history(token_address, days)
        
        # On-chain metrics from blockchain
        supply_data = self._get_supply_metrics(token_address)
        
        # Gaming-specific metrics
        gaming_metrics = self._get_gaming_metrics(token_address)
        
        return {
            'price_history': price_data,
            'supply_metrics': supply_data,
            'gaming_metrics': gaming_metrics,
            'collected_at': datetime.now()
        }
    
    def _get_price_history(self, token_address, days):
        """Fetch historical price and volume data"""
        url = f"https://api.coingecko.com/api/v3/coins/{token_address}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Convert to pandas DataFrame for easier analysis
            df = pd.DataFrame({
                'timestamp': [pd.to_datetime(item[0], unit='ms') for item in data['prices']],
                'price': [item[1] for item in data['prices']],
                'volume': [item[1] for item in data['total_volumes']]
            })
            
            return df
        
        return None
    
    def _get_supply_metrics(self, token_address):
        """Fetch token supply and distribution metrics"""
        # This would connect to blockchain APIs or smart contract calls
        # For demonstration, we'll use mock data structure
        return {
            'total_supply': 1000000000,
            'circulating_supply': 350000000,
            'burned_tokens': 50000000,
            'staked_tokens': 200000000,
            'treasury_balance': 400000000,
            'daily_emissions': 1000000
        }
    
    def _get_gaming_metrics(self, token_address):
        """Fetch gaming-specific metrics"""
        # This would integrate with gaming platform APIs
        return {
            'daily_active_users': 15000,
            'monthly_active_users': 75000,
            'average_session_time': 45,  # minutes
            'tokens_earned_per_hour': 50,
            'new_user_acquisition': 500,  # daily
            'user_retention_7d': 0.35,
            'user_retention_30d': 0.15
        }

# Usage example
collector = GameFiDataCollector(config)
token_data = collector.fetch_token_metrics('axie-infinity')


