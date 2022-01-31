from django.contrib import admin

# Register your models here.
from .models import *

from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class carResource(resources.ModelResource):
    class Meta:
        model = car

class spareResource(resources.ModelResource):
    class Meta:
        model = spare

class carAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=("car_manufacturer","car_model","transmission","carfrom","carto")
    search_fields=("car_manufacturer","car_model")
    list_filter=("car_manufacturer",)
    ordering = ('car_manufacturer', 'car_model')
    resource_class = carResource

class engineAdmin(admin.ModelAdmin):
    list_display=("engine_ide","engine_l","engine_type","engine_cylinder","engine_pistons")
    search_fields=("engine_ide","engine_l","engine_cylinder")
    list_filter=("engine_l",)
    ordering = ('engine_ide', 'engine_l')
    filter_horizontal=["car_engine_info",]
    exclude=("engine_power_kw","engine_power_hp",)

class spareAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    # raw_id_fields=("car_info","engine_info",)
    list_display=("spare_code","spare_name","spare_category","note")
    search_fields=("spare_code","spare_name")
    list_filter=("spare_category",)
    ordering = ('spare_code',"spare_name")
    filter_horizontal=["car_info","engine_info","spare_spare","spare_vendor"]
    exclude=("spare_brand","shape",)
    autocomplete_fields = ("spare_category",)
    resource_class = spareResource

class vendorAdmin(admin.ModelAdmin):
    list_display=("vendorName",)
    search_fields=("vendorName",)
    list_filter=("vendorName",)
    ordering = ('vendorName',)

class categoryAdmin(admin.ModelAdmin):
    list_display=("category",)
    search_fields=("category",)
    # list_filter=("category",)
    ordering = ('category',)
    # autocomplete_fields = ("category",)
    # list_filter=("category",)


class dimensionAdmin(admin.ModelAdmin):
    list_display=("dimensionSpare","atributeName","atributeVal")
    list_filter=("atributeName",)
    ordering = ("dimensionSpare","atributeName","atributeVal")
    autocomplete_fields = ("dimensionSpare",)

    def response_add(self, request, obj, post_url_continue=None):
            if '_addanother' in request.POST:
                url = reverse("admin:spareapp_dimension_add")

                dimensionSpare = request.POST['dimensionSpare']
                qs2 = '?dimensionSpare=%s' % dimensionSpare

                return HttpResponseRedirect(''.join((url, qs2)))
            else:
                return HttpResponseRedirect(reverse("admin:spareapp_dimension_changelist"))

    def response_change(self, request, obj, post_url_continue=None):
        if '_addanother' in request.POST:
            url = reverse("admin:spareapp_dimension_add")
            dimensionSpare = request.POST['dimensionSpare']
            qs2 = '?dimensionSpare=%s' % dimensionSpare
            return HttpResponseRedirect(''.join((url, qs2)))
        else:
            return HttpResponseRedirect(reverse("admin:spareapp_dimension_changelist"))

class atributeAdmin(admin.ModelAdmin):
    list_display=("atributeSpare","atributeName","atributeVal")
    # search_fields=("atributeName","atributeVal")
    list_filter=("atributeName",)
    ordering = ("atributeSpare","atributeName","atributeVal")
    # raw_id_fields=("atributeSpare",)
    # filter_horizontal=["atributeSpare",]
    autocomplete_fields = ("atributeSpare",)

    def response_add(self, request, obj, post_url_continue=None):
            if '_addanother' in request.POST:
                url = reverse("admin:spareapp_atribute_add")
                # atributeCategory = request.POST['atributeCategory']
                # qs = '?atributeCategory=%s' % atributeCategory

                atributeSpare = request.POST['atributeSpare']
                qs2 = '?atributeSpare=%s' % atributeSpare

                return HttpResponseRedirect(''.join((url, qs2)))
            else:
                return HttpResponseRedirect(reverse("admin:spareapp_atribute_changelist"))

    def response_change(self, request, obj, post_url_continue=None):
        if '_addanother' in request.POST:
            url = reverse("admin:spareapp_atribute_add")
            # atributeCategory = request.POST['atributeCategory']
            # qs = '?atributeCategory=%s' % atributeCategory
            atributeSpare = request.POST['atributeSpare']
            qs2 = '?atributeSpare=%s' % atributeSpare
            return HttpResponseRedirect(''.join((url, qs2)))
        else:
            return HttpResponseRedirect(reverse("admin:spareapp_atribute_changelist"))

class referenceAdmin(admin.ModelAdmin):
    list_display=("referenceSpare","referenceNote","referenceCode")
    # search_fields=("atributeName","atributeVal")
    # list_filter=("referenceSpare",)
    ordering = ("referenceSpare","referenceCode")
    # raw_id_fields=("referenceCar",)
    # readonly_fields=["referenceCar",]
    autocomplete_fields = ("referenceSpare",)


    def response_add(self, request, obj, post_url_continue=None):
            if '_addanother' in request.POST:
                url = reverse("admin:spareapp_reference_add")

                referenceSpare = request.POST['referenceSpare']
                qs2 = '?referenceSpare=%s' % referenceSpare

                return HttpResponseRedirect(''.join((url, qs2)))
            else:
                return HttpResponseRedirect(reverse("admin:spareapp_reference_changelist"))

    def response_change(self, request, obj, post_url_continue=None):
        if '_addanother' in request.POST:
            url = reverse("admin:spareapp_reference_add")
            referenceSpare = request.POST['referenceSpare']
            qs2 = '?referenceSpare=%s' % referenceSpare
            return HttpResponseRedirect(''.join((url, qs2)))
        else:
            return HttpResponseRedirect(reverse("admin:spareapp_reference_changelist"))

class spareCartAdmin(admin.ModelAdmin):
    list_display=("spareId","spareCode","nameUser",)
    search_fields=("spareCode",)

admin.site.register(car,carAdmin)
admin.site.register(engine,engineAdmin)
admin.site.register(spare,spareAdmin)
admin.site.register(category,categoryAdmin)
admin.site.register(vendor,vendorAdmin)
admin.site.register(reference,referenceAdmin)
admin.site.register(dimension,dimensionAdmin)
admin.site.register(atribute,atributeAdmin)
admin.site.register(Profile)
admin.site.register(persona)
admin.site.register(factType)
admin.site.register(factCategory)
admin.site.register(factura)
admin.site.register(mainTable)
admin.site.register(mainTableAux)
admin.site.register(customTable)
admin.site.register(tableOperacion)
admin.site.register(tableOperacionCat)
# admin.site.register(spareCart,spareCartAdmin)

admin.site.site_header = "Auto Repuestos Interamericana administrator"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Welcome to Auto Repuestos Interamericana administrator panel"