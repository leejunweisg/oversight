from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Stock
from .logic import parse_holdings, get_site_data

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
        print(f"User: {request.user.username}")

        # get user
        user = request.user

        # retrieve user's stocks from model
        stocks = Stock.objects.filter(owner=user).order_by('-date').values()

        # parse complete holdings from queryset
        holdings = parse_holdings(stocks)

        # get calculated data (total gain, day's gain etc)
        context = get_site_data(holdings)

        # data to pass into template
        context['stocks_list'] = holdings


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


def dashboard_refresh(request):
    pass