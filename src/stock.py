import json
from datetime import datetime

import yfinance as yf
import pandas as pd
import pandas_ta as ta

def _calculate_stochastic(df: pd.DataFrame) -> dict:
    try:
        result = df.ta.stoch()
        return {
            "stochastic_k": round(result['STOCHk_14_3_3'].iloc[-1], 2),
            "stochastic_d": round(result['STOCHd_14_3_3'].iloc[-1], 2)
            }
    except Exception as e:
        return {}

def _calculate_macd(df: pd.DataFrame) -> dict:
    try:
        result = df.ta.macd()
        return {
            "macd": round(result['MACD_12_26_9'].iloc[-1], 4),
            "signal_line": round(result['MACDs_12_26_9'].iloc[-1], 4),
            "histogram": round(result['MACDh_12_26_9'].iloc[-1], 4)
        }
    except Exception as e:
        return {}

def _calculate_adx(df: pd.DataFrame) -> dict:
    try:
        result = df.ta.adx()
        return {
            "adx": round(result['ADX_14'].iloc[-1], 2),
            "di_plus": round(result['DMP_14'].iloc[-1], 2),
            "di_minus": round(result['DMN_14'].iloc[-1], 2)
        }
    except Exception as e:
        return {}

def _calculate_supertrend(df: pd.DataFrame) -> dict:
    try:
        result = df.ta.supertrend(length=10)
        return {
            "supertrend": round(result['SUPERT_10_3.0'].iloc[-1], 2),
            "direction": "UP" if result['SUPERTd_10_3.0'].iloc[-1] == 1 else "DOWN"
        }
    except Exception as e:
        return {
            "supertrend": None,
            "direction": None
        }

def _calculate_ichimoku(df: pd.DataFrame) -> dict:
    try:
        result = df.ta.ichimoku()
        historical_df = result[0]

        # senkou_span_b：(過去52日の高値 + 過去52日の安値) / 2 を26日先にシフト
        high_52 = df['High'].rolling(window=52).max()
        low_52 = df['Low'].rolling(window=52).min()
        senkou_b_value = (high_52 + low_52) / 2
        senkou_b_shifted = senkou_b_value.shift(26)
        senkou_b = senkou_b_shifted.iloc[-1]

        return {
            "tenkan_sen": round(historical_df['ISA_9'].iloc[-1], 2),
            "kijun_sen": round(historical_df['ISB_26'].iloc[-1], 2),
            "chikou_span": round(historical_df['ITS_9'].iloc[-1], 2),
            "cloud": {
                "senkou_span_a": round(historical_df['IKS_26'].iloc[-1], 2),
                "senkou_span_b": round(senkou_b, 2)
            }
        }
    except Exception as e:
        return {}

def _get_valuation_data(stock) -> dict:
    try:
        return {
            "per": round(stock.info.get('trailingPE'), 2),
            "pbr": round(stock.info.get('priceToBook'), 2)
        }
    except Exception as e:
        return {}

def _get_financial_data(stock) -> dict:
    quarterly_financials = stock.quarterly_financials
    try:
        if quarterly_financials.empty or 'Total Revenue' not in quarterly_financials.index:
            return {}

        latest = quarterly_financials.columns[0]
        return {
            "revenue_billion_yen": round(quarterly_financials.loc['Total Revenue', latest] / 1e9, 1),
            "operating_income_billion_yen": round(quarterly_financials.loc['Operating Income', latest] / 1e9, 1)
        }
    except Exception as e:
        return {}

def _get_risk_metrics(stock) -> dict:
    try:
        earnings_date = None
        calendar = stock.calendar
        if calendar is not None and 'Earnings Date' in calendar:
            earnings_date_value = calendar['Earnings Date']
            if isinstance(earnings_date_value, list) and len(earnings_date_value) > 0:
                earnings_date = str(earnings_date_value[0])
            else:
                earnings_date = str(earnings_date_value)

        return {
            "beta": round(stock.info.get('beta'), 2),
                "average_volume": int(stock.info.get('averageVolume')),
                "earnings_date": earnings_date
            }
    except Exception as e:
        return {}

def _get_current_price_info(hist: pd.DataFrame) -> dict:
    try:
        latest = hist.iloc[-1]
        latest_date = hist.index[-1].strftime('%Y-%m-%d')
        current_close = round(latest['Close'], 2)

        prev_close = None
        change_percent = None
        if len(hist) >= 2:
            prev_close = round(hist.iloc[-2]['Close'], 2)
            if prev_close:
                change_percent = round(((current_close - prev_close) / prev_close * 100), 2)

        return {
            "date": latest_date,
            "open": round(latest['Open'], 2),
            "high": round(latest['High'], 2),
            "low": round(latest['Low'], 2),
            "close": current_close,
            "prev_close": prev_close,
            "change_percent": change_percent,
            "volume": int(latest['Volume'])
        }
    except Exception as e:
        return {}

def _get_52_week_info(stock, hist: pd.DataFrame) -> dict:
    try:
        latest = hist.iloc[-1]
        current_close = round(latest['Close'], 2)

        change_from_high_percent = round(((current_close - stock.info.get('fiftyTwoWeekHigh')) / stock.info.get('fiftyTwoWeekLow') * 100), 2)

        return {
            "high": round(stock.info.get('fiftyTwoWeekHigh'), 2),
            "low": round(stock.info.get('fiftyTwoWeekLow'), 2),
            "change_from_high_percent": change_from_high_percent
        }
    except Exception as e:
        return {}

def _get_news(stock, limit: int = 5) -> list:
    try:
        news_list = []

        for i in range(min(limit, len(stock.news))):
            article = stock.news[i]
            content = article.get('content', {})

            provider = content.get('provider', {})
            publisher = provider.get('displayName')

            click_url = content.get('clickThroughUrl') or {}
            link = click_url.get('url', '')

            news_item = {
                "title": content.get('title'),
                "publisher": publisher,
                "link": link,
                "providerPublishTime": content.get('pubDate')
            }
            news_list.append(news_item)

        return news_list
    except Exception as e:
        return []

def get_market_conditions() -> dict:
    try:
        market_data = {}
        indicators = {
            "nikkei225": "^N225",
            "sp500": "^GSPC",
            "nasdaq": "^IXIC",
            "vix": "^VIX",
            "usdjpy": "USDJPY=X"
        }

        for name, ticker in indicators.items():
            data = yf.Ticker(ticker).history(period="5d")

            prev_close = data['Close'].iloc[-2]
            latest_close = data['Close'].iloc[-1]
            change_rate = round(((latest_close - prev_close) / prev_close * 100), 2)

            market_data[name] = {
                "prev_close": round(prev_close, 2),
                "latest_close": round(latest_close, 2),
                "change_percent": change_rate
            }

        return market_data
    except Exception as e:
        return {}

def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")

    data = {
        "timestamp": datetime.now().isoformat(),
        "ticker": ticker,
        "company_name": stock.info.get('longName'),
        "sector": stock.info.get('sector'),
        "industry": stock.info.get('industry'),
        "dividend_yield": round(stock.info.get('dividendYield'), 2),
        "market_cap_billion_yen": round(stock.info.get('marketCap') / 1e9, 1),
        "valuation": _get_valuation_data(stock),
        "financial": _get_financial_data(stock),
        "risk_metrics": _get_risk_metrics(stock),
        "current_price": _get_current_price_info(df),
        "52_week": _get_52_week_info(stock, df),
        "technical_indicators": {
            "stochastic_rsi": _calculate_stochastic(df),
            "macd": _calculate_macd(df),
            "adx": _calculate_adx(df),
            "supertrend": _calculate_supertrend(df),
            "ichimoku": _calculate_ichimoku(df)
        },
        "news": _get_news(stock)
    }

    return data

if __name__ == "__main__":
    print(json.dumps(get_market_conditions(), indent=4, ensure_ascii=False))
    print(json.dumps(get_stock_info("2914.T"), indent=4, ensure_ascii=False))