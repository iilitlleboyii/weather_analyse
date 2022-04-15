from django.contrib import admin

# Register your models here.
from region.models import Region


class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    list_editable = ['name', 'parent']


admin.site.register(Region, RegionAdmin)
