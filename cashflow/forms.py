from django import forms
from .models import Transaction, Person
from django.utils.translation import ugettext_lazy as _

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ['created_at', 'updated_at']
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

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ['created_at', 'updated_at']
        labels = {
            'name': _('Nome'),
            'group': _('Grupo'),
            'phone_number': _('Telefone'),
        }
