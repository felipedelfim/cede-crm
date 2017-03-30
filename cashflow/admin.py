from django.contrib import admin

# Register your models here.

from .models import Group

admin.site.register(Group)

from .models import Person

admin.site.register(Person)

from .models import Item

admin.site.register(Item)

from .models import Method

admin.site.register(Method)

from .models import Transaction

admin.site.register(Transaction)