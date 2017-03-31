from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Transaction
from .forms import TransactionForm

class IndexView(generic.ListView):
	def get_queryset(self):
		"""Return the last five published questions."""
		return Transaction.objects.order_by('-updated_at')[:5]

class DetailView(generic.DetailView):
	model = Transaction

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
