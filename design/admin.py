from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from design.models import Design, Card


@admin.register(Design)
class DesignImportExport(ImportExportModelAdmin):
    list_display = ['id', 'name', 'image']


@admin.register(Card)
class CardImportExport(ImportExportModelAdmin):
    list_display = ['id', 'first_name', 'last_name']




