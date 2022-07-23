from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from account.models import Event, Invitation



@admin.register(Event)
class EventImportExport(ImportExportModelAdmin):
    list_display = ['id', 'name', 'user', 'city', 'country', 'capacity']


@admin.register(Invitation)
class InvitationImportExport(ImportExportModelAdmin):
    list_display = ['id', 'event', 'first_name', 'last_name','mobile', 'email', 'status', 'reference']


