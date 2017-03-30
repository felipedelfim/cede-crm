from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Transaction

class IndexView(generic.ListView):
	def get_queryset(self):
		"""Return the last five published questions."""
		return Transaction.objects.order_by('-updated_at')[:5]

class DetailView(generic.DetailView):
	model = Transaction

