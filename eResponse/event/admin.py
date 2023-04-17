from django.contrib import admin

from eResponse.event.models import ThreadEvent, Role, LastEventToken


@admin.register(ThreadEvent)
class AdminThreadEvent(admin.ModelAdmin):
    list_display = 'id', 'timestamp'


@admin.register(Role)
class AdminRole(admin.ModelAdmin):
    list_display = 'id', 'timestamp'


@admin.register(LastEventToken)
class AdminLastEventToken(admin.ModelAdmin):
    list_display = 'token',
