from django.contrib import admin

from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_name', 'parent', 'url', 'named_url')
    list_filter = ('menu_name',)
    search_fields = ('name', 'url', 'named_url')


admin.site.register(MenuItem, MenuItemAdmin)
