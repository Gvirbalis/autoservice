# Generated by Django 5.1.3 on 2024-12-05 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0016_rename_reader_uzsakymas_savininkas'),
    ]

    operations = [
        migrations.AddField(
            model_name='uzsakymas',
            name='bus_sutvarkyta',
            field=models.DateField(blank=True, null=True, verbose_name='Bus sutvarkyta'),
        ),
        migrations.AlterField(
            model_name='uzsakymas',
            name='data',
            field=models.DateField(blank=True, null=True, verbose_name='Data'),
        ),
    ]
