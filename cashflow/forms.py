from django import forms
from .models import Transaction, Person, Group, Category, CostCenter, Item
from django.utils.translation import ugettext_lazy as _

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ['created_at', 'updated_at']
        labels = {
            'category': _('Categoria'),
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
            'paid_at': forms.DateInput(format='%d/%m/%Y', attrs={'class':'date'}),
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
        widgets = {
            'phone_number': forms.TextInput(attrs={'class':'phone'}),
        }

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ['created_at', 'updated_at']
        labels = {
            'name': _('Nome'),
            'category': _('Categoria'),
            'cost_center': _('Centro de Custo'),
            'value': _('Valor'),
            'inventory': _('Estoque'),
        }

class PersonImportForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.order_by('name'), empty_label="---------", label='Grupo')
    person_list = forms.CharField(label='Frequentadores', widget=forms.Textarea, help_text='1 nome por linha')

class ItemImportForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.order_by('name'), empty_label="---------", label='Categoria')
    cost_center = forms.ModelChoiceField(queryset=CostCenter.objects.order_by('name'), empty_label="---------", label='Centro de Custo')
    item_list = forms.CharField(label='Itens', widget=forms.Textarea, help_text='1 nome por linha')

class TransactionReportFilterForm(forms.Form):
    date_range = forms.CharField(label='Data')

class TransactionListFilterForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.order_by('name'), empty_label="Todos", label='Frequentador', required=False)
    item = forms.ModelChoiceField(queryset=Item.objects.order_by('name'), empty_label="Todos", label='Item', required=False)
    status = forms.ChoiceField(choices=(('all', 'Todos'),('paid','Pago'),('unpaid','Não Pago')))

class ItemListFilterForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.order_by('name'), empty_label="Todos", label='Item', required=False)
    cost_center = forms.ModelChoiceField(queryset=CostCenter.objects.order_by('name'), empty_label="Todos", label='Centro de Custo', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.order_by('name'), empty_label="Todas", label='Categoria', required=False)

class PersonListFilterForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.order_by('name'), empty_label="Todos", label='Frequentador', required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.order_by('name'), empty_label="Todos", label='Grupo', required=False)
