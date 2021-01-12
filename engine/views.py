from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Stock
from .logic import parse_holdings, get_site_data, stringify, group_stocks
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

        # retrieve user's stocks from model
        stocks = list(Stock.objects.filter(owner=user).order_by('-date').values())

        # parse complete holdings from queryset
        stocks_list = parse_holdings(stocks)

        # get summary data (total gain, day's gain etc)
        context = get_site_data(stocks_list)

        # add 'stock_list' data to context as well
        context['stocks_list'] = stringify(stocks_list)
        context['grouped_list'] = group_stocks(stocks_list)

        # return json response
        return JsonResponse(context, status=200, safe=False)
