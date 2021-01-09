from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Stock
from .logic import portfolio_value, original_portfolio_value, get_complete_holdings

DEBUG = True
def log(msg):
    if DEBUG:
        print(msg)


# Create your views here.
@login_required
def dashboard(request):
    log("--- Dashboard ---")

    # if user is authenticated
    if request.user.is_authenticated:
        print(f"--- User: {request.user.username} ---")

        # get user
        user = request.user
        stocks = Stock.objects.filter(owner=user).order_by('-date').values()

        # get complete holdings
        holdings = get_complete_holdings(stocks)

        # calculate portfolio values
        portfolio_val = portfolio_value(holdings)
        original_portfolio_val = original_portfolio_value(holdings)
        percentage_chng = ((portfolio_val-original_portfolio_val)/original_portfolio_val) * 100
        
        # pie chart data
        pie={}
        test = []
        test = [x['symbol'] for x in stocks if x['symbol']]
        pie['labels'] = test
        pie['data'] = [1,2,3]

        # data to pass into template
        context = {
            'portfolio_value': portfolio_val,
            'original_portfolio_value': original_portfolio_val,
            'percentage_change': percentage_chng,
            'stocks_list': holdings,
            'chart': pie
        }

    else:
        # empty data to pass into template
        context = {
            'portfolio_value': 0,
            'original_portfolio_value': 0,
            'percentage_change': 0
        }



    # render template
    print("----------------")
    return render(request, 'engine/dashboard.html', context)
