from django.contrib import admin

# Register your models here.
from .models import *

class carAdmin(admin.ModelAdmin):
    list_display=("car_manufacturer","car_model","transmission","car_from","car_to")
    search_fields=("car_manufacturer","car_model")
    list_filter=("car_manufacturer",)
    ordering = ('car_manufacturer', 'car_model')

class engineAdmin(admin.ModelAdmin):
    list_display=("engine_ide","engine_l","engine_type","engine_cylinder","engine_pistons","engine_power_kw","engine_power_hp")
    search_fields=("engine_ide","engine_l","engine_cylinder")
    list_filter=("engine_l",)
    ordering = ('engine_ide', 'engine_l')

class spareAdmin(admin.ModelAdmin):
    list_display=("spare_code","spare_brand","spare_name")
    search_fields=("spare_code","spare_brand")
    list_filter=("spare_name",)
    ordering = ('spare_code', 'spare_brand',"spare_name")

admin.site.register(car,carAdmin)
admin.site.register(engine,engineAdmin)
admin.site.register(spare,spareAdmin)
admin.site.register(category)
admin.site.register(reference)
