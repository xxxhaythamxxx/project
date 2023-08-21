from django.db import models
from django.db.models.deletion import CASCADE
# from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey
from django.utils.timezone import now
from datetime import datetime, timezone
from datetime import timedelta
import os
from django.db import models
from django.contrib.auth.models import User
# from flask_sqlalchemy import SQLAlchemy

# Create your models here.

class vendor(models.Model):
    vendorName=models.CharField(max_length=40, verbose_name="Vendor name",blank=True,null=True)

    def __str__(self):
        return '%s' %(self.vendorName)
    
class transmission(models.Model):
    trans=models.CharField(max_length=20, verbose_name="Transmission", blank=True,null=True)

    def __str__(self):
        return '%s' %(self.trans)

class manufacturer(models.Model):
    manufacturer=models.CharField(max_length=40, verbose_name="Manufacturer",blank=True,null=True)

    class Meta:
        verbose_name_plural = "Manufacturers"

    def __str__(self):
        return '%s' %(self.manufacturer)

class branddb(models.Model):
    brand=models.CharField(max_length=100, verbose_name="Brand",blank=True,null=True)
    # brandPrice=models.FloatField(verbose_name="Price", blank=True,null=True)
    # cantidad = models.IntegerField(verbose_name="Quantity", blank=True,null=True)
    # vendor = models.ForeignKey(vendor,on_delete=CASCADE,verbose_name="Vendor",blank=True,null=True)

    class Meta:
        verbose_name_plural = "Brands"

    def __str__(self):
        return '%s' %(self.brand)

class car(models.Model):
    car_manufacturer = models.ForeignKey(manufacturer,on_delete=CASCADE,verbose_name="Manufacturer",blank=True,null=True)
    car_model=models.CharField(max_length=100, verbose_name="Model", blank=True,null=True)           #Ejemplo: 100 C1 Coupe (817)
    carfrom=models.IntegerField(verbose_name="From", blank=True,null=True)      #Ejemplo: 11/2015
    carto=models.IntegerField(verbose_name="To", blank=True,null=True)          #Ejemplo: 11/2018
    transmission=models.ManyToManyField(transmission, verbose_name="Transmision", blank=True,null=True)        #Ejemplo: ATM, MTM (Automatic, Manual)
    chasis=models.CharField(max_length=50, verbose_name="Chasis", blank=True,null=True)        #Ejemplo: ATM, MTM (Automatic, Manual)

    def __str__(self):
        return '%s %s %s %s' %(self.car_manufacturer, self.car_model, self.carfrom, self.chasis)

class engine(models.Model):
    car_engine_info=models.ManyToManyField(car,blank=True,null=True)
    engine_manufacturer = models.ForeignKey(manufacturer,on_delete=CASCADE,verbose_name="Manufacturer",blank=True,null=True)
    engine_l=models.CharField(max_length=10, verbose_name="Litre",blank=True,null=True)             #Ejemplo: 1.8 D
    engine_ide=models.CharField(max_length=80, verbose_name="Code",blank=True,null=True)          #Ejemplo: 1GRFE
    engine_type=models.CharField(max_length=15, verbose_name="Type",blank=True,null=True)         #Ejemplo: Diesel, Petrol
    engine_cylinder=models.IntegerField(verbose_name="Valve",blank=True,null=True)               #Ejemplo: 1588 ccm
    engine_pistons=models.IntegerField(verbose_name="Pistons",blank=True,null=True)                #Ejemplo: 4 pistons
    engine_power_kw=models.IntegerField(verbose_name="Power (kW)",blank=True,null=True)               #Ejemplo: 63 kw
    engine_power_hp=models.IntegerField(verbose_name="Power (hp)",blank=True,null=True)               #Ejemplo: 85 hp

    def __str__(self):
        return '%s %s' %(self.engine_ide, self.engine_l)
    

class category(models.Model):
    category=models.CharField(max_length=40, verbose_name="Category",blank=True,null=True)     #Ejemplo: Filter

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return '%s' %(self.category)

class subcategory(models.Model):

    category = models.ForeignKey(category,on_delete=CASCADE,verbose_name="Category",blank=True,null=True)
    subcategory=models.CharField(max_length=40, verbose_name="Sub Category",blank=True,null=True)     #Ejemplo: Filter

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return '%s' %(self.subcategory)

class spare(models.Model):
    spare_code=models.CharField(max_length=40, verbose_name="Code", unique=True,blank=True,null=True)          #Ejemplo: 50013073
    spare_brand=models.ManyToManyField(branddb,blank=True,null=True)         #Ejemplo: KOLBENSCMIDT
    spare_name=models.CharField(max_length=400, verbose_name="Description",blank=True,null=True)          #Ejemplo: Oil filter
    car_info=models.ManyToManyField(car,blank=True,null=True)
    engine_info=models.ManyToManyField(engine,blank=True,null=True)
    # ChainedManyToManyField(
    #     engine,
    #     chained_field="car_info",
    #     chained_model_field="car_engine_info",blank=True,null=True)
    spare_category = models.ForeignKey(category,on_delete=CASCADE,verbose_name="Category",blank=True,null=True)
    spare_subcategory = models.ForeignKey(subcategory,on_delete=CASCADE,verbose_name="Sub Category",blank=True,null=True)
    spare_vendor = models.ManyToManyField(vendor,verbose_name="Vendor",blank=True,null=True)
    # spare_reference=models.ManyToManyField(reference,verbose_name="Reference code",blank=True,null=True)
    spare_photo=models.ImageField(upload_to="spares", verbose_name="Photo",blank=True,null=True)                           #Será ImageField()
    shape=models.CharField(max_length=20, verbose_name="Shape",blank=True,null=True)             #Ejemplo: Rectangular
    # filter_horizontal=("car_info",)
    price_m=models.FloatField(verbose_name="Price M",blank=True,null=True)
    price_d=models.FloatField(verbose_name="Price D",blank=True,null=True)
    spare_spare = models.ManyToManyField("self",verbose_name="Spare target",blank=True,null=True)
    note = models.TextField(max_length=400, verbose_name="VIN",blank=True,null=True)

    def __str__(self):
        return '%s %s' %(self.spare_code, self.spare_name)
    
class vendorSpare(models.Model):

    spare = models.ForeignKey(spare,on_delete=CASCADE,blank=True,null=True,verbose_name="Spare")
    vendor = models.ForeignKey(vendor,on_delete=CASCADE,blank=True,null=True,verbose_name="Spare")
    brand = models.ForeignKey(branddb,on_delete=CASCADE,blank=True,null=True,verbose_name="Brand")
    brandPrice=models.FloatField(verbose_name="Price", blank=True,null=True)
    cantidad = models.IntegerField(verbose_name="Quantity", blank=True,null=True)

    def __str__(self):
        return '%s %s' %(self.spare, self.vendor)

class dimension(models.Model):
    
    dimensionSpare = models.ForeignKey(spare,on_delete=CASCADE,blank=True,null=True,verbose_name="Spare")
    atributeName=models.CharField(max_length=20, verbose_name="Name", blank=True,null=True)
    atributeVal=models.FloatField(verbose_name="Atribute (mm)",blank=True,null=True)

    def __str__(self):
        return '%s %s' %(self.atributeName, self.atributeVal)

class atribute(models.Model):
    
    atributeSpare = models.ForeignKey(spare,on_delete=CASCADE,blank=True,null=True,verbose_name="Spare")
    atributeName=models.CharField(max_length=20, verbose_name="Name", blank=True,null=True)
    atributeVal=models.CharField(max_length=50, verbose_name="Atribute",blank=True,null=True)

    def __str__(self):
        return '%s %s' %(self.atributeName, self.atributeVal)

class reference(models.Model):

    referenceSpare = models.ForeignKey(spare,on_delete=CASCADE,blank=True,null=True,verbose_name="Spare")
    referenceCode = models.CharField(max_length=20, verbose_name="Code", blank=True,null=True)
    referenceNote = models.CharField(max_length=40, verbose_name="Note", blank=True,null=True)
    cantidad = models.IntegerField(verbose_name="Quantity", blank=True,null=True)

    def __str__(self):
        return '%s - %s' %(self.referenceSpare, self.referenceCode)
    
class spareCart(models.Model):

    spareId=models.CharField(max_length=20, verbose_name="Id", blank=True,null=True)          #Ejemplo: 50013073
    spareCode=models.CharField(max_length=20, verbose_name="Code", blank=True,null=True)          #Ejemplo: 50013073
    nameUser=models.CharField(max_length=20, verbose_name="User", blank=True,null=True)          #Ejemplo: 50013073

    def __str__(self):
            return '%s %s %s' %(self.spareId, self.spareCode, self.nameUser)

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=CASCADE)
    ventas = models.BooleanField(default=False)
    bodega = models.BooleanField(default=False)
    mayorista = models.BooleanField(default=False)
    detal = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

# Contabilidad --------------------------------------------------------------------

class persona(models.Model):

    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    documento = models.CharField(max_length=50, verbose_name="Documento",default="",blank=True,null=True)
    ingreso = models.BooleanField(default=False,verbose_name="Ingreso",blank=True,null=True)
    gasto = models.BooleanField(default=False,verbose_name="Gasto",blank=True,null=True)

    def __str__(self):
        return str(self.nombre)

class factType(models.Model):

    nombre = models.CharField(max_length=40, verbose_name="Tipo",default='Tipo')
    include = models.BooleanField(default=True,verbose_name="Include")
    manual = models.BooleanField(default=False,verbose_name="Manual")
    mercPagada = models.BooleanField(default=False,verbose_name="Mercancia pagada")
    mercPagar = models.BooleanField(default=False,verbose_name="Mercancia pagar")
    facCobrar = models.BooleanField(default=False,verbose_name="Factura cobrar")
    facCobrada = models.BooleanField(default=False,verbose_name="Factura cobrada")
    visa = models.BooleanField(default=False,verbose_name="Tarjeta visa")
    clave = models.BooleanField(default=False,verbose_name="Tarjeta clave")
    ingreso = models.BooleanField(default=False,verbose_name="Ingreso")
    gasto = models.BooleanField(default=False,verbose_name="Gasto")
    # models.ForeignKey(spare,on_delete=CASCADE,blank=True,null=True,verbose_name="Spare")
    def __str__(self):
        return str(self.nombre)

class factCategory(models.Model):

    nombre = models.CharField(max_length=40, verbose_name="Categoría",blank=True,null=True)
    ingreso = models.BooleanField(default=False,verbose_name="Ingreso")
    egreso = models.BooleanField(default=False,verbose_name="Egreso")
    limite = models.BooleanField(default=False,verbose_name="Fecha imite")

    def __str__(self):
            return '%s' %(self.nombre)

class factura(models.Model):

    num = models.CharField(max_length=20,verbose_name="Número de factura",blank=True,null=True)
    refPersona = models.ForeignKey(persona,on_delete=CASCADE,verbose_name="Persona",default='Persona')
    refType = models.ForeignKey(factType,on_delete=CASCADE,verbose_name="Tipo",default='Tipo')
    refCategory = models.ForeignKey(factCategory,on_delete=CASCADE,verbose_name="Category",default='Categoria')
    fechaCreado = models.DateTimeField(auto_now_add=False,verbose_name="Fecha")
    fechaTope = models.DateField(auto_now=False,auto_now_add=False,verbose_name="Fecha tope",blank=True,null=True)
    fechaCobrado = models.DateField(auto_now=False,auto_now_add=False,verbose_name="Fecha cobrado",blank=True,null=True)
    iva = models.FloatField(verbose_name="Impuesto",blank=True,null=True)
    monto = models.FloatField(verbose_name="Monto")
    total = models.FloatField(verbose_name="Total",default=0)
    pendiente = models.BooleanField(default=False,verbose_name="Pendiente",blank=True,null=True)
    nc = models.BooleanField(default=False,verbose_name="Nota de crédito",blank=True,null=True)
    note = models.TextField(max_length=400, verbose_name="Nota",blank=True,null=True)

    def __str__(self):
        return '%s %s %s' %(self.num, self.refPersona, self.fechaCreado)
    
class mainTable(models.Model):

    fecha = models.DateTimeField(auto_now_add=False,verbose_name="Fecha")
    tabNombre = models.CharField(max_length=80,verbose_name="Nombre de tabla",default='Principal')
    tabTipo = models.ForeignKey(factType,on_delete=CASCADE,verbose_name="Tipo",default='Tipo')
    principal = models.BooleanField(default=False,verbose_name="Principal",blank=True,null=True)
    # tabPagos = models.FloatField(verbose_name="Pagos")
    # tabRetiros = models.FloatField(verbose_name="Retiros")
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.fecha)

class mainTableAux(models.Model):

    tabTipo = models.ForeignKey(factType,on_delete=CASCADE,verbose_name="Tipo",default='Tipo')
    # tabPagos = models.FloatField(verbose_name="Pagos")
    # tabRetiros = models.FloatField(verbose_name="Retiros")
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.tabTotal)

class customTable(models.Model):

    fecha = models.DateTimeField(auto_now_add=False,verbose_name="Fecha",default=now)
    tabNombre = models.CharField(max_length=80,verbose_name="Nombre de tabla",default='Principal')
    tabTipo = models.ForeignKey(factType,on_delete=CASCADE,verbose_name="Tipo",default='Tipo')
    principal = models.BooleanField(default=False,verbose_name="Principal",blank=True,null=True)
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.tabNombre)

class customAux(models.Model):

    tabNombre = models.CharField(max_length=80,verbose_name="Nombre de tabla",default='Principal')
    tabTipo = models.ForeignKey(factType,on_delete=CASCADE,verbose_name="Tipo",default='Tipo')
    principal = models.BooleanField(default=False,verbose_name="Principal",blank=True,null=True)
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.tabNombre)

class tableOperacion(models.Model):

    fecha = models.DateTimeField(auto_now_add=False,verbose_name="Fecha",default=now)
    tabNombre = models.CharField(max_length=80,verbose_name="Nombre de tabla",default='Principal')
    tabTipo = models.ForeignKey(factType,on_delete=CASCADE,verbose_name="Tipo",default='Tipo')
    principal = models.BooleanField(default=False,verbose_name="Principal",blank=True,null=True)
    suma = models.BooleanField(default=True,verbose_name="Suma")
    resta = models.BooleanField(default=False,verbose_name="Resta")
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.tabNombre)

class tableOperacionAux(models.Model):

    tabNombre = models.CharField(max_length=80,verbose_name="Nombre de tabla",default='Principal')
    tabTipo = models.ForeignKey(factType,on_delete=CASCADE,verbose_name="Tipo",default='Tipo')
    principal = models.BooleanField(default=False,verbose_name="Principal",blank=True,null=True)
    suma = models.BooleanField(default=True,verbose_name="Suma")
    resta = models.BooleanField(default=False,verbose_name="Resta")
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.tabNombre)

class tableOperacionCat(models.Model):

    fecha = models.DateTimeField(auto_now_add=False,verbose_name="Fecha",default=now)
    tabNombre = models.CharField(max_length=80,verbose_name="Nombre de tabla",default='Principal')
    tabCat = models.ForeignKey(factCategory,on_delete=CASCADE,verbose_name="Categoria",default='Categoria')
    principal = models.BooleanField(default=False,verbose_name="Principal",blank=True,null=True)
    suma = models.BooleanField(default=True,verbose_name="Suma")
    resta = models.BooleanField(default=False,verbose_name="Resta")
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.tabNombre)

class tableOperacionAuxCat(models.Model):

    tabNombre = models.CharField(max_length=80,verbose_name="Nombre de tabla",default='Principal')
    tabCat = models.ForeignKey(factCategory,on_delete=CASCADE,verbose_name="Categoria",default='Categoria')
    principal = models.BooleanField(default=False,verbose_name="Principal",blank=True,null=True)
    suma = models.BooleanField(default=True,verbose_name="Suma")
    resta = models.BooleanField(default=False,verbose_name="Resta")
    tabTotal = models.FloatField(verbose_name="Total")

    def __str__(self):
        return '%s' %(self.tabNombre)
    
class shopCart(models.Model):

    product = models.ForeignKey(vendorSpare,on_delete=CASCADE,blank=True,null=True,verbose_name="Product")
    quantity = models.FloatField(verbose_name="Quantity", blank=True,null=True)
    SubTotal = models.FloatField(verbose_name="SubTotal", blank=True,null=True)
    Total = models.FloatField(verbose_name="Total", blank=True,null=True)

    def __str__(self):
        return '%s' %(self.Total)