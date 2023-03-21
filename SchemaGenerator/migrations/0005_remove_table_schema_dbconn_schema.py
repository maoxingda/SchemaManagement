# Generated by Django 4.1 on 2023-03-21 02:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SchemaGenerator', '0004_table_schema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='schema',
        ),
        migrations.AddField(
            model_name='dbconn',
            name='schema',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='schema'),
            preserve_default=False,
        ),
    ]
