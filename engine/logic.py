from yahoo_fin import stock_info
import yfinance as yf
from forex_python.converter import CurrencyRates


def get_complete_holdings(portfolio):

    holdings = []

    # get all unique tickers in portfolio
    tickers = []
    for stock in portfolio:
        symbol = stock.get('symbol')
        if symbol not in tickers:
            tickers.append(symbol)

    print("Tickers found.")

    # get price of all tickers
    data = yf.download(' '.join(tickers), period='1d', progress=False)

    print("Prices downloaded.")

    # construct holdings dataframe
    for stock in portfolio:
        holdings.append(stock)

        symbol = stock.get('symbol').upper()
        executedprice = stock.get('price')
        currentprice = data['Close'][symbol].values[1]
        yestprice = data['Close'][symbol].values[0]

        stock['avg'] = (executedprice * stock.get('shares') + stock.get('fees')) / stock.get('shares')
        stock['marketvalue'] = stock.get('shares') * currentprice
        stock['dailygain'] = (currentprice - yestprice) * stock.get('shares')
        stock['daily_p'] = (currentprice - yestprice)/yestprice * 100
        stock['totalgain'] = (currentprice - executedprice) * stock.get('shares') - stock.get('fees')
        stock['total_p'] = (currentprice - executedprice)/executedprice * 100

    print("Completed parsing.")
    # return complete holdings
    return holdings # type: list of dictionaries

def portfolio_value(holdings, base_currency="USD"):
    c = CurrencyRates()

    total = 0
    for x in holdings:
        if base_currency != x['currency']:
            converted = c.convert(x['currency'], base_currency, x['marketvalue'])
            total += converted
        else:
            total += x['marketvalue']

    return total

def original_portfolio_value(holdings, base_currency="USD"):
    # market value only, does not include fees

    c = CurrencyRates()

    total = 0
    for x in holdings:
        value = x['price'] * x['shares']
        if base_currency != x['currency']:
            converted = c.convert(x['currency'], base_currency, value)
            total += converted
        else:
            total += value

    return total