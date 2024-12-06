# Generated by Django 5.1.3 on 2024-12-06 13:04

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0023_remove_custumerreview_uzsakymas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Naujienos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Data')),
                ('aprasymas', tinymce.models.HTMLField(help_text='Aprasymas', null=True, verbose_name='Aprasymas')),
            ],
        ),
        migrations.DeleteModel(
            name='CustumerReview',
        ),
    ]
