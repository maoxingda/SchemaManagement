from django.urls import path
from . import views

# app_name = 'schema-generator'

urlpatterns = [
    path('dbconn/<int:dbconn_id>/generate/', views.schema_generate, name='schema_generate'),
    path('dbconn/<int:dbconn_id>/redshift/generate/', views.redshift_schema_generate, name='redshift_schema_generate'),
    path('dbconn/<int:dbconn_id>/redshift/create-table/', views.redshift_create_table, name='redshift_create_table'),
]
