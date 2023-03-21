# Generated by Django 4.1 on 2023-03-21 04:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SchemaGenerator', '0008_alter_dbconn_db_type_alter_dbconn_dns'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbconn',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=256, verbose_name='密码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dbconn',
            name='user',
            field=models.CharField(default=django.utils.timezone.now, max_length=256, verbose_name='用户'),
            preserve_default=False,
        ),
    ]
