# Generated by Django 5.1.4 on 2025-01-29 16:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_customer_business_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 29, 17, 3, 11, 98708)),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(default='New', max_length=20, null=True),
        ),
    ]
