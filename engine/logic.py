from yahoo_fin import stock_info
import yfinance as yf
from forex_python.converter import CurrencyRates


# parse query set into a list of dictionaries with additional columns
# (avg price per share, market value, dailygain, totalgain)
def parse_holdings(portfolio):
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
        stock['yestvalue'] = stock.get('shares') * yestprice
        stock['dailygain'] = (currentprice - yestprice) * stock.get('shares')
        stock['daily_p'] = (currentprice - yestprice)/yestprice * 100
        stock['totalgain'] = (currentprice - executedprice) * stock.get('shares') - stock.get('fees')
        stock['total_p'] = (currentprice - executedprice)/executedprice * 100

    # return complete holdings
    print("Completed parsing.")
    return holdings # type: list of dictionaries


# returns the current portfolio market value (adds up market value column)
# does conversion of currency to a defined base currency as well
def get_current_value(holdings, base_currency="USD"):
    c = CurrencyRates()

    total = 0
    for x in holdings:
        if base_currency != x['currency']:
            converted = c.convert(x['currency'], base_currency, x['marketvalue'])
            total += converted
        else:
            total += x['marketvalue']

    return total


def get_yest_value(holdings, base_currency="USD"):
    c = CurrencyRates()

    total = 0
    for x in holdings:
        if base_currency != x['currency']:
            converted = c.convert(x['currency'], base_currency, x['yestvalue'])
            total += converted
        else:
            total += x['yestvalue']

    return total

# returns the original value of the portfolio (price executed x # of shares)
# market value only, does not include fees
def get_original_value(holdings, base_currency="USD"):
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


# returns the total fees paid in all trades
# does conversion of currency to a defined base currency as well
def get_total_fees(holdings, base_currency="USD"):
    c = CurrencyRates()

    total = 0
    for x in holdings:
        if base_currency != x['currency']:
            converted = c.convert(x['currency'], base_currency, x['fees'])
            total += converted
        else:
            total += x['fees']

    return total


def get_site_data(holdings, base_currency="USD"):
    # calculate portfolio values
    current_portfolio_value = get_current_value(holdings, base_currency)
    original_portfolio_value = get_original_value(holdings, base_currency)
    yest_portfolio_value = get_yest_value(holdings, base_currency)
    total_fees = get_total_fees(holdings, base_currency)

    # total change (including fees)
    total_change = current_portfolio_value-original_portfolio_value-total_fees
    total_change_p = (total_change/original_portfolio_value) * 100

    # day change (no fees)
    day_change = current_portfolio_value - yest_portfolio_value
    day_change_p = (day_change/yest_portfolio_value) * 100

    data = {
        'portfolio_value': current_portfolio_value,
        'total_change': total_change,
        'total_change_p': total_change_p,
        'day_change': day_change,
        'day_change_p': day_change_p
    }    

    return data