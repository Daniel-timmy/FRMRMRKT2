# Generated by Django 5.1.5 on 2025-03-02 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_product_date_added_remove_wishlist_products_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 2, 14, 29, 48, 302308)),
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='products',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='products',
            field=models.ManyToManyField(to='store.product'),
        ),
    ]
