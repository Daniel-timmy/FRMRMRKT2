# Generated by Django 5.1.5 on 2025-02-02 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_product_category_alter_product_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 2, 12, 20, 58, 952686)),
        ),
    ]
