from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pandas.core import base
from .models import Stock
from .logic import parse_holdings, get_summary_data, stringify1, stringify2
from datetime import datetime

DEBUG = True
def log(msg):
    if DEBUG:
        print(msg)

# Create your views here.
@login_required
def dashboard(request): 
    context={}
    return render(request, 'engine/dashboard.html', context)

def dashboard_refresh(request):
    if request.is_ajax():
        # get user
        user = request.user
        base_currency = 'USD'
        
        # retrieve user's stocks from model
        stocks = list(Stock.objects.filter(owner=user).order_by('-date').values())

        # if no holdings, return empty=1
        if len(stocks) == 0:
            return JsonResponse({'empty': 1}, status=200, safe=False)

        # parse complete holdings from queryset
        holdings_table, grouped_table = parse_holdings(stocks)

        # get summary data (total gain, day's gain etc)
        context = get_summary_data(holdings_table, base_currency)

        # add 'stock_list' data to context as well
        context['stocks_list'] = stringify1(holdings_table)
        context['grouped_list'] = stringify2(grouped_table)

        # return json response
        return JsonResponse(context, status=200, safe=False)
