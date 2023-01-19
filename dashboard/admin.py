from django.contrib import admin

from .models import ApiData, BlingUser, Keys


class BlingUserAdmin(admin.ModelAdmin):
    ...


class ApiDataAdmin(admin.ModelAdmin):
    ...


class KeysAdmin(admin.ModelAdmin):
    ...


admin.site.register(BlingUser, BlingUserAdmin)
admin.site.register(ApiData, ApiDataAdmin)
admin.site.register(Keys, KeysAdmin)
