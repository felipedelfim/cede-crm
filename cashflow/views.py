from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.db.models import Sum


from .models import Transaction, Item, Person, Group
from .forms import TransactionForm, PersonForm, PersonImportForm

class IndexView(generic.ListView):
    model = Transaction
    template_name = 'cadhflow/transaction_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'transactions'  # Default: object_list
    paginate_by = 25
    queryset = Transaction.objects.order_by('-updated_at')

def transaction_new(request):
	if request.method == "POST":
		form = TransactionForm(request.POST)
		if form.is_valid():
			transaction = form.save()
			return redirect('cashflow:index')
	else:
		form = TransactionForm()
	return render(request, 'cashflow/transaction_edit.html', {'form': form})

def transaction_edit(request, pk):
	transaction = get_object_or_404(Transaction, pk=pk)
	if request.method == "POST":
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
	report = Transaction.objects.values('paid_at').annotate(total=Sum("total")).order_by()
	return render(request, 'cashflow/transaction_report.html', {'report': report})

class PersonListView(generic.ListView):
    model = Person
    template_name = 'cadhflow/person_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'persons'  # Default: object_list
    paginate_by = 25
    queryset = Person.objects.order_by('name')

def person_new(request):
	if request.method == "POST":
		form = PersonForm(request.POST)
		if form.is_valid():
			person = form.save()
			return redirect('cashflow:person_list')
	else:
		form = PersonForm()
	return render(request, 'cashflow/person_edit.html', {'form': form})

def person_edit(request, pk):
	person = get_object_or_404(Person, pk=pk)
	if request.method == "POST":
		form = PersonForm(request.POST, instance=person)
		if form.is_valid():
			person = form.save()
			return redirect('cashflow:person_list')
	else:
		form = PersonForm(instance=person)
	return render(request, 'cashflow/person_edit.html', {'form': form})

def person_import(request):
    if request.method == "POST":
        form = PersonImportForm(request.POST)
        if form.is_valid():
            for name in form.cleaned_data['person_list'].splitlines():
                person = Person(group=form.cleaned_data['group'], name=name)
                person.save()
            return redirect('cashflow:person_list')
    else:
        form = PersonImportForm()

    return render(request, 'cashflow/person_import.html', {'form': form})


def item_get_value(request, pk):
	item = get_object_or_404(Item, pk=pk)
	data = {
		'value': item.value
	}
	return JsonResponse(data)

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
