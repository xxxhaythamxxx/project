from django.db import models
from django.db.models.deletion import CASCADE
from smart_selects.db_fields import ChainedManyToManyField

# Create your models here.
class car(models.Model):
    car_manufacturer=models.CharField(max_length=20, verbose_name="Manufacturer", blank=True,null=True)    #Ejemplo: Audi
    car_model=models.CharField(max_length=100, verbose_name="Model", unique=True, blank=True,null=True)           #Ejemplo: 100 C1 Coupe (817)
    car_from=models.DateField(verbose_name="From", blank=True,null=True)      #Ejemplo: 11/2015
    car_to=models.DateField(verbose_name="To", blank=True,null=True)          #Ejemplo: 11/2018
    transmission=models.CharField(max_length=10, blank=True,null=True)        #Ejemplo: ATM, MTM (Automatic, Manual)

    def __str__(self):
        return '%s %s, (%s / %s)' %(self.car_manufacturer, self.car_model, self.car_from.year, self.car_to.year)

class engine(models.Model):
    car_engine_info=models.ManyToManyField(car,blank=True,null=True)
    engine_l=models.CharField(max_length=10, verbose_name="Litre",blank=True,null=True)             #Ejemplo: 1.8 D
    engine_ide=models.CharField(max_length=80, verbose_name="Code",blank=True,null=True)          #Ejemplo: 1GRFE
    engine_type=models.CharField(max_length=15, verbose_name="Type",blank=True,null=True)         #Ejemplo: Diesel, Petrol
    engine_cylinder=models.IntegerField(verbose_name="Cylinder (ccm)",blank=True,null=True)               #Ejemplo: 1588 ccm
    engine_pistons=models.IntegerField(verbose_name="Pistons",blank=True,null=True)                #Ejemplo: 4 pistons
    engine_power_kw=models.IntegerField(verbose_name="Power (kW)",blank=True,null=True)               #Ejemplo: 63 kw
    engine_power_hp=models.IntegerField(verbose_name="Power (hp)",blank=True,null=True)               #Ejemplo: 85 hp

    def __str__(self):
        return '%s %s %s %s ccm/%s pistons %s kW/%s hp' %(self.engine_ide, self.engine_l, self.engine_type, self.engine_cylinder, self.engine_pistons, self.engine_power_kw, self.engine_power_hp)
    

class category(models.Model):
    category=models.CharField(max_length=40, verbose_name="Category",blank=True,null=True)     #Ejemplo: Filter

    def __str__(self):
        return '%s' %(self.category)

class reference(models.Model):
    reference_code=models.CharField(max_length=80, verbose_name="Code",blank=True,null=True)     #Ejemplo: 45646546ad
    reference_car = models.ForeignKey(car,on_delete=CASCADE,blank=True,null=True)               

    def __str__(self):
        return '%s - %s' %(self.reference_code, self.reference_car)

class spare(models.Model):
    car_info=models.ManyToManyField(car,blank=True,null=True)
    engine_info=ChainedManyToManyField(
        engine,
        chained_field="car_info",
        chained_model_field="car_engine_info",blank=True,null=True)
    spare_category = models.ForeignKey(category,on_delete=CASCADE,blank=True,null=True)
    spare_spare = models.ManyToManyField("self",verbose_name="Spare target",blank=True,null=True)
    spare_reference=models.ManyToManyField(reference,verbose_name="Reference code",blank=True,null=True)
    spare_photo=models.ImageField(upload_to="spares", verbose_name="Photo",blank=True,null=True)                           #Será ImageField()
    spare_code=models.CharField(max_length=15, verbose_name="Code", unique=True,blank=True,null=True)          #Ejemplo: 50013073
    spare_brand=models.CharField(max_length=20, verbose_name="Brand",blank=True,null=True)         #Ejemplo: KOLBENSCMIDT
    spare_name=models.CharField(max_length=80, verbose_name="Name",blank=True,null=True)          #Ejemplo: Oil filter
    shape=models.CharField(max_length=20, verbose_name="Shape",blank=True,null=True)             #Ejemplo: Rectangular
    long=models.FloatField(verbose_name="Long",blank=True,null=True)
    wide=models.FloatField(verbose_name="Wide",blank=True,null=True)
    high=models.FloatField(verbose_name="High",blank=True,null=True)
    diameter=models.FloatField(verbose_name="Diameter",blank=True,null=True)
    radio=models.FloatField(verbose_name="Radio",blank=True,null=True)

    def __str__(self):
        return '%s %s %s' %(self.spare_code, self.spare_brand, self.spare_name)
