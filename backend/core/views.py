import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import Record


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
    total = Record.objects.count()
    active = Record.objects.filter(status='active').count()
    pending = Record.objects.filter(status='pending').count()
    inactive = Record.objects.filter(status='inactive').count()
    recent = Record.objects.all()[:10]
    return render(request, 'dashboard.html', {
        'total': total, 'active': active, 'pending': pending,
        'inactive': inactive, 'recent': recent,
    })


@login_required
def records_view(request):
    records = Record.objects.all()
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    if status_filter:
        records = records.filter(status=status_filter)
    if search:
        records = records.filter(name__icontains=search)
    return render(request, 'records.html', {'records': records, 'status_filter': status_filter, 'search': search})


@login_required
def record_create(request):
    if request.method == 'POST':
        Record.objects.create(
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            status=request.POST.get('status', 'active'),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            amount=request.POST.get('amount', 0) or 0,
            notes=request.POST.get('notes', ''),
        )
        return redirect('/records/')
    return render(request, 'record_form.html', {'editing': False})


@login_required
def record_edit(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.name = request.POST.get('name', record.name)
        record.description = request.POST.get('description', record.description)
        record.status = request.POST.get('status', record.status)
        record.email = request.POST.get('email', record.email)
        record.phone = request.POST.get('phone', record.phone)
        record.amount = request.POST.get('amount', record.amount) or 0
        record.notes = request.POST.get('notes', record.notes)
        record.save()
        return redirect('/records/')
    return render(request, 'record_form.html', {'record': record, 'editing': True})


@login_required
def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
    return redirect('/records/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


# API endpoints
@login_required
def api_stats(request):
    return JsonResponse({
        'total': Record.objects.count(),
        'active': Record.objects.filter(status='active').count(),
        'pending': Record.objects.filter(status='pending').count(),
        'inactive': Record.objects.filter(status='inactive').count(),
    })
