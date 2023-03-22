import textwrap

import psycopg2
import sqlparse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.safestring import mark_safe

from SchemaGenerator.models import DbConn


def schema_generate(request, dbconn_id):
    new_line = '",\n            "'
    dbconn = get_object_or_404(DbConn, id=dbconn_id)
    locals_template = textwrap.dedent(f'''
        locals {{
          engine_name = "{DbConn.DbType.mysql.name if dbconn.db_type == DbConn.DbType.mysql else DbConn.DbType.postgres.name}" # mysql | postgres
          username    = "{dbconn.user}"
          password    = "{dbconn.password}"
          server_name = "{dbconn.dns}"
          port        = "{dbconn.port}"
          database    = "{dbconn.name}"
          schema_name = "{dbconn.schema}" # mysql不支持schema 填数据库名称
          tables      = [
            "{new_line.join([t.name for t in dbconn.tables.all()])}"
          ]
        
          target_schema_name       = "" # 可选参数 默认为：temp
          target_table_name_prefix = "" # 可选参数 默认为：local.database + '_'
        }}
    ''')

    with open('/Users/maoxd/open-source/my-terraform/main-sync-schema-locals.tf', 'w') as f:
        f.write(locals_template)

    messages.info(request, mark_safe(f'<pre>{locals_template}</pre>'))

    return redirect(dbconn)


def redshift_schema_generate(request, dbconn_id):
    req_schema = request.GET.get('schema')
    dbconn = get_object_or_404(DbConn, id=dbconn_id)
    dw_dbconn = get_object_or_404(DbConn, name='beta')
    table_name_prefix = f'{dbconn.name}'
    if dbconn.target_table_name_prefix:
        table_name_prefix = f'{dbconn.target_table_name_prefix}'
    with psycopg2.connect(dw_dbconn.server_address()) as conn:
        with conn.cursor() as cursor:
            ddl_sql = ''
            for table in dbconn.tables.all():
                query_columns_sql = f"select column_name, data_type, character_maximum_length, numeric_precision, numeric_scale " \
                                    f"from pg_catalog.svv_all_columns where schema_name = '{dbconn.target_schema}' and table_name = '{table_name_prefix }_{table.name}'"
                print(query_columns_sql)
                cursor.execute(query_columns_sql)
                columns = cursor.fetchall()
                max_column_lengh = max([len(column) for column, _, _, _, _ in columns] + [1])
                max_column_lengh = 25 if max_column_lengh < 25 else max_column_lengh

                external = ''
                if_not_exists = ''
                if req_schema == 'emr':
                    external = 'external'
                else:
                    if_not_exists = 'if not exists'

                ddl_sql += f'create {external} table {if_not_exists} {req_schema}.{"db_" if req_schema == "ods" else ""}{dbconn.name}_{table.name}\n' \
                           f'(\n'
                for column, data_type, column_lengh, numeric_precision, numeric_scale in columns:
                    if data_type in ('smallint', 'integer', 'bigint', 'date', 'timestamp', 'real', 'double precision'):
                        ddl_sql += f'    {column.ljust(max_column_lengh)} {data_type},\n'
                    elif data_type in ('timestamp without time zone',):
                        ddl_sql += f'    {column.ljust(max_column_lengh)} timestamp,\n'
                    elif data_type in ('numeric',):
                        ddl_sql += f'    {column.ljust(max_column_lengh)} {data_type}({numeric_precision}, {numeric_scale}),\n'
                    elif data_type in ('string', 'character varying'):
                        if column == 'op':
                            ddl_sql += f'    {column.ljust(max_column_lengh)} char(1),\n'
                        else:
                            ddl_sql += f'    {column.ljust(max_column_lengh)} varchar({column_lengh}),\n'
                    else:
                        messages.error(request, mark_safe(f'<pre>未知数据类型：{dbconn.target_schema, table.name, column, data_type}</pre>'))

                ddl_sql += f"    {'commit_timestamp'.ljust(max_column_lengh)} varchar(50),\n"
                ddl_sql += f"    {'op'.ljust(max_column_lengh)} char(1),\n"
                ddl_sql += f"    {'cdc_transact_id'.ljust(max_column_lengh)} varchar(50),\n"
                if req_schema == 'ods':
                    ddl_sql += f"    {'event_time'.ljust(max_column_lengh)} varchar(128),\n"
                    ddl_sql += f"    {'timestamp_executed_insert'.ljust(max_column_lengh)} timestamp default sysdate + interval '8h',\n"
                    ddl_sql += f"    {'timestamp_executed_update'.ljust(max_column_lengh)} timestamp default sysdate + interval '8h'\n"
                else:
                    ddl_sql = ddl_sql[:-2] + '\n'
                ddl_sql += ')\n'
                if req_schema == 'emr':
                    ddl_sql += 'partitioned by (event_time varchar(128))\n'
                    ddl_sql += 'stored as parquet\n'
                    ddl_sql += f"location 's3://bi-data-lake/realtime-cdc/id-mapping/id_mapping'\n"
                ddl_sql += f";\n\n"

    if settings.DEBUG:
        with open(f'{req_schema}-create-table-ddl.sql', 'w') as f:
            f.write('\n-- 建表语句\n' + ddl_sql)

    messages.info(request, mark_safe(f'<pre>{ddl_sql}</pre>'))

    return redirect(dbconn)


def redshift_create_table(request, dbconn_id):
    req_schema = request.GET.get('schema')
    dbconn = get_object_or_404(DbConn, id=dbconn_id)
    dw_dbconn = get_object_or_404(DbConn, name='beta')

    with open(f'{req_schema}-create-table-ddl.sql') as f:
        sql_stmts = f.read()

    with psycopg2.connect(dw_dbconn.server_address()) as conn:
        with conn.cursor() as cursor:
            for sql_stmt in sqlparse.split(sql_stmts):
                messages.info(request, mark_safe(f'<pre>{sql_stmt}</pre>'))
                cursor.execute(sql_stmt)

    return redirect(dbconn)
