from django.contrib import admin
from .models import Account, Invoice, Payment

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "account_type", "code", "balance", "created_at"]
    list_filter = ["account_type"]
    search_fields = ["name", "code"]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "customer_name", "amount", "tax", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["invoice_number", "customer_name"]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["reference", "payer", "amount", "method", "date", "created_at"]
    list_filter = ["method"]
    search_fields = ["reference", "payer", "invoice_ref"]
