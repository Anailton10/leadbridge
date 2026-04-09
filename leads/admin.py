from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "contact", "promoter", "created_at")
    search_fields = ("name", "city", "contact")
    list_filter = ("promoter",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
