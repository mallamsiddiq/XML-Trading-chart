from django.contrib import admin
from .models import Transaction, Credit, Debit

admin.site.register(Transaction)

admin.site.register(Credit)
admin.site.register(Debit)

# Register your models here.
