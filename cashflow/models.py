from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Transaction(models.Model):
	def __str__(self):
		return self.item.name + ' (' + str(self.amount) + ') '
	def was_paid(self):
		return self.paid_at is not None
	def pay(self):
		self.paid_at = timezone.now()
	def _get_transacted_at(self):
		if self.was_paid():
			return self.paid_at
		return self.created_at
	def save(self, *args, **kwargs):
		if not self.pk:
			self.item.add_inventory(-1 * self.amount)
		super(Transaction, self).save(args, kwargs)
	category = models.ForeignKey('Category', on_delete=models.PROTECT)
	item = models.ForeignKey('Item', on_delete=models.PROTECT)
	person = models.ForeignKey('Person', on_delete=models.PROTECT)
	method = models.ForeignKey('Method', on_delete=models.PROTECT)
	item_value = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	amount = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	total = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	comments = models.TextField(blank=True)
	paid_at = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated
	transacted_at = property(_get_transacted_at)
	class Meta:
		ordering = ["-updated_at"]

class Method(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200, unique=True)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated
	class Meta:
		ordering = ["name"]

class Item(models.Model):
	def __str__(self):
		return self.name
	def add_inventory(self, amount):
		self.inventory += amount
		if self.inventory < 0:
			self.inventory = 0
		self.save()
	name = models.CharField(max_length=200, unique=True)
	category = models.ForeignKey('Category', on_delete=models.PROTECT)
	cost_center = models.ForeignKey('CostCenter', on_delete=models.PROTECT)
	value = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	inventory = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated
	class Meta:
		ordering = ["name"]

class CostCenter(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200, unique=True)
	class Meta:
		ordering = ["name"]

class Category(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200, unique=True)
	class Meta:
		ordering = ["name"]

class Person(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200, unique=True)
	phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\(?\d{2}?\)?\d{8,10}$', message="Phone number must be entered in the format: '(11)999999999'. Up to 15 digits allowed.")], blank=True) # validators should be a list
	group = models.ForeignKey('Group', on_delete=models.PROTECT)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated
	class Meta:
		ordering = ["name"]

class Group(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200, unique=True)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated
	class Meta:
		ordering = ["name"]
