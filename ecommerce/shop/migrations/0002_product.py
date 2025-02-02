# Generated by Django 5.0.6 on 2024-07-04 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=20)),
                ('p_desc', models.TextField()),
                ('p_image', models.ImageField(blank=True, null=True, upload_to='media/products')),
                ('p_stock', models.IntegerField()),
                ('p_available', models.BooleanField(default=True)),
                ('p_created', models.DateTimeField(auto_now_add=True)),
                ('p_updated', models.DateTimeField(auto_now=True)),
                ('p_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
        ),
    ]
