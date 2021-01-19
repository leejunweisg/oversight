from .models import Stock
from bootstrap_modal_forms.forms import BSModalModelForm

class StockModelForm(BSModalModelForm):
    class Meta:
        model = Stock
        fields = ['date', 'symbol', 'shares', 'price', 'fees', 'currency']
        