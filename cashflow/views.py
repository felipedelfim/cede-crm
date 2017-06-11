from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.db.models import Sum
from django.utils import timezone
import datetime

from .models import Transaction, Item, Person, Group, Category, Method, CostCenter
from .forms import TransactionForm, PersonForm, PersonImportForm, ItemImportForm, TransactionReportFilterForm

class IndexView(generic.ListView):
    model = Transaction
    template_name = 'cadhflow/transaction_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'transactions'  # Default: object_list
    paginate_by = 25

def transaction_new(request):
	if request.method == 'POST':
		form = TransactionForm(request.POST)
		if form.is_valid():
			transaction = form.save()
			return redirect('cashflow:index')
	else:
		form = TransactionForm()
	return render(request, 'cashflow/transaction_edit.html', {'form': form})

def transaction_edit(request, pk):
	transaction = get_object_or_404(Transaction, pk=pk)
	if request.method == 'POST':
		form = TransactionForm(request.POST, instance=transaction)
		if form.is_valid():
			transaction = form.save()
			return redirect('cashflow:index')
	else:
		form = TransactionForm(instance=transaction)
	return render(request, 'cashflow/transaction_edit.html', {'form': form})

def transaction_pay(request, pk):
	transaction = get_object_or_404(Transaction, pk=pk)
	transaction.pay()
	transaction.save()
	return redirect('cashflow:index')

def transaction_remove(request, pk):
	transaction = get_object_or_404(Transaction, pk=pk)
	transaction.delete()
	return redirect('cashflow:index')

def transaction_report(request):
    if request.method == 'POST':
        form = TransactionReportFilterForm(request.POST)
        if form.is_valid():
            date_range = form.cleaned_data['date_range']
            start_at = datetime.datetime.strptime(date_range.split(' - ')[0], "%d/%m/%Y").date()
            end_at = datetime.datetime.strptime(date_range.split(' - ')[1], "%d/%m/%Y").date()
    else:
        form = TransactionReportFilterForm()
        start_at = datetime.date.today()
        end_at = datetime.date.today()

    report_by_paid_at = Transaction.objects.values('paid_at').filter(paid_at__gte=start_at, paid_at__lte=end_at).annotate(total=Sum('total')).order_by('-paid_at')
    report_by_category = Category.objects.order_by('name').filter(transaction__paid_at__gte=start_at, transaction__paid_at__lte=end_at).annotate(total=Sum('transaction__total')).order_by('-total')
    report_by_method = Method.objects.order_by('name').filter(transaction__paid_at__gte=start_at, transaction__paid_at__lte=end_at).annotate(total=Sum('transaction__total')).order_by('-total')
    report_by_cost_center = CostCenter.objects.order_by('name').filter(item__transaction__paid_at__gte=start_at, item__transaction__paid_at__lte=end_at).annotate(total=Sum('item__transaction__total')).order_by('-total')
    return render(request, 'cashflow/transaction_report.html',
    {'form': form,
    'report_by_paid_at': report_by_paid_at,
    'report_by_category': report_by_category,
    'report_by_method': report_by_method,
    'report_by_cost_center': report_by_cost_center})

class PersonListView(generic.ListView):
    model = Person
    template_name = 'cadhflow/person_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'persons'  # Default: object_list
    paginate_by = 25

def person_new(request):
	if request.method == 'POST':
		form = PersonForm(request.POST)
		if form.is_valid():
			person = form.save()
			return redirect('cashflow:person_list')
	else:
		form = PersonForm()
	return render(request, 'cashflow/person_edit.html', {'form': form})

def person_edit(request, pk):
	person = get_object_or_404(Person, pk=pk)
	if request.method == 'POST':
		form = PersonForm(request.POST, instance=person)
		if form.is_valid():
			person = form.save()
			return redirect('cashflow:person_list')
	else:
		form = PersonForm(instance=person)
	return render(request, 'cashflow/person_edit.html', {'form': form})

def person_import(request):
    if request.method == 'POST':
        form = PersonImportForm(request.POST)
        if form.is_valid():
            for name in form.cleaned_data['person_list'].splitlines():
                person = Person(group=form.cleaned_data['group'], name=name)
                person.save()
            return redirect('cashflow:person_list')
    else:
        form = PersonImportForm()

    return render(request, 'cashflow/person_import.html', {'form': form})

class ItemListView(generic.ListView):
    model = Item
    template_name = 'cadhflow/item_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'items'  # Default: object_list
    paginate_by = 25

def item_get_value(request, pk):
	item = get_object_or_404(Item, pk=pk)
	data = {
		'value': item.value
	}
	return JsonResponse(data)

def item_import(request):
    if request.method == 'POST':
        form = ItemImportForm(request.POST)
        if form.is_valid():
            for name in form.cleaned_data['item_list'].splitlines():
                item = Item(category=form.cleaned_data['category'], cost_center=form.cleaned_data['cost_center'], value=form.cleaned_data['value'], name=name)
                item.save()
            return redirect('cashflow:item_list')
    else:
        form = ItemImportForm()

    return render(request, 'cashflow/item_import.html', {'form': form})

def category_items(request, pk):
    items = get_list_or_404(Item, category_id=pk)
    data = []
    for item in items:
        data.append({
        'id': item.id,
        'name': item.name
        })
    #return HttpJsonResponse(data, is_ajax=request.is_ajax())
    return JsonResponse({'items':data})
