from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, ListView
from django.template.defaultfilters import date as date_filter
import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.contrib import messages


from authapp.models import Trader

from .forms import DateForm

class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        if bool(getattr(self.request.user, 'trader', False)):
            messages.info(self.request, "Only your Dashboard is accesible to you")
            return redirect(reverse_lazy('dashboard'))

        messages.info(self.request, "You can't view other's transactions")
        return redirect(reverse_lazy('home'))
    

class OnlyTradersInMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):

        return bool(getattr(self.request.user, 'trader', False))

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.info(self.request, "You have no transactions, Consider Trading")
        return redirect(reverse_lazy('home'))

class DashboardBase:
    model = Trader
    template_name = 'traders/publicprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start = self.request.GET.get('start')
        end = self.request.GET.get('end')

        trader = self.get_trader(context)

        transactions = trader.transactions.all()

        if start:
            transactions = transactions.filter(created_date__gte=start)
        if end:
            transactions = transactions.filter(created_date__lte=end)

        timestamps = [date_filter(transaction.created_date, "c") for transaction in transactions]
        profit_loss = [transaction.balance for transaction in transactions]
        prev_balance = [(transaction.balance - transaction.amount, transaction.balance)[transaction.amount < 0 and transaction.balance - transaction.amount > 0] for transaction in transactions]
        bar_data = [(transaction.amount, abs(transaction.amount))[(transaction.balance - transaction.amount) > 0] for transaction in transactions]

        context.update({
            'data_labels': json.dumps(timestamps),
            'data_values': profit_loss,
            'bar_data': bar_data,
            'prev_balance': prev_balance,
            'transactions': transactions,
            'dateform': DateForm,
        })

        return context

class DasboardView(OnlyTradersInMixin, DashboardBase, TemplateView):
    
    def get_trader(self, _):
        return Trader.objects.get(user_ptr=self.request.user)

class TraderDasboardView(AdminRequiredMixin, DashboardBase, DetailView):
    model = Trader
    slug_field = 'pk'
    slug_url_kwarg = 'trader_id'

    def get_trader(self, context):
        
        return context['object'] 

class AllTradersView(ListView):
    model = Trader
    template_name = 'traders/home.html'
    context_object_name = 'user_profiles'
