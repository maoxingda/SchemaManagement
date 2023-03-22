from admin_decorators import short_description
from django.db import models


# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe


class DbConn(models.Model):
    class DbType(models.TextChoices):
        mysql = 'MySQL'
        postgres = 'PostgreSQL'

    name = models.CharField('数据库', max_length=128, unique=True)  # TODO MySQL从数据库地址截取 pg库必填
    db_type = models.CharField('类型', max_length=16, choices=DbType.choices, default=DbType.postgres)
    dns = models.CharField('地址', max_length=256)
    port = models.SmallIntegerField('端口号', default=5432)
    user = models.CharField('用户', max_length=256)
    password = models.CharField('密码', max_length=256)
    schema = models.CharField('schema', max_length=128)

    target_schema = models.CharField('目标表', max_length=128, blank=True, default='temp', help_text='可选参数 默认为：temp')
    target_table_name_prefix = models.CharField('目标表前缀', max_length=128, blank=True, help_text='可选参数 默认为：数据库 + _')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/admin/{self._meta.app_label}/{self._meta.model_name}/{self.id}/change/'

    def server_address(self):
        return f'{DbConn.DbType.mysql.name if self.db_type == DbConn.DbType.mysql else DbConn.DbType.postgres.name}://' \
               f'{self.user}:{self.password}@{self.dns}:{self.port}/{self.name}'


class Table(models.Model):
    class Meta:
        ordering = [
            'conn',
            'name',
        ]

    name = models.CharField('表', max_length=128)
    conn = models.ForeignKey(DbConn, verbose_name='数据库地址', on_delete=models.CASCADE, related_name='tables')

    def __str__(self):
        return self.name

    @short_description('操作')
    def actions_html(self):
        buttons = [f'<a href="{self.conn.get_absolute_url()}">所属数据库</a>']
        return mark_safe('&emsp;&emsp'.join(buttons))
