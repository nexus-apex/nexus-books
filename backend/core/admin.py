from django.contrib import admin
from .models import Record

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'email', 'amount', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'description']
