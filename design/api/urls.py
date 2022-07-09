from django.urls import path
from design.api.views import get_all_designs, export_data, import_data


urlpatterns = [
    path('designs/', get_all_designs, name='get_all_designs'),
    path('export/', export_data, name='export_data'),
    path('import/', import_data, name='import_data'),
]