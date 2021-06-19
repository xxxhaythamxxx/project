from django.contrib import admin

# Register your models here.
from .models import *

from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse

class carAdmin(admin.ModelAdmin):
    list_display=("car_manufacturer","car_model","transmission","carfrom","carto")
    search_fields=("car_manufacturer","car_model")
    list_filter=("car_manufacturer",)
    ordering = ('car_manufacturer', 'car_model')

class engineAdmin(admin.ModelAdmin):
    list_display=("engine_ide","engine_l","engine_type","engine_cylinder","engine_pistons","engine_power_kw","engine_power_hp")
    search_fields=("engine_ide","engine_l","engine_cylinder")
    list_filter=("engine_l",)
    ordering = ('engine_ide', 'engine_l')

class spareAdmin(admin.ModelAdmin):
    list_display=("spare_code","spare_brand","spare_name","spare_category")
    search_fields=("spare_code","spare_brand")
    list_filter=("spare_name",)
    ordering = ('spare_code', 'spare_brand',"spare_name")

class dimensionAdmin(admin.ModelAdmin):
    list_display=("dimensionSpare","atributeName","atributeVal")
    search_fields=("atributeName","atributeVal")
    list_filter=("dimensionCategory","atributeName","dimensionSpare")
    ordering = ("dimensionSpare","atributeName","atributeVal")

    def response_add(self, request, obj, post_url_continue=None):
            if '_addanother' in request.POST:
                url = reverse("admin:spareapp_dimension_add")
                dimensionCategory = request.POST['dimensionCategory']
                qs = '?dimensionCategory=%s' % dimensionCategory

                dimensionSpare = request.POST['dimensionSpare']
                qs2 = '&dimensionSpare=%s' % dimensionSpare

                return HttpResponseRedirect(''.join((url, qs, qs2)))
            else:
                return HttpResponseRedirect(reverse("admin:spareapp_dimension_changelist"))

    def response_change(self, request, obj, post_url_continue=None):
        if '_addanother' in request.POST:
            url = reverse("admin:spareapp_dimension_add")
            dimensionCategory = request.POST['dimensionCategory']
            qs = '?dimensionCategory=%s' % dimensionCategory
            dimensionSpare = request.POST['dimensionSpare']
            qs2 = '&dimensionSpare=%s' % dimensionSpare
            return HttpResponseRedirect(''.join((url, qs, qs2)))
        else:
            return HttpResponseRedirect(reverse("admin:spareapp_dimension_changelist"))


admin.site.register(car,carAdmin)
admin.site.register(engine,engineAdmin)
admin.site.register(spare,spareAdmin)
admin.site.register(category)
admin.site.register(reference)
admin.site.register(dimension,dimensionAdmin)
