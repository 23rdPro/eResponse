from django.contrib import admin

from eResponse.event.models import ThreadEvent


@admin.register(ThreadEvent)
class AdminThreadEvent(admin.ModelAdmin):
    list_display = 'id', 'timestamp'
