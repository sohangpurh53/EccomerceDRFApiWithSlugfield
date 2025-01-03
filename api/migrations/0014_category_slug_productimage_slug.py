# Generated by Django 4.2.1 on 2023-10-18 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=True, max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='productimage',
            name='slug',
            field=models.SlugField(default=True, max_length=200, unique=True),
        ),
    ]
