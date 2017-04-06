from django import forms
from .models import Transaction
from django.utils.translation import ugettext_lazy as _

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ['created_at', 'updated_at']
        #localized_fields = ['__all__']
        labels = {
            'item': _('Item'),
            'person': _('Frequentador'),
            'method': _('Forma de Pagamento'),
            'item_value': _('Valor Unitário'),
            'amount': _('Quantidade'),
            'total': _('Total'),
            'comments': _('Comentários'),
            'paid_at': _('Pago em'),
        }
        widgets = {
            'paid_at': forms.DateInput(attrs={'class':'datepicker'}),
        }
