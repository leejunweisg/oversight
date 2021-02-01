from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from pandas.core import base
from .models import Stock
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .logic import parse_holdings, get_summary_data, stringify1, stringify2, get_currency
from datetime import datetime
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from .forms import StockModelForm
from django.urls import reverse_lazy


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
        base_currency = 'SGD'
        sort_holdings =  request.GET.get("sort_holdings")
        sort_lots = request.GET.get("sort_lots")

        # retrieve user's stocks from model
        stocks = list(Stock.objects.filter(owner=user).order_by('-date').values())

        # if no holdings, return empty=1
        if len(stocks) == 0:
            return JsonResponse({'empty': 1}, status=200, safe=False)

        # parse complete holdings from queryset
        holdings_table, grouped_table = parse_holdings(stocks, sort_holdings, sort_lots)

        # get summary data (total gain, day's gain etc)
        context = get_summary_data(holdings_table, base_currency)

        # add 'stock_list' data to context as well
        context['stocks_list'] = stringify1(holdings_table)
        context['grouped_list'] = stringify2(grouped_table)

        # return json response
        return JsonResponse(context, status=200, safe=False)

class StockCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'engine/create_stock.html'
    form_class = StockModelForm
    success_message = 'Success! The new holding has been added to your portfolio!'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # set the owner to the current logged in user
        form.instance.owner = self.request.user
        form.instance.currency = get_currency(form.instance.symbol)
        return super().form_valid(form)


class StockDeleteView(LoginRequiredMixin, UserPassesTestMixin, BSModalDeleteView):
    model = Stock
    template_name = 'engine/delete_stock.html'
    success_message = 'Success: The lot has been deleted!'
    success_url = reverse_lazy('dashboard')

    # ensure only author can delete his post
    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.owner:
            return True
        else:
            return False

class StockUpdateView(LoginRequiredMixin, UserPassesTestMixin, BSModalUpdateView):
    model = Stock
    template_name = 'engine/update_stock.html'
    form_class = StockModelForm
    success_message = 'Success: Your holdings has been updated!'
    success_url = reverse_lazy('dashboard')

    # ensure only author can update his post
    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.owner:
            return True
        else:
            return False