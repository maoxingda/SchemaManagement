# Generated by Django 4.1 on 2023-03-21 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchemaGenerator', '0010_dbconn_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbconn',
            name='target_schema',
            field=models.CharField(blank=True, default='temp', help_text='可选参数 默认为：temp', max_length=128, verbose_name='目标表'),
        ),
        migrations.AddField(
            model_name='dbconn',
            name='target_table_name_prefix',
            field=models.CharField(blank=True, help_text='可选参数 默认为：local.database + _', max_length=128, verbose_name='目标表前缀'),
        ),
    ]
