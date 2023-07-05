from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class AdminUser(admin.ModelAdmin):
    list_display = 'email', 'is_active', 'verify_credentials'

    @admin.display(description='Verify user status')
    def verify_credentials(self, obj):
        return obj.has_perm('')  # todo set permissions/groups
