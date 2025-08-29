# config.py - Configuration for data sources
import os

# API Configuration
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
DEXTOOLS_API_KEY = os.getenv('DEXTOOLS_API_KEY')
DEFILLAMA_API_URL = "https://api.llama.fi"

# Ollama Configuration
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama2:13b"

# Analysis Parameters
ANALYSIS_TIMEFRAME = 30  # Days
MIN_DAILY_VOLUME = 10000  # USD
MIN_MARKET_CAP = 1000000  # USD



