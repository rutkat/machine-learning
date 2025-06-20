#
# Polars, a lightning-fast DataFrame library designed for optimal performance and scalability
#

import polars as pl
import numpy as np
from datetime import datetime, timedelta
import io

print("Polars Pipeline")

# generate records with stock tickers
np.random.seed(42)
n_records = 100000
dates = [datetime(2024, 1, 1) + timedelta(days=i//100) for i in range(n_records)]
tickers = np.random.choice(['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'], n_records)

# mock data
data = {
    'timestamp': dates,
    'ticker': tickers,
    'price': np.random.lognormal(4, 0.3, n_records),
    'volume': np.random.exponential(1000000, n_records).astype(int),
    'bid_ask_spread': np.random.exponential(0.01, n_records),
    'market_cap': np.random.lognormal(25, 1, n_records),
    'sector': np.random.choice(['Tech', 'Finance', 'Healthcare', 'Energy'], n_records)
}

print(f"Generated {n_records:,} mock stock records.")

# load data
lf = pl.LazyFrame(data)

result = (
    lf
    .with_columns([
        pl.col('timestamp').dt.year().alias('year'),
        pl.col('timestamp').dt.month().alias('month'),
        pl.col('timestamp').dt.weekday().alias('weekday'),
        pl.col('timestamp').dt.quarter().alias('quarter')
    ])
   
    .with_columns([
        pl.col('price').rolling_mean(20).over('ticker').alias('sma_20'),
        pl.col('price').rolling_std(20).over('ticker').alias('volatility_20'),
       
        pl.col('price').ewm_mean(span=12).over('ticker').alias('ema_12'),
       
        pl.col('price').diff().alias('price_diff'),
       
        (pl.col('volume') * pl.col('price')).alias('dollar_volume')
    ])
   
    .with_columns([
        pl.col('price_diff').clip(0, None).rolling_mean(14).over('ticker').alias('rsi_up'),
        pl.col('price_diff').abs().rolling_mean(14).over('ticker').alias('rsi_down'),
       
        (pl.col('price') - pl.col('sma_20')).alias('bb_position')
    ])
   
    .with_columns([
        (100 - (100 / (1 + pl.col('rsi_up') / pl.col('rsi_down')))).alias('rsi')
    ])
   
    .filter(
        (pl.col('price') > 10) &
        (pl.col('volume') > 100000) &
        (pl.col('sma_20').is_not_null())
    )
   
    .group_by(['ticker', 'year', 'quarter'])
    .agg([
        pl.col('price').mean().alias('avg_price'),
        pl.col('price').std().alias('price_volatility'),
        pl.col('price').min().alias('min_price'),
        pl.col('price').max().alias('max_price'),
        pl.col('price').quantile(0.5).alias('median_price'),
       
        pl.col('volume').sum().alias('total_volume'),
        pl.col('dollar_volume').sum().alias('total_dollar_volume'),
       
        pl.col('rsi').filter(pl.col('rsi').is_not_null()).mean().alias('avg_rsi'),
        pl.col('volatility_20').mean().alias('avg_volatility'),
        pl.col('bb_position').std().alias('bollinger_deviation'),
       
        pl.len().alias('trading_days'),
        pl.col('sector').n_unique().alias('sectors_count'),
       
        (pl.col('price') > pl.col('sma_20')).mean().alias('above_sma_ratio'),
       
        ((pl.col('price').max() - pl.col('price').min()) / pl.col('price').min())
          .alias('price_range_pct')
    ])
   
    .with_columns([
        pl.col('total_dollar_volume').rank(method='ordinal', descending=True).alias('volume_rank'),
        pl.col('price_volatility').rank(method='ordinal', descending=True).alias('volatility_rank')
    ])
   
    .filter(pl.col('trading_days') >= 10)
    .sort(['ticker', 'year', 'quarter'])
)


df = result.collect()
print(f"\n Analysis Results: {df.height:,} aggregated records")
print("\nTop 10 High-Volume Quarters:")
print(df.sort('total_dollar_volume', descending=True).head(10).to_pandas())


print("\n \nAdvanced Analytics:")


pivot_analysis = (
    df.group_by('ticker')
    .agg([
        pl.col('avg_price').mean().alias('overall_avg_price'),
        pl.col('price_volatility').mean().alias('overall_volatility'),
        pl.col('total_dollar_volume').sum().alias('lifetime_volume'),
        pl.col('above_sma_ratio').mean().alias('momentum_score'),
        pl.col('price_range_pct').mean().alias('avg_range_pct')
    ])
    .with_columns([
        (pl.col('overall_avg_price') / pl.col('overall_volatility')).alias('risk_adj_score'),
       
        (pl.col('momentum_score') * 0.4 +
         pl.col('avg_range_pct') * 0.3 +
         (pl.col('lifetime_volume') / pl.col('lifetime_volume').max()) * 0.3)
         .alias('composite_score')
    ])
    .sort('composite_score', descending=True)
)


print("\n \nTicker Performance Ranking:")
print(pivot_analysis.to_pandas())

lf = pl.LazyFrame(data)


result = (
    lf
    .with_columns([
        pl.col('timestamp').dt.year().alias('year'),
        pl.col('timestamp').dt.month().alias('month'),
        pl.col('timestamp').dt.weekday().alias('weekday'),
        pl.col('timestamp').dt.quarter().alias('quarter')
    ])
   
    .with_columns([
        pl.col('price').rolling_mean(20).over('ticker').alias('sma_20'),
        pl.col('price').rolling_std(20).over('ticker').alias('volatility_20'),
       
        pl.col('price').ewm_mean(span=12).over('ticker').alias('ema_12'),
       
        pl.col('price').diff().alias('price_diff'),
       
        (pl.col('volume') * pl.col('price')).alias('dollar_volume')
    ])
   
    .with_columns([
        pl.col('price_diff').clip(0, None).rolling_mean(14).over('ticker').alias('rsi_up'),
        pl.col('price_diff').abs().rolling_mean(14).over('ticker').alias('rsi_down'),
       
        (pl.col('price') - pl.col('sma_20')).alias('bb_position')
    ])
   
    .with_columns([
        (100 - (100 / (1 + pl.col('rsi_up') / pl.col('rsi_down')))).alias('rsi')
    ])
   
    .filter(
        (pl.col('price') > 10) &
        (pl.col('volume') > 100000) &
        (pl.col('sma_20').is_not_null())
    )
   
    .group_by(['ticker', 'year', 'quarter'])
    .agg([
        pl.col('price').mean().alias('avg_price'),
        pl.col('price').std().alias('price_volatility'),
        pl.col('price').min().alias('min_price'),
        pl.col('price').max().alias('max_price'),
        pl.col('price').quantile(0.5).alias('median_price'),
       
        pl.col('volume').sum().alias('total_volume'),
        pl.col('dollar_volume').sum().alias('total_dollar_volume'),
       
        pl.col('rsi').filter(pl.col('rsi').is_not_null()).mean().alias('avg_rsi'),
        pl.col('volatility_20').mean().alias('avg_volatility'),
        pl.col('bb_position').std().alias('bollinger_deviation'),
       
        pl.len().alias('trading_days'),
        pl.col('sector').n_unique().alias('sectors_count'),
       
        (pl.col('price') > pl.col('sma_20')).mean().alias('above_sma_ratio'),
       
        ((pl.col('price').max() - pl.col('price').min()) / pl.col('price').min())
          .alias('price_range_pct')
    ])
   
    .with_columns([
        pl.col('total_dollar_volume').rank(method='ordinal', descending=True).alias('volume_rank'),
        pl.col('price_volatility').rank(method='ordinal', descending=True).alias('volatility_rank')
    ])
   
    .filter(pl.col('trading_days') >= 10)
    .sort(['ticker', 'year', 'quarter'])
)

df = result.collect()
print(f"\n Analysis Results: {df.height:,} aggregated records")
print("\nTop 10 High-Volume Quarters:")
print(df.sort('total_dollar_volume', descending=True).head(10).to_pandas())


print("\n Advanced Analytics:")


pivot_analysis = (
    df.group_by('ticker')
    .agg([
        pl.col('avg_price').mean().alias('overall_avg_price'),
        pl.col('price_volatility').mean().alias('overall_volatility'),
        pl.col('total_dollar_volume').sum().alias('lifetime_volume'),
        pl.col('above_sma_ratio').mean().alias('momentum_score'),
        pl.col('price_range_pct').mean().alias('avg_range_pct')
    ])
    .with_columns([
        (pl.col('overall_avg_price') / pl.col('overall_volatility')).alias('risk_adj_score'),
       
        (pl.col('momentum_score') * 0.4 +
         pl.col('avg_range_pct') * 0.3 +
         (pl.col('lifetime_volume') / pl.col('lifetime_volume').max()) * 0.3)
         .alias('composite_score')
    ])
    .sort('composite_score', descending=True)
)


print("\n Ticker Performance Ranking:")
print(pivot_analysis.to_pandas())

print("\n SQL Interface Demo:")
pl.Config.set_tbl_rows(5)


sql_result = pl.sql("""
    SELECT
        ticker,
        AVG(avg_price) as mean_price,
        STDDEV(price_volatility) as volatility_consistency,
        SUM(total_dollar_volume) as total_volume,
        COUNT(*) as quarters_tracked
    FROM df
    WHERE year >= 2021
    GROUP BY ticker
    ORDER BY total_volume DESC
""", eager=True)


print(sql_result)
print(f"\n Export Options:")
print("   • Parquet (high compression): df.write_parquet('data.parquet')")
print("   • Delta Lake: df.write_delta('delta_table')")
print("   • JSON streaming: df.write_ndjson('data.jsonl')")
print("   • Apache Arrow: df.to_arrow()")

