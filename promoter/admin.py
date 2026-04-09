from django.contrib import admin
from .models import State, Promoter


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "sigla")
    search_fields = ("name", "sigla")
    ordering = ("name",)


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ("name", "last_name", "state", "contact")
    search_fields = ("name", "last_name", "contact")
    list_filter = ("state",)
    ordering = ("name",)
