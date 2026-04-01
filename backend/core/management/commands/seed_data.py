from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Record
import os

# These get replaced per app by the customize script
APP_NAME = os.environ.get('APP_NAME', 'NexusBooks')
RECORDS = [
    ('Sample Record 1', 'First demo record', 'active', 'demo1@example.com', '+91-9876543210', 15000),
    ('Sample Record 2', 'Second demo record', 'active', 'demo2@example.com', '+91-9876543211', 25000),
    ('Sample Record 3', 'Third demo record', 'pending', 'demo3@example.com', '+91-9876543212', 8500),
    ('Sample Record 4', 'Fourth demo record', 'active', 'demo4@example.com', '+91-9876543213', 42000),
    ('Sample Record 5', 'Fifth demo record', 'inactive', 'demo5@example.com', '+91-9876543214', 12000),
    ('Sample Record 6', 'Sixth demo record', 'active', 'demo6@example.com', '+91-9876543215', 31000),
    ('Sample Record 7', 'Seventh demo record', 'pending', 'demo7@example.com', '+91-9876543216', 19500),
    ('Sample Record 8', 'Eighth demo record', 'active', 'demo8@example.com', '+91-9876543217', 55000),
    ('Sample Record 9', 'Ninth demo record', 'active', 'demo9@example.com', '+91-9876543218', 7800),
    ('Sample Record 10', 'Tenth demo record', 'inactive', 'demo10@example.com', '+91-9876543219', 23000),
]


class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **kwargs):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuscrm.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Create demo records
        if Record.objects.count() == 0:
            for name, desc, status, email, phone, amount in RECORDS:
                Record.objects.create(
                    name=name, description=desc, status=status,
                    email=email, phone=phone, amount=amount
                )
            self.stdout.write(self.style.SUCCESS(f'{len(RECORDS)} demo records created'))
        else:
            self.stdout.write('Records already exist, skipping seed')
