from django.contrib import admin
from . import models


@admin.register(models.Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = 'id', 'severity'


@admin.register(models.Brief)
class BriefAdmin(admin.ModelAdmin):
    list_display = 'id', 'title'
