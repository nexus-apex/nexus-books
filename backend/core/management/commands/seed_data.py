from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Account, Invoice, Payment
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusBooks with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusbooks.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Account.objects.count() == 0:
            for i in range(10):
                Account.objects.create(
                    name=f"Sample Account {i+1}",
                    account_type=random.choice(["asset", "liability", "equity", "revenue", "expense"]),
                    code=f"Sample {i+1}",
                    balance=round(random.uniform(1000, 50000), 2),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Account records created'))

        if Invoice.objects.count() == 0:
            for i in range(10):
                Invoice.objects.create(
                    invoice_number=f"Sample {i+1}",
                    customer_name=f"Sample Invoice {i+1}",
                    amount=round(random.uniform(1000, 50000), 2),
                    tax=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["draft", "sent", "paid", "overdue", "void"]),
                    due_date=date.today() - timedelta(days=random.randint(0, 90)),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Invoice records created'))

        if Payment.objects.count() == 0:
            for i in range(10):
                Payment.objects.create(
                    reference=f"Sample {i+1}",
                    payer=f"Sample {i+1}",
                    amount=round(random.uniform(1000, 50000), 2),
                    method=random.choice(["bank_transfer", "cash", "card", "upi", "cheque"]),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    invoice_ref=f"Sample {i+1}",
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Payment records created'))
