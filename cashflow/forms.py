from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('item',
            'person',
            'method',
            'amount',
            'comments',
            'paid_at',)
