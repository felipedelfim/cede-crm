from django.contrib import admin

# Register your models here.

from .models import Group, Person, Item, CostCenter, Method, Transaction

admin.site.register(Group)

admin.site.register(Person)

admin.site.register(Item)

admin.site.register(CostCenter)

admin.site.register(Method)

admin.site.register(Transaction)
