from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Stock
from .logic import parse_holdings, get_site_data, stringify
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
        stocks = Stock.objects.filter(owner=user).order_by('-date').values()

        # parse complete holdings from queryset
        holdings = parse_holdings(stocks)

        # get calculated data (total gain, day's gain etc)
        context = get_site_data(holdings)

        # data to pass into template
        context['stocks_list'] = stringify(holdings)

        # return json response
        return JsonResponse(context, status=200, safe=False)
