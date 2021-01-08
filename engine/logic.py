from yahoo_fin import stock_info

# stock_info.get_live_price('qqq')

def total_portfolio_value(portfolio):
    total_value = 0

    for stock in portfolio:
        symbol = stock['symbol']
        shares = stock['shares']
        price = stock_info.get_live_price(symbol)
        total = price * shares
        print(f"Total for {shares} shares of {symbol.upper()}: ${total:.2f}")
        total_value += total

    return total_value

p = [
    {'symbol': 'qqq', 'shares': 10},
    {'symbol': 'amd', 'shares': 10},
]

print(total_portfolio_value(p))