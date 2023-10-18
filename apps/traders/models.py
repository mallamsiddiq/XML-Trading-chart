import datetime
from typing import Any
from djongo import models
from django.contrib.auth import get_user_model
from authapp.models import Trader

from abc import abstractclassmethod

class NoNegativeError(Exception):
    "Only positive amount are allowed in transaction"

class NoPositiveError(Exception):
    "Only negative amount are allowed in transaction"

from django.db.models import Sum

class Transaction(models.Model):

    class TypeChoice(models.TextChoices):
        
        Credit = "Credit", "Credit"
        Debit = "Debit", "Debit"
        Transaction = "Transaction", "Transaction"
        
    type = models.CharField(max_length = 20, choices = TypeChoice.choices, default = TypeChoice.Transaction)
    customer = models.ForeignKey(Trader, on_delete = models.CASCADE, related_name = 'transactions')

    created_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateTimeField(default = datetime.date(2022,10,22))

    checque_no = models.IntegerField(null = True, unique = True)
    description = models.CharField(max_length= 64)

    amount = models.FloatField(default = 0)

    #   saving the most recent balance here
    balance = models.FloatField(default = 0)
    
    
    @abstractclassmethod
    def amount_validation(self):
        ""

    class Meta:
        # ordering = ['-created_date']
        get_latest_by = ["created_date", 'pk']

    def __str__(self):

        return f"[{self.type.upper()} TRANSACTION] -- {self.description}"


class Credit(Transaction):

    @property
    def creditamount(self):
        return self.amount
    
    def amount_validation(self):
        if self.amount < 0:
            raise NoNegativeError

    def save(self, *args, **kwargs):
        self.amount_validation()
        current_balance = self.customer.balance + self.creditamount

        self.customer.balance = current_balance
        self.customer.save()
        self.balance = current_balance
        self.type = "Credit"
        super(Credit, self).save(*args, **kwargs)


class Debit(Transaction):

    @property
    def debitamount(self):
        return abs(self.amount)
    
    def amount_validation(self):
        ""

    def save(self, *args, **kwargs):
        self.amount_validation()
        current_balance = self.customer.balance - self.debitamount
        self.customer.balance = current_balance
        self.customer.save()
        self.balance = current_balance
        self.amount = - self.debitamount
        self.type = 'Debit'
        super(Debit, self).save(*args, **kwargs)

class Report(models.Model):

    def __init__(self, trader, from_date, to_date = datetime.datetime.now(), **kwargs) -> None:

        self.date_now = datetime.datetime.now()
        self.trader = trader
        self.from_date = from_date
        self.to_date = to_date

    @property
    def transactions(self):
        end_date = self.end_date + datetime.timedelta(days=1)
        return self.customer.transactions.filter(created_date__range=[self.start_date, end_date])
    
    @property
    def balance(self):
        return