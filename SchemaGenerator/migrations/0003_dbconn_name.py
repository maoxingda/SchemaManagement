# Generated by Django 4.1 on 2023-03-21 02:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SchemaGenerator', '0002_alter_dbconn_dns'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbconn',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='数据库'),
            preserve_default=False,
        ),
    ]