from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50, choices=[("asset", "Asset"), ("liability", "Liability"), ("equity", "Equity"), ("revenue", "Revenue"), ("expense", "Expense")], default="asset")
    code = models.CharField(max_length=255, blank=True, default="")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("sent", "Sent"), ("paid", "Paid"), ("overdue", "Overdue"), ("void", "Void")], default="draft")
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number

class Payment(models.Model):
    reference = models.CharField(max_length=255)
    payer = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    method = models.CharField(max_length=50, choices=[("bank_transfer", "Bank Transfer"), ("cash", "Cash"), ("card", "Card"), ("upi", "UPI"), ("cheque", "Cheque")], default="bank_transfer")
    date = models.DateField(null=True, blank=True)
    invoice_ref = models.CharField(max_length=255, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.reference
