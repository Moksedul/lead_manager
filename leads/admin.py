from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin):
    list_display = (
        "full_name", "phone_number", "email",
        "created_time", "assigned_member", "assigned_to", 'uploaded_time',
        'status', 'contacted',
                    )
