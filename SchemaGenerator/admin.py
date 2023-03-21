from django.contrib import admin

# Register your models here.
from SchemaGenerator.models import DbConn, Table


class TableInlineAdmin(admin.TabularInline):
    model = Table
    extra = 0


@admin.register(DbConn)
class DbConnAdmin(admin.ModelAdmin):
    inlines = (
        TableInlineAdmin,
    )
    radio_fields = {
        'db_type': admin.HORIZONTAL,
    }
    list_display = (
        'name',
        'server_address',
    )


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'actions_html',
        'conn',
    )
    list_filter = (
        'conn',
    )
