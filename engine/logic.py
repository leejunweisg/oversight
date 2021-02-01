from forex_python.converter import CurrencyCodes
import requests
import pandas as pd
import yfinance as yf

DEBUG = True
def log(msg):
    if DEBUG:
        print(msg)

# this function retrieves price data from yahoo finance
# retrieves current close, and previous close
def get_prices(symbols):
    # retrieve data from yahoo finance
    url = "https://query1.finance.yahoo.com/v8/finance/spark?symbols={}".format(','.join(symbols))
    params={}
    params['range']='1d'
    params['interval']='1d'
    params['indicators']='close'
    params['includePrePost']='true'
    params['corsDomain']='finance.yahoo.com'
    data = requests.get(url=url, params=params)

    # clean data and construct dataframe
    cleaned_data = []
    for k, v in data.json().items():
        temp={}
        temp['symbol'] = k
        temp['close'] = v['close'][-1]
        temp['prevclose'] = v['chartPreviousClose']
        cleaned_data.append(temp)
    df = pd.DataFrame(cleaned_data)

    # return
    return df

# this function retrieves currency rates data
# gets quotes against a base currency
def get_rates(base):
    url = "https://api.exchangerate.host/latest?base={}".format(base)
    data = requests.get(url=url)
    return data.json()['rates']


# parse query set into a list of dictionaries with additional columns
# (avg price per share, market value, dailygain, totalgain)
def parse_holdings(portfolio, sort_holdings, sort_lots):
    # get all unique tickers in portfolio
    symbols = set([x['symbol'] for x in portfolio])
    log(f"Symbols retrieved: {', '.join(symbols)}")

    # get price of all tickers
    price_df = get_prices(symbols)
    log("Prices downloaded!")

    # construct holdings dataframe
    holdings_df = pd.DataFrame(portfolio)

    # check for non-existent symbols, and remove
    invalid = set()
    for sym in symbols:
        if sym not in price_df['symbol'].values:
            print("Symbol(s) not found and ignored:", sym)
            invalid.add(sym)
    symbols = symbols.difference(invalid)

    # merge downloaded prices into holdings_df
    holdings_df = pd.merge(holdings_df, price_df, on='symbol')
    holdings_df['avg'] = (holdings_df['shares']*holdings_df['price']+holdings_df['fees'])/holdings_df['shares']
    holdings_df['marketvalue'] = holdings_df['shares'] * holdings_df['close']
    holdings_df['yestvalue'] = holdings_df['shares'] * holdings_df['prevclose']
    holdings_df['dailygain'] = (holdings_df['close'] - holdings_df['prevclose']) * holdings_df['shares']
    holdings_df['daily_p'] = ((holdings_df['close'] - holdings_df['prevclose'])/holdings_df['prevclose']) * 100
    holdings_df['totalgain'] = ((holdings_df['close'] - holdings_df['price']) * holdings_df['shares']) - holdings_df['fees']
    holdings_df['total_p'] = ((holdings_df['close'] - holdings_df['price'])/holdings_df['price']) *100

    # created grouped_df for grouped table
    grouped_df = pd.DataFrame(columns=['symbol', 'shares', 'avgprice', 'avgcost', 'marketvalue', 'dailygain', 'daily_p','totalgain', 'total_p'])
    for sym in symbols:
        filtered = holdings_df[holdings_df['symbol']==sym]
        row = {}
        row['symbol'] = sym
        row['change'] = filtered['close'].iloc[0] - filtered['prevclose'].iloc[0]
        row['change_p'] = ((filtered['close'].iloc[0] - filtered['prevclose'].iloc[0])/filtered['prevclose'].iloc[0])*100
        row['shares'] = filtered['shares'].sum()
        row['avgprice'] = (filtered['shares'] * filtered['price']).sum() / filtered['shares'].sum()
        row['avgcost'] = (filtered['shares'] * filtered['price'] + filtered['fees']).sum() / filtered['shares'].sum()
        row['marketvalue'] = filtered['shares'].sum() * filtered['close'].sum()
        row['dailygain'] = ((filtered['close'] - filtered['prevclose']) * filtered['shares']).sum()
        row['daily_p'] = (((filtered['close']*filtered['shares']).sum() - (filtered['prevclose']*filtered['shares']).sum())/(filtered['prevclose']*filtered['shares']).sum()) * 100
        row['totalgain'] = ((filtered['close'] - filtered['price']) * filtered['shares']).sum() - filtered['fees'].sum()
        row['total_p'] = (row['totalgain']/(filtered['price'] * filtered['shares']).sum()) *100
        grouped_df = grouped_df.append(row, ignore_index=True)
    
    # sort holdings
    if sort_holdings == "2":
        grouped_df.sort_values("avgprice", inplace=True, ascending=False)
    elif sort_holdings == "3":
        grouped_df.sort_values("avgcost", inplace=True, ascending=False)
    elif sort_holdings == "4":
        grouped_df.sort_values("marketvalue", inplace=True, ascending=False)
    elif sort_holdings == "5":
        grouped_df.sort_values("dailygain", ascending=False, inplace=True)
    elif sort_holdings == "6":
        grouped_df.sort_values("totalgain", ascending=False, inplace=True)
    else:
         grouped_df.sort_values("symbol", inplace=True)

    # sort lots
    if sort_lots == "2":
        holdings_df.sort_values("symbol", inplace=True)
    elif sort_lots == "3":
        holdings_df.sort_values("marketvalue", ascending=False, inplace=True)
    elif sort_lots == "4":
        holdings_df.sort_values("dailygain", ascending=False, inplace=True)
    elif sort_lots == "5":
        holdings_df.sort_values("totalgain", ascending=False, inplace=True)

    # return complete holdings
    log("Completed parsing.")
    return holdings_df.to_dict('records'), grouped_df.to_dict('records') # type: list of dictionaries


# returns the current portfolio market value (adds up market value column)
# does conversion of currency to a defined base currency as well
def get_current_value(stocks_list, base_currency, currency_rates):
    total = 0
    for x in stocks_list:
        if base_currency != x['currency']:
            converted = x['marketvalue'] / currency_rates[x['currency']]
            total += converted
        else:
            total += x['marketvalue']
    return total

# returns yesterday's portfolio market value (adds up yestvalue column)
# does conversion of currency to a defined base currency as well
def get_yest_value(stocks_list, base_currency, currency_rates):
    total = 0
    for x in stocks_list:
        if base_currency != x['currency']:
            converted = x['yestvalue'] / currency_rates[x['currency']]
            total += converted
        else:
            total += x['yestvalue']
    return total


# returns the original value of the portfolio (price executed x # of shares)
# market value only, does not include fees
def get_original_value(stocks_list, base_currency, currency_rates):
    total = 0
    for x in stocks_list:
        value = x['price'] * x['shares']
        if base_currency != x['currency']:
            converted = value / currency_rates[x['currency']]
            total += converted
        else:
            total += value
    return total


# returns the total fees paid in all trades
# does conversion of currency to a defined base currency as well
def get_total_fees(stocks_list, base_currency, currency_rates):
    total = 0
    for x in stocks_list:
        if base_currency != x['currency']:
            converted = x['fees'] / currency_rates[x['currency']]
            total += converted
        else:
            total += x['fees']
    return total


def get_summary_data(stocks_list, base_currency="USD"):
    # get currency rates
    currency_rates = get_rates(base_currency)

    # get currency symbol
    c = CurrencyCodes()
    currency_sym = c.get_symbol(base_currency)

    # calculate portfolio values
    current_portfolio_value = get_current_value(stocks_list, base_currency, currency_rates)
    original_portfolio_value = get_original_value(stocks_list, base_currency, currency_rates)
    yest_portfolio_value = get_yest_value(stocks_list, base_currency, currency_rates)
    total_fees = get_total_fees(stocks_list, base_currency, currency_rates)

    # total change (including fees)
    total_change = current_portfolio_value-original_portfolio_value-total_fees
    total_change_p = (total_change/original_portfolio_value) * 100

    # day change (no fees)
    day_change = current_portfolio_value - yest_portfolio_value
    day_change_p = (day_change/yest_portfolio_value) * 100

    # data for summary section of dashboard
    data = {
        'portfolio_value': f"{currency_sym} {current_portfolio_value:,.2f}",
        'total_change': f"{currency_sym} {total_change:,.2f}",
        'total_change_p': f"{total_change_p:+.2f}",
        'day_change': f"{currency_sym} {day_change:,.2f}",
        'day_change_p': f"{day_change_p:+.2f}"
    }

    return data

def stringify1(holdings_table):
    for stock in holdings_table:
        stock['avg'] = f"{stock['avg']:,.02f}"
        stock['marketvalue'] = f"{stock['marketvalue']:,.02f}"
        stock['yestvalue'] = f"{stock['yestvalue']:,.02f}"
        stock['dailygain'] = f"{stock['dailygain']:+,.02f}"
        stock['daily_p'] = f"{stock['daily_p']:+,.02f}"
        stock['totalgain'] = f"{stock['totalgain']:+,.02f}"
        stock['total_p'] = f"{stock['total_p']:+,.02f}"
    return holdings_table

def stringify2(grouped_table):
    for stock in grouped_table:
        stock['change']=f"{stock['change']:+,.02f}"
        stock['change_p'] = f"{stock['change_p']:+,.02f}"
        stock['avgprice'] = f"{stock['avgprice']:,.02f}"
        stock['avgcost'] = f"{stock['avgcost']:,.02f}"
        stock['marketvalue'] = f"{stock['marketvalue']:,.02f}"
        stock['dailygain'] = f"{stock['dailygain']:+,.02f}"
        stock['daily_p'] = f"{stock['daily_p']:+,.02f}"
        stock['totalgain'] = f"{stock['totalgain']:+,.02f}"
        stock['total_p'] = f"{stock['total_p']:+,.02f}"
    return grouped_table

def get_currency(ticker):
    stock = yf.Ticker(ticker)
    return stock.info['currency']