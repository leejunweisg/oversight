from .models import Stock
from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ValidationError
from .logic import exist_ticker
from django import forms

class StockModelForm(BSModalModelForm):

    class Meta:
        model = Stock
        fields = ['date', 'symbol', 'shares', 'price', 'fees']
        
    def clean_symbol(self):

        # uppercase
        symbol = self.cleaned_data['symbol'].upper()

        # raise exception if symbol doesn't exist
        if not exist_ticker(symbol):
            raise ValidationError("That symbol does not exist!")

        return symbol
