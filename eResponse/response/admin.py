from django.contrib import admin
from eResponse.response.models import Emergency, Brief


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = 'id', 'severity'


@admin.register(Brief)
class BriefAdmin(admin.ModelAdmin):
    list_display = 'id', 'title'
