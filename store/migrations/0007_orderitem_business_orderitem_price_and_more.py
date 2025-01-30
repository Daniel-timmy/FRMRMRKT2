# Generated by Django 5.1.4 on 2025-01-29 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer'),
        ),
    ]
