import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Account, Invoice, Payment


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['account_count'] = Account.objects.count()
    ctx['account_asset'] = Account.objects.filter(account_type='asset').count()
    ctx['account_liability'] = Account.objects.filter(account_type='liability').count()
    ctx['account_equity'] = Account.objects.filter(account_type='equity').count()
    ctx['account_total_balance'] = Account.objects.aggregate(t=Sum('balance'))['t'] or 0
    ctx['invoice_count'] = Invoice.objects.count()
    ctx['invoice_draft'] = Invoice.objects.filter(status='draft').count()
    ctx['invoice_sent'] = Invoice.objects.filter(status='sent').count()
    ctx['invoice_paid'] = Invoice.objects.filter(status='paid').count()
    ctx['invoice_total_amount'] = Invoice.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['payment_count'] = Payment.objects.count()
    ctx['payment_bank_transfer'] = Payment.objects.filter(method='bank_transfer').count()
    ctx['payment_cash'] = Payment.objects.filter(method='cash').count()
    ctx['payment_card'] = Payment.objects.filter(method='card').count()
    ctx['payment_total_amount'] = Payment.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['recent'] = Account.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def account_list(request):
    qs = Account.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(account_type=status_filter)
    return render(request, 'account_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def account_create(request):
    if request.method == 'POST':
        obj = Account()
        obj.name = request.POST.get('name', '')
        obj.account_type = request.POST.get('account_type', '')
        obj.code = request.POST.get('code', '')
        obj.balance = request.POST.get('balance') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/accounts/')
    return render(request, 'account_form.html', {'editing': False})


@login_required
def account_edit(request, pk):
    obj = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.account_type = request.POST.get('account_type', '')
        obj.code = request.POST.get('code', '')
        obj.balance = request.POST.get('balance') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/accounts/')
    return render(request, 'account_form.html', {'record': obj, 'editing': True})


@login_required
def account_delete(request, pk):
    obj = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/accounts/')


@login_required
def invoice_list(request):
    qs = Invoice.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(invoice_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'invoice_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def invoice_create(request):
    if request.method == 'POST':
        obj = Invoice()
        obj.invoice_number = request.POST.get('invoice_number', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.tax = request.POST.get('tax') or 0
        obj.status = request.POST.get('status', '')
        obj.due_date = request.POST.get('due_date') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/invoices/')
    return render(request, 'invoice_form.html', {'editing': False})


@login_required
def invoice_edit(request, pk):
    obj = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        obj.invoice_number = request.POST.get('invoice_number', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.tax = request.POST.get('tax') or 0
        obj.status = request.POST.get('status', '')
        obj.due_date = request.POST.get('due_date') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/invoices/')
    return render(request, 'invoice_form.html', {'record': obj, 'editing': True})


@login_required
def invoice_delete(request, pk):
    obj = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/invoices/')


@login_required
def payment_list(request):
    qs = Payment.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(reference__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(method=status_filter)
    return render(request, 'payment_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def payment_create(request):
    if request.method == 'POST':
        obj = Payment()
        obj.reference = request.POST.get('reference', '')
        obj.payer = request.POST.get('payer', '')
        obj.amount = request.POST.get('amount') or 0
        obj.method = request.POST.get('method', '')
        obj.date = request.POST.get('date') or None
        obj.invoice_ref = request.POST.get('invoice_ref', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/payments/')
    return render(request, 'payment_form.html', {'editing': False})


@login_required
def payment_edit(request, pk):
    obj = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        obj.reference = request.POST.get('reference', '')
        obj.payer = request.POST.get('payer', '')
        obj.amount = request.POST.get('amount') or 0
        obj.method = request.POST.get('method', '')
        obj.date = request.POST.get('date') or None
        obj.invoice_ref = request.POST.get('invoice_ref', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/payments/')
    return render(request, 'payment_form.html', {'record': obj, 'editing': True})


@login_required
def payment_delete(request, pk):
    obj = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/payments/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['account_count'] = Account.objects.count()
    data['invoice_count'] = Invoice.objects.count()
    data['payment_count'] = Payment.objects.count()
    return JsonResponse(data)
