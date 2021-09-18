from typing import List
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse, HttpResponseRedirect
from .models import *
from django.views import View
from .cart import *
import json
from openpyxl import load_workbook, workbook
from openpyxl.utils import get_column_letter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from random import seed
from random import random
import random
import datetime
from datetime import date
from datetime import datetime, timezone
from django.contrib.auth.models import User, Permission
# import numpy as np

# Create your views here.

# Creo el diccionario para los formularios en común de todos los templates
# def same():
#     # Consigo todos los valores de nombre de las dimensiones
#     dim=dimension.objects.values("atributeName").distinct()
#     # Consigo todos los valores de las dimensiones
#     dim2=dimension.objects.all()

#     # Consigo todos los valores de nombre de las atribute
#     atr=atribute.objects.values("atributeName").distinct()
#     # Consigo todos los valores de las atribute
#     atr2=atribute.objects.all()
    
#     # Consigo TODOS los spares
#     allSparesall=spare.objects.all()
#     # Consigo TODAS las categorias
#     allCategories=category.objects.all()
#     # Consigo TODOS los motores
#     allEngines=engine.objects.all()
#     # Conseguir TODOS los carros por fabricante
#     onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
#     # Conseguir TODOS los carros
#     allCars=car.objects.all()
#     # Conseguir TODOS los repuestos por nombre
#     allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
#     dicc={"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}
#     return dicc

# dic=same().copy()

# Código para saber si usa el input o el filtro
def selectf(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all().order_by("spare_name","spare_code")
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}


    if request.method=="POST":
        list = request.POST.getlist('toAdd')
        delist = request.POST.getlist("toDel")
        if delist:
            carrito = Cart(request)
            for a in delist:                
                spare_part = get_object_or_404(spare, id = a)
                carrito.remove(spare_part)
        if list:
            carrito = Cart(request)
            for a in list:                
                spare_part = get_object_or_404(spare, id = a)
                carrito.add(spare_part)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method=="GET":
        search=request.GET.get("engine_id")
        # Si usaron el filter
        if search:
            # Valor del modelo del motor
            engModel=request.GET.get("engine_id")  
            # Valor del carro enviado     
            carManu=request.GET.get("car_id")    
            #Valor del modelo del carro enviado       
            carModel=request.GET.get("car_model_id")    
            comp=spare.objects.filter(engine_info__engine_ide__icontains=engModel,car_info__car_manufacturer__icontains=carManu,car_info__car_model__icontains=carModel).order_by("id")  # Creo un Query de spare que tenga el valor del motor pasado
            engcomp=engine.objects.filter(engine_ide__icontains=engModel,car_engine_info__car_manufacturer__icontains=carManu)
            dic.update({"carManu":carManu,"carModel":carModel,"spare":comp,"mig":engModel,"engcomp":engcomp})
            return render(request,"spareapp/findfil.html",dic)
        # Si se usa el buscador por código de repuesto
        else:   
            valor=request.GET.get("search")
            bol = False
            if valor:
                if valor=="":
                    return render(request,"spareapp/home.html",dic)
                else:
                    # Compara el codigoRepuesto con valor
                    b=[]
                    vec = valor.split(" ")
                    # comp=spare.objects.filter(spare_code__icontains=vec).order_by("spare_code","spare_brand","spare_name").distinct() 
                    todos=spare.objects.all()
                    ref=reference.objects.all()
                    cars=car.objects.all()
                    engines=engine.objects.all()
                    contVar = 0
                    for t in todos:
                        s=t.spare_code
                        # br=t.spare_brand
                        n=t.spare_name
                        ch=t.car_info
                        for v in vec:
                            if s:
                                out = s.translate(str.maketrans('', '', '.''-'))
                                if valor.upper() in out.upper():
                                    bol = True
                                if v.upper() in out.upper():
                                    bol = True
                                if v.upper() in s.upper():
                                    bol = True
                            if n:
                                out = n.split(" ")
                                for o in out:
                                    if o.upper().startswith(v.upper()):
                                        bol = True
                            for r in ref:
                                sr=r.referenceCode
                                if sr:
                                    out = sr.translate(str.maketrans('', '', '.''-'))
                                    if valor.upper() in out.upper():
                                        if s == r.referenceSpare.spare_code:
                                            bol = True
                                    if v.upper() in out.upper():
                                        if s == r.referenceSpare.spare_code:
                                            bol = True
                            for r in cars:
                                sr=r.transmission
                                man=r.car_manufacturer
                                if sr:
                                    out = sr.translate(str.maketrans('', '', '.''-'))
                                    if valor.upper() in out.upper():
                                        for to in t.car_info.all():
                                            if to.transmission in r.transmission:
                                                bol = True
                                    if v.upper() in out.upper():
                                        for to in t.car_info.all():
                                            if to.transmission in r.transmission:
                                                bol = True
                                if man:
                                    out = man.translate(str.maketrans('', '', '.''-'))
                                    if out.upper().startswith(valor.upper()):
                                        for to in t.car_info.all():
                                            if to.car_manufacturer in r.car_manufacturer:
                                                bol = True
                                    if out.upper().startswith(v.upper()):
                                        for to in t.car_info.all():
                                            if to.car_manufacturer in r.car_manufacturer:
                                                bol = True
                            
                            if bol == True:
                                contVar=contVar+1
                            bol = False
                            
                            # -----------------------------------------------------

                            for r in engines:
                                # transmission
                                sr=r.engine_ide
                                # car_manufacturer
                                # man=r.car_manufacturer
                                if sr:
                                    out = sr.translate(str.maketrans('', '', '.''-'))
                                    if valor.upper() in out.upper():
                                        for to in t.engine_info.all():
                                            if to.engine_ide in r.engine_ide:
                                                bol = True
                                    if v.upper() in out.upper():
                                        for to in t.engine_info.all():
                                            if to.engine_ide in r.engine_ide:
                                                bol = True
                                # if man:
                                #     out = man.translate(str.maketrans('', '', '.''-'))
                                #     if out.upper().startswith(valor.upper()):
                                #         for to in t.car_info.all():
                                #             if to.car_manufacturer in r.car_manufacturer:
                                #                 bol = True
                                #     if out.upper().startswith(v.upper()):
                                #         for to in t.car_info.all():
                                #             if to.car_manufacturer in r.car_manufacturer:
                                #                 bol = True
                            
                            if bol == True:
                                contVar=contVar+1
                            bol = False

                            # --------------------------------------------------------------
                        
                        if contVar == len(vec):
                            b.append(t)
                        contVar = 0
                            
                    b = (set(b))
                    dic.update({"spare":b,"mig":valor,"parameter":"Parameters"})
                    return render(request,"spareapp/find.html",dic)
            else:
                return False


def home(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    # spCart=spareCart.objects.values("spareId","nameUser").distinct()
    
    spCart = spareCart.objects.filter(nameUser=request.user.get_username()).values("spareId","nameUser").distinct().order_by("spareId")
    if request.user.get_username() == "":
        spCart = spareCart.objects.filter(nameUser="AnonymousUser").values("spareId","nameUser").distinct()
    dic={"spCart":spCart,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}


    if request.method=="POST":
        list = request.POST.getlist('toAdd')
        delist = request.POST.getlist("toDel")
        # print("list")
        # print(list)
        # print("delist")
        # print(delist)
        # Si es una lista que se envía para guardarla
        if list:
            # print("List")
            # print(list)
            # cart = spareCart()
            # Si se va a crear un nuevo carrito
            if request.POST.get("cartNumber") == "":
                randomNum = datetime.now().strftime("%Y%m%d%H%M%S")
                # print("Fecha actual")
                # print(datetime.now().strftime("%Y%m%d%H%M%S"))
                # cart = spareCart()
                # cart.save()
                # form = UserRegisterForm(request.POST)
                print("Voy a entrar a list")
                for a in list:
                    cart = spareCart()
                    print("Random: "+str(randomNum))
                    cart.spareId = randomNum
                    # cart1 = spareCart.objects.get(id=cart.id)
                    print("Imprimo cart1")
                    # print(cart)
                    cart.spareCode = a
                    print("Voy a guardar add a")
                    # cart1.spareCode.add(a)
                    print("Codigo: "+str(a))
                    # Si hay iniciada una sesion
                    if request.user.get_username() != "":
                        username = request.user.get_username()
                        cart.nameUser = username
                        # cart1.nameUser.add(username)
                    # Si no hay iniciada una sesion
                    else:
                        cart.nameUser = "AnonymousUser"
                        # cart1.nameUser.add("User")
                    print("Guarda")
                    cart.save()
                    # cart1.add(cart1)
            else:
                print("Envía a un carrito especifico")
                for a in list:
                    cart = spareCart()
                    if request.user.get_username() == "":
                        cartPrueba=spareCart.objects.filter(spareId=request.POST.get("cartNumber"),spareCode=a,nameUser="AnonymousUser")
                    else:
                        cartPrueba=spareCart.objects.filter(spareId=request.POST.get("cartNumber"),spareCode=a,nameUser=request.user.get_username())
                    if cartPrueba:
                        print("Ya existe")
                    else:
                        cart.spareId = request.POST.get("cartNumber")
                        cart.spareCode = a
                        # Si hay iniciada una sesion
                        if request.user.get_username() != "":
                            username = request.user.get_username()
                            cart.nameUser = username
                        # Si no hay iniciada una sesion
                        else:
                            cart.nameUser = "AnonymousUser"
                        cart.save()
        

        # # Carrito antes
        # if delist:
        #     carrito = Cart(request)
        #     for a in delist:                
        #         spare_part = get_object_or_404(spare, id = a)
        #         carrito.remove(spare_part)
        # if list:
        #     carrito = Cart(request)
        #     for a in list:                
        #         spare_part = get_object_or_404(spare, id = a)
        #         carrito.add(spare_part)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method=="GET":

        if selectf(request)==False:
            # alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            # from typing import List
            # alls = list(spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct())
            alls = [x for x in spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct()]
            # print(alls)
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            return selectf(request)

def find(request):
    return render(request,"spareapp/find.html")

def sparedetails(request,val,val2):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()
    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}


    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            pr1=spare.objects.filter(spare_code=val).order_by("spare_name","spare_code","spare_brand")
            ar=spare.objects.values("spare_code","car_info__car_manufacturer").filter(spare_code=val).distinct()
            spareaux = val2
            valor=spareaux.lstrip("<QuerySet [spare:")

            valor2=valor.rstrip("]>")
            characters = "<>"
            valor = ''.join( x for x in valor2 if x not in characters)

            line= valor.replace(" spare: ", "")
            line= line.replace("{spare: ", "")
            line=line.rstrip("}")
            
            valAux = 0
            vector=line.split(",")
            i=0
            for v in vector:
                if val == v.split(" ")[0]:
                    valAux=(i)
                i=i+1

            i=0
            for v in vector:
                if i == valAux:
                    codeAux=v.split(" ")[0]
                i=i+1
            pr=spare.objects.filter(spare_code=codeAux).order_by("spare_name","spare_code","spare_brand")
            # print("-------------------------------------")
            # print(codeAux)
            dbTotal = len(vector)
            dbActual = valAux+1
            dic.update({"spare1":pr1,"vector":vector,"dbTotal":dbTotal,"dbActual":dbActual,"spareAux":spareaux,"spare":pr,"spareReference":ar})
            return render(request,"spareapp/sparedetails.html",dic)
    else:
        return selectf(request)
    

def brand(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            # pr=spare.objects.values("id","spare_photo","spare_code","spare_brand","spare_name","car_info__car_manufacturer").filter(spare_brand__icontains=val).distinct()
            pr=spare.objects.filter(spare_brand__icontains=val).order_by("spare_name","spare_code","spare_brand").distinct()
            dic.update({"spare":pr,"mig":val,"parameter":"Spare brand"})
            return render(request,"spareapp/find.html",dic)
    else:
        return selectf(request)

def name(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            # pr=spare.objects.values("id","spare_photo","spare_code","spare_brand","spare_name","car_info__car_manufacturer").filter(spare_name__icontains=val).distinct()
            pr=spare.objects.filter(spare_name__icontains=val).order_by("spare_name","spare_code","spare_brand").distinct()
            dic.update({"spare":pr,"mig":val,"parameter":"Description"})
            return render(request,"spareapp/find.html",dic)
    else:
        return selectf(request)

def trunc(val):
    allen = car.objects.filter(car_manufacturer__icontains=val).values("car_model").order_by("car_model")
    b=[]
    for a in allen:
        a = a["car_model"].split(" ")[0]
        b.append(a+" .")
    b = list(set(b)) 
    return b

def manuf(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            tr = trunc(val)
            pr=car.objects.filter(car_manufacturer__icontains=val)
            dic.update({"car":pr,"mig":val,"tr":tr})
            return render(request,"spareapp/manuf.html",dic)
    else:
        return selectf(request)

def allmodel(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            rep = spare.objects.filter(car_info__car_model__icontains=val).order_by("spare_name","spare_code","spare_brand").distinct()
            dic.update({"spare":rep,"mig":val,"parameter":"Car model"})
            return render(request,"spareapp/find.html",dic)
    else:
        return selectf(request)

def allmanu(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    
    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            rep = spare.objects.filter(car_info__car_manufacturer__icontains=val).order_by("spare_name","spare_code","spare_brand").distinct()
            dic.update({"spare":rep,"mig":val,"parameter":"Car manufacturer"})
            return render(request,"spareapp/find.html",dic)
    else:
        return selectf(request)

def model(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            pr=engine.objects.filter(car_engine_info__car_model__icontains=val)
            dic.update({"engine":pr,"mig":val,"parameter":"Car model"})
            return render(request,"spareapp/model.html",dic)
    else:
        return selectf(request)

def enginel(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            pr=spare.objects.filter(engine_info__engine_ide__icontains=val).order_by("spare_name","spare_code","spare_brand")
            dic.update({"spare":pr,"parameter":"Engine code","mig":val})
            return render(request,"spareapp/find.html",dic)
    else:
        return selectf(request)

def detail(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}


    if selectf(request)==False:
        spares = spare.objects.all().order_by("spare_name","spare_code","spare_brand")
        carrito = Cart(request)
        dic.update({'carrito': carrito,'spare':spares})
        return render(request, 'spareapp/detail.html', dic)
    else:
        return selectf(request)

def shape(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            spares = spare.objects.all().filter(shape__icontains=val).order_by("spare_name","spare_code","spare_brand")
            dic.update({'spare':spares,'parameter':'Shape','mig':val})
            return render(request, 'spareapp/find.html',dic)
    else:
        return selectf(request)

def longi(request,val1,val2):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        spares = spare.objects.all().filter(
            dimension__atributeName__icontains=val1,
            dimension__atributeVal=val2).order_by("spare_name","spare_code")
        dic.update({'spare':spares,'parameter':val1,'mig':val2})
        return render(request, 'spareapp/find.html',dic)
    else:
        return selectf(request)

def atributes(request,val1,val2):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        spares = spare.objects.all().filter(
            atribute__atributeName__icontains=val1,
            atribute__atributeVal=val2).order_by("spare_name","spare_code")
        dic.update({'spare':spares,'parameter':val1,'mig':val2})
        return render(request, 'spareapp/find.html',dic)
    else:
        return selectf(request)

def carBrands(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        return render(request,"spareapp/carBrands.html",dic)
    else:
        return selectf(request)

def categoryi(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            # pr=spare.objects.filter(spare_category__category__icontains=val).order_by("spare_name","spare_code","spare_brand").distinct()
            pr=spare.objects.filter(spare_category__category__icontains=val).order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":pr,"mig":val,"parameter":"Category"})
            return render(request,"spareapp/find.html",dic)
    else:
        return selectf(request)

def chasis(request, val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    dic={"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            pr=spare.objects.filter(car_info__transmission__icontains=val).order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":pr,"mig":val,"parameter":"Chasis"})
            return render(request,"spareapp/find.html",dic)
    else:
        return selectf(request)

def prev(request,val,val2):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()
    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}


    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            ar=spare.objects.values("spare_code","car_info__car_manufacturer").filter(spare_code=val).distinct()
            spareaux = spare.objects.none()
            spareaux = val2
            valor=spareaux.lstrip("<QuerySet [spare:")

            valor2=valor.rstrip("]>")
            characters = "<>"
            valor = ''.join( x for x in valor2 if x not in characters)

            line= valor.replace(" spare: ", "")
            line= line.replace("{spare: ", "")
            line=line.rstrip("}")
            
            
            vector=line.split(",")
            i=0
            valAux = 0
            
            for v in vector:
                if val == v.split(" ")[0]:
                    if i>0:
                        valAux=(i-1)
                    else:
                        valAux=0
                i=i+1

            i=0
            for v in vector:
                if i == valAux:
                    codeAux=v.split(" ")[0]
                i=i+1
            
            pr=spare.objects.filter(spare_code=codeAux).order_by("spare_name","spare_code","spare_brand")
            dbTotal = len(vector)
            dbActual = valAux+1
            dic.update({"dbTotal":dbTotal,"dbActual":dbActual,"spareAux":spareaux,"spare":pr,"spareReference":ar})
            return render(request,"spareapp/sparedetails.html",dic)
    else:
        return selectf(request)

def next(request,val,val2):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()
    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}


    if selectf(request)==False:
        valsearch=request.GET.get("search")
        if valsearch=="":
            alls = spare.objects.all().order_by("spare_name","spare_code","spare_brand").distinct() 
            dic.update({"spare":alls})
            return render(request,"spareapp/home.html",dic)
        else:
            ar=spare.objects.values("spare_code","car_info__car_manufacturer").filter(spare_code=val).distinct()

            spareaux = spare.objects.none()
            spareaux = val2
            valor=spareaux.lstrip("<QuerySet [spare:")

            valor2=valor.rstrip("]>")
            characters = "<>"
            valor = ''.join( x for x in valor2 if x not in characters)

            line= valor.replace(" spare: ", "")
            line= line.replace("{spare: ", "")
            line=line.rstrip("}")
            
            
            vector=line.split(",")

            i=0
            valAux = 0

            for v in vector:
                if val == v.split(" ")[0]:
                    if i<(len(vector)-1):
                        valAux=(i+1)
                    else:
                        valAux=(len(vector)-1)
                i=i+1

            i=0
            for v in vector:
                if i == valAux:
                    codeAux=v.split(" ")[0]
                i=i+1
            
            pr=spare.objects.filter(spare_code=codeAux).order_by("spare_name","spare_code","spare_brand")
            dbTotal = len(vector)
            dbActual = valAux+1
            dic.update({"dbTotal":dbTotal,"dbActual":dbActual,"spareAux":spareaux,"spare":pr,"spareReference":ar})
            return render(request,"spareapp/sparedetails.html",dic)
    else:
        return selectf(request)

# def getCar(request):
#     id = request.GET.get('id', '')
#     print(id+"---------------------------------------------------------------------")
#     result = list(car.objects.filter(
#     spare_id=int(id)).values('id', 'car_manufacturer'))
#     return HttpResponse(json.dumps(result), content_type="application/json")

def filldb(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()
    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/filldb.html",dic)

def fillcar(request):

    print("Entra a fillcar")
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()
    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if request.method == "POST":
        print("Entra a post de fillcar")
        car1 = car()
        car1.car_manufacturer = request.POST.get("manufactur")
        car1.car_model = request.POST.get("mode")
        if request.POST.get("yearfro") == "":
            car1.carfrom = None
        else:
            car1.carfrom = request.POST.get("yearfro")
        if request.POST.get("yeart") == "":
            car1.carto = None
        else:
            car1.carto = request.POST.get("yeart")
        car1.transmission = request.POST.get("chasi")
        car1.save()

        print(request.POST.get("id"))

        if request.POST.get("id") == "secondForm":
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # return render(request,"spareapp/fillengine.html",dic)
        else:
            return render(request,"spareapp/fillcar.html",dic)
        
    else:
        return render(request,"spareapp/fillcar.html",dic)

def editcar(request,val):
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    sparefind=car.objects.filter(id=val)
    car1 = car.objects.get(id=val)

    dic={"val":val,"sparefind":sparefind,"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}
    if request.method == "POST":

        car1.car_manufacturer=request.POST.get("manufactur")
        car1.car_model=request.POST.get("mode")
        if request.POST.get("yearfro") == "":
            car1.carfrom = None
        else:
            car1.carfrom=request.POST.get("yearfro")
        if request.POST.get("yeart") == "":
            car1.carto = None
        else:
            car1.carto=request.POST.get("yeart")
        car1.transmission=request.POST.get("chasi")
        
        car1.save()
        
        return render(request,"spareapp/listcar.html",dic)
    else:
        return render(request,"spareapp/editcar.html",dic)


def fillengine(request):

    print("Entra a fillengine")
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()
    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if request.method == "POST":
        print("Entra en el POST de fillengine")
        engine1 = engine()
        engine1.engine_l = request.POST.get("litresfill")
        engine1.engine_ide = request.POST.get("codefill")
        engine1.engine_type = request.POST.get("typefill")
        if request.POST.get("valvefill")=="":
            pass
        else:
            engine1.engine_cylinder = request.POST.get("valvefill")
        if request.POST.get("pistonsfill")=="":
            pass
        else:
            engine1.engine_pistons = request.POST.get("pistonsfill")
        engine1.save()
        print(request.POST.getlist("engcartoReg"))
        cartoreg = request.POST.getlist("engcartoReg")
        carAux = []
        cartopass = request.POST.getlist("engcartoPass")
        print(cartopass)
        print(request.POST)

        if cartoreg == []:
            for c in allCars:
                bandt = False
                for ca in cartopass:
                    if str(c) == str(ca):
                        bandt = True
                if bandt == False:
                    carAux.append(c)

        if cartoreg == []:
            for sp in carAux:
                for c in allCars:
                    if str(c) == str(sp):
                        idAux = c.id
                targetCar = car.objects.get(id=idAux)
                engine1.car_engine_info.add(targetCar)
        else:
            for sp in cartoreg:
                for c in allCars:
                    if str(c) == str(sp):
                        idAux = c.id
                targetCar = car.objects.get(id=idAux)
                engine1.car_engine_info.add(targetCar)


        # for sp in cartoreg:
        #     for c in allCars:
        #         if str(c) == str(sp):
        #             idAux = c.id
        #     targetCar = car.objects.get(id=idAux)
        #     engine1.car_engine_info.add(targetCar)

        if request.POST.get("id") == "secondForm":
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            # return render(request,"spareapp/fillengine.html",dic)
        else:
            return render(request,"spareapp/fillengine.html",dic)

        # return render(request,"spareapp/fillengine.html",dic)
    else:
        return render(request,"spareapp/fillengine.html",dic)

def editengine(request,val):
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    engine1 = engine.objects.get(engine_ide=val)
    auxCar = car.objects.filter(engine__engine_ide = val)

    sparefind = engine.objects.filter(engine_ide=val)
    dic={"auxCar":auxCar,"sparefind":sparefind,"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if request.method == "POST":
        engine1.engine_l = request.POST.get("litresfill")
        engine1.engine_ide = request.POST.get("codefill")
        engine1.engine_type = request.POST.get("typefill")
        if request.POST.get("valvefill")=="":
            engine1.engine_cylinder = None
        else:
            engine1.engine_cylinder = request.POST.get("valvefill")
        if request.POST.get("pistonsfill")=="":
            engine1.engine_pistons = None
        else:
            engine1.engine_pistons = request.POST.get("pistonsfill")
        engine1.save()


# Car info ----------------------------------------------------

        cartoreg = request.POST.getlist("engcartoReg")
        cartopass = request.POST.getlist("engcartoPass")
        carAux = []

        spAux = engine.objects.filter(engine_ide=val)

        for sp in spAux:
            for a in sp.car_engine_info.all():
                engine1.car_engine_info.remove(a.id)
        
        if cartoreg == []:
            for c in allCars:
                bandt = False
                for ca in cartopass:
                    if str(c) == str(ca):
                        bandt = True
                if bandt == False:
                    carAux.append(c)

        if cartoreg == []:
            for sp in carAux:
                for c in allCars:
                    if str(c) == str(sp):
                        idAux = c.id
                targetCar = car.objects.get(id=idAux)
                engine1.car_engine_info.add(targetCar)
        else:
            for sp in cartoreg:
                for c in allCars:
                    if str(c) == str(sp):
                        idAux = c.id
                targetCar = car.objects.get(id=idAux)
                engine1.car_engine_info.add(targetCar)

        return render(request,"spareapp/listengine.html",dic)
    else:
        return render(request,"spareapp/editengine.html",dic)

def fillspare(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    spare1 = spare()
    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if request.method == "POST":
        print("POST")
# Spare ------------------------------------------------------
        spareAux = spare.objects.filter(spare_code=request.POST.get("cod"))
        if spareAux:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            pass
        sparrr = request.POST.getlist("toReg")
        spare1.spare_code = request.POST.get("cod")
        spare1.spare_name = request.POST.get("descriptio")

        if "phot" in request.FILES:
            spare1.spare_photo = request.FILES['phot']
        else:
            pass

        if request.POST.get("pricem")=="":
            pass
        else:
            spare1.price_m = request.POST.get("pricem")

        if request.POST.get("priced")=="":
            pass
        else:
            spare1.price_d = request.POST.get("priced")

        if request.POST.get("catSelect") == "":
            pass
        else:
            print("catSelect")
            print(request.POST.get("catSelect"))
            category1 = category.objects.get(category=request.POST.get("catSelect"))
            spare1.spare_category = category1    

        spare1.save()

# Car info ----------------------------------------------------

        
        cartoreg = request.POST.getlist("cartoReg")
        for sp in cartoreg:
            for c in allCars:
                if str(c) == str(sp):
                    # print(c.id)
                    idAux = c.id
            targetCar = car.objects.get(id=idAux)
            spare1.car_info.add(targetCar)

# Engine info ----------------------------------------------------
        
        enginetoreg = request.POST.getlist("enginetoReg")
        for sp in enginetoreg:
            for c in allEngines:
                if str(c) == str(sp):
                    idAux = c.id
            targetCar = engine.objects.get(id=idAux)
            spare1.engine_info.add(targetCar)

# Vendor -----------------------------------------------

        vendortoReg = request.POST.getlist("vendortoReg")
        for sp in vendortoReg:
            for c in allVendors:
                if str(c) == str(sp):
                    idAux = c.id
            targetVendor = vendor.objects.get(id=idAux)
            spare1.spare_vendor.add(targetVendor)

# Spare targets -----------------------------------------------
        for sp in sparrr:
            varId = 0
            aux = sp.split(" ")
            code = (aux[0])

            auxSp = spare.objects.filter(spare_code=code)
            for sp in auxSp:
                varId = sp.id
            targetCode = spare.objects.get(id=varId)
            spare1.spare_spare.add(targetCode)
        
# Reference ------------------------------------------------------
        codesList = request.POST.getlist("refcodes")
        notesList = request.POST.getlist("refcodesnote")
        i = 0
        for ref in codesList:

            if (ref != "") and (notesList[i] != ""):
                reference1 = reference()
                auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
                for sp in auxSp:
                    varId = sp.id
                targetSpare = spare.objects.get(id=varId)
                reference1.referenceSpare = targetSpare
                reference1.referenceCode = ref
                reference1.referenceNote = notesList[i]
                reference1.save()
            i = i + 1

# Atributes ------------------------------------------------------

        atrtName = request.POST.getlist("atributName")
        atrtVal = request.POST.getlist("atributVal")
        i = 0
        for ref in atrtName:

            if (ref != "") and (atrtVal[i] != ""):
                atribute1 = atribute()
                auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
                for sp in auxSp:
                    varId = sp.id
                targetSpare = spare.objects.get(id=varId)
                atribute1.atributeSpare = targetSpare
                atribute1.atributeName = ref
                atribute1.atributeVal = atrtVal[i]
                atribute1.save()
            i = i + 1

# Dimensions ------------------------------------------------------

        dimName = request.POST.getlist("dimensName")
        dimVal = request.POST.getlist("dimensVal")
        print(dimName)
        print(dimVal)
        i = 0
        for ref in dimName:

            if (ref != "") and (dimVal[i] != ""):
                dimension1 = dimension()
                auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
                for sp in auxSp:
                    varId = sp.id
                targetSpare = spare.objects.get(id=varId)
                dimension1.dimensionSpare = targetSpare
                print(ref)
                print(dimVal[i])
                dimension1.atributeName = ref
                dimension1.atributeVal = dimVal[i]
                dimension1.save()
            i = i + 1

        return render(request,"spareapp/fillspare.html",dic)
    else:
        return render(request,"spareapp/fillspare.html",dic)

def editspare(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    refAux = reference.objects.filter(referenceSpare__spare_code=val)

    spare1 = spare.objects.get(spare_code=val)
    sparefind=spare.objects.filter(spare_code=val)
    # Con sparefind puedo enviar el mismo valor al final para seguir editando

    auxCar = car.objects.filter(spare__spare_code = val)
    auxEnegine = engine.objects.filter(spare__spare_code = val)
    auxVendor = vendor.objects.filter(spare__spare_code = val)
    auxAtributes = atribute.objects.filter(atributeSpare__spare_code = val)
    auxDimensions = dimension.objects.filter(dimensionSpare__spare_code = val)

    dic={"auxDimensions":auxDimensions,"auxAtributes":auxAtributes,"auxVendor":auxVendor,"auxEnegine":auxEnegine,"auxCar":auxCar,"refAux":refAux,"val":val,"sparefind":sparefind,"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if request.method == "POST":

# Eliminamos tabla si no tiene atributos en precios ---------

        # if request.POST.get("pricem")=="":
        #     if spare1.spare_code == None:
        #         pass
        #     else:
        #         spare1.delete()
        #     spare1 = spare()
        
        # if request.POST.get("priced")=="":
        #     if spare1.spare_code == None:
        #         pass
        #     else:
        #         spare1.delete()
        #     spare1 = spare()
        
# Spare ------------------------------------------------------
        sparrr = request.POST.getlist("toReg")
        sparrrPasar = request.POST.getlist("toPass")
        sparrrAux = []
        varcont = 0
        if sparrr == []:
            for sp in allSparesall:
                bandt = False
                for sp2 in sparrrPasar:
                    if str(sp) == str(sp2):
                        varcont = varcont + 1
                        bandt = True
                if bandt == False:
                    sparrrAux.append(sp)
        spare1.spare_code = request.POST.get("cod")
        if request.POST.get("descriptio") == "":
            spare1.spare_name = None
        else:
            spare1.spare_name = request.POST.get("descriptio")
        
        if "phot" in request.FILES:
            spare1.spare_photo = request.FILES['phot']
        else:
            pass

# Cagetory ----------------------------------------------------

        # print("Category")
        # print(request.POST.get("catSelect"))
        if request.POST.get("catSelect") == "":
            # print("Entra")
            # category1 = category.objects.get(category=request.POST.get("catSelect"))
            spare1.spare_category = None
        else:
            category1 = category.objects.get(category=request.POST.get("catSelect"))
            spare1.spare_category = category1



# Prices ------------------------------------------------------

        if request.POST.get("pricem")=="":
            spare1.price_m = None
        else:
            spare1.price_m = request.POST.get("pricem")

        if request.POST.get("priced")=="":
            spare1.price_d = None
        else:
            spare1.price_d = request.POST.get("priced")
        spare1.save()

# Car info ----------------------------------------------------

        cartoreg = request.POST.getlist("cartoReg")
        cartopass = request.POST.getlist("cartoPass")
        carAux = []

        spAux = spare.objects.filter(spare_code=val)

        for sp in spAux:
            for a in sp.car_info.all():
                spare1.car_info.remove(a.id)
        
        if cartoreg == []:
            for c in allCars:
                bandt = False
                for ca in cartopass:
                    if str(c) == str(ca):
                        bandt = True
                if bandt == False:
                    carAux.append(c)

        if cartoreg == []:
            for sp in carAux:
                for c in allCars:
                    if str(c) == str(sp):
                        idAux = c.id
                targetCar = car.objects.get(id=idAux)
                spare1.car_info.add(targetCar)
        else:
            for sp in cartoreg:
                for c in allCars:
                    if str(c) == str(sp):
                        idAux = c.id
                targetCar = car.objects.get(id=idAux)
                spare1.car_info.add(targetCar)
        
# Engine info ----------------------------------------------------

        enginetoreg = request.POST.getlist("enginetoReg")
        enginetopass = request.POST.getlist("enginetoPass")
        engineAux = []

        spAux = spare.objects.filter(spare_code = val)

        for sp in spAux:
            for a in sp.engine_info.all():
                spare1.engine_info.remove(a.id)
        
        if enginetoreg == []:
            for c in allEngines:
                bandt = False
                for ca in enginetopass:
                    if str(c) == str(ca):
                        bandt = True
                if bandt == False:
                    engineAux.append(c)

        if enginetoreg == []:
            for sp in engineAux:
                for c in allEngines:
                    if str(c) == str(sp):
                        idAux = c.id
                targetEngine = engine.objects.get(id=idAux)
                spare1.engine_info.add(targetEngine)
        else:
            for sp in enginetoreg:
                for c in allEngines:
                    if str(c) == str(sp):
                        idAux = c.id
                targetEngine = engine.objects.get(id=idAux)
                spare1.engine_info.add(targetEngine)

# Vendors ----------------------------------------------------

        vendortoreg = request.POST.getlist("vendortoReg")
        vendortopass = request.POST.getlist("vendortoPass")
        vendorAux = []

        spAux = spare.objects.filter(spare_code = val)

        for sp in spAux:
            for a in sp.spare_vendor.all():
                spare1.spare_vendor.remove(a.id)
        
        if vendortoreg == []:
            for c in allVendors:
                bandt = False
                for ca in vendortopass:
                    if str(c) == str(ca):
                        bandt = True
                if bandt == False:
                    vendorAux.append(c)

        if vendortoreg == []:
            for sp in vendorAux:
                for c in allVendors:
                    if str(c) == str(sp):
                        idAux = c.id
                targetVendor = vendor.objects.get(id=idAux)
                spare1.spare_vendor.add(targetVendor)
        else:
            for sp in vendortoreg:
                for c in allVendors:
                    if str(c) == str(sp):
                        idAux = c.id
                targetVendor = vendor.objects.get(id=idAux)
                spare1.spare_vendor.add(targetVendor)

# Spare targets -----------------------------------------------

        spAux = spare.objects.filter(spare_code=val)

        for sp in spAux:
            for a in sp.spare_spare.all():
                spare1.spare_spare.remove(a.id)

        if sparrr == []:
            for sp in sparrrAux:
                varId = 0
                aux = str(sp).split(" ")
                code = (aux[0])

                auxSp = spare.objects.filter(spare_code=code)
                for sp in auxSp:
                    varId = sp.id
                targetCode = spare.objects.get(id=varId)
                spare1.spare_spare.add(targetCode)
        else:
            for sp in sparrr:
                varId = 0
                aux = sp.split(" ")
                code = (aux[0])

                auxSp = spare.objects.filter(spare_code=code)
                for sp in auxSp:
                    varId = sp.id
                targetCode = spare.objects.get(id=varId)
                spare1.spare_spare.add(targetCode)
        
# Reference ------------------------------------------------------
        codesList = request.POST.getlist("refcodes")
        notesList = request.POST.getlist("refcodesnote")

        auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
        if auxSp:
            reference1 = reference.objects.filter(referenceSpare__spare_code=request.POST.get("cod"))
            reference1.delete()
        else:
            print("No consigue codigo")
            reference1 = reference()

        i = 0
        for ref in codesList:

            if (ref != "") and (notesList[i] != ""):
                reference1 = reference()
                auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
                for sp in auxSp:
                    varId = sp.id
                targetSpare = spare.objects.get(id=varId)
                reference1.referenceSpare = targetSpare
                reference1.referenceCode = ref
                reference1.referenceNote = notesList[i]
                reference1.save()
            i = i + 1

# Atributes ------------------------------------------------------

        atrtName = request.POST.getlist("atributName")
        atrtVal = request.POST.getlist("atributVal")

        auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
        if auxSp:
            atribute1 = atribute.objects.filter(atributeSpare__spare_code=request.POST.get("cod"))
            atribute1.delete()
        else:
            print("No consigue codigo")
            atribute1 = reference()

        i = 0
        for ref in atrtName:

            if (ref != "") and (atrtVal[i] != ""):
                atribute1 = atribute()
                auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
                for sp in auxSp:
                    varId = sp.id
                targetSpare = spare.objects.get(id=varId)
                atribute1.atributeSpare = targetSpare
                print(ref)
                print(atrtVal[i])
                atribute1.atributeName = ref
                atribute1.atributeVal = atrtVal[i]
                atribute1.save()
            i = i + 1

# Dimensions ------------------------------------------------------

        dimName = request.POST.getlist("dimensName")
        dimVal = request.POST.getlist("dimensVal")
        print(dimName)
        print(dimVal)
        print(type(dimVal[0]))

        auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
        if auxSp:
            dimension1 = dimension.objects.filter(dimensionSpare__spare_code=request.POST.get("cod"))
            dimension1.delete()
        else:
            dimension1 = dimension()

        i = 0
        for ref in dimName:

            if (ref != "") and (dimVal[i] != ""):
                dimension1 = dimension()
                auxSp = spare.objects.filter(spare_code=request.POST.get("cod"))
                for sp in auxSp:
                    varId = sp.id
                targetSpare = spare.objects.get(id=varId)
                dimension1.dimensionSpare = targetSpare
                dimension1.atributeName = ref
                dimension1.atributeVal = dimVal[i]
                dimension1.save()
            i = i + 1
        
        return render(request,"spareapp/listspare.html",dic)
    else:
        return render(request,"spareapp/editspare.html",dic)


def listspare(request):

    allSparesall=spare.objects.all()
    allVendors=vendor.objects.all()
    dic={"allSparesall":allSparesall,"allVendors":allVendors}

    return render(request,"spareapp/listspare.html",dic)

def listengine(request):
    allEngines=engine.objects.all()
    dic={"allEngines":allEngines}

    return render(request,"spareapp/listengine.html",dic)

def listcar(request):
    allCars=car.objects.all()
    dic={"allCars":allCars}

    return render(request,"spareapp/listcar.html",dic)

def deleteengine(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    engine1 = engine.objects.get(engine_ide=val)
    engine1.delete()
    # sparefind=spare.objects.filter(spare_code=val)
    dic={"val":val,"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/listengine.html",dic)

def deletespare(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    spare1 = spare.objects.get(spare_code=val)
    spare1.delete()
    # sparefind=spare.objects.filter(spare_code=val)
    dic={"val":val,"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/listspare.html",dic)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def deletecar(request,val):
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    car1 = car.objects.get(id=val)
    car1.delete()
    # sparefind=spare.objects.filter(spare_code=val)
    dic={"val":val,"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/listcar.html",dic)

def fillcategory(request):

    print("Entra en fillCategory")

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    print(request.POST)
    category1 = category()
    print("categor")
    print(request.POST.get("categor"))
    category1.category = request.POST.get("categor")
    category1.save()

    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/fillspare.html",dic)

def fillvendor(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    print(request.POST.get("vendo"))
    vendor1 = vendor()    
    vendor1.vendorName = request.POST.get("vendo")
    vendor1.save()
    # category1 = category()
    # category1.category = request.POST.get("categor")
    # category1.save()

    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/fillspare.html",dic)

def importCar(request):
    
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    print(request.POST)

    if "phot" in request.FILES:
        print("Hay archivo")

        FILE_PATH = request.FILES['phot']
        
        # FILE_PATH = "prueba.xlsx"

        workbook = load_workbook(FILE_PATH)
        sheet = workbook.active

        maxCol = []
        maxRow = []

        for col in sheet.iter_rows():
            maxCol.append(col)
        
        i=0
        poscar_manufacturer = -1
        poscar_model = -1
        poscarfrom = -1
        poscarto = -1
        postransmission = -1
        cont = 0
        for fil in maxCol:
            j=0
            for col in fil:
                if col.value == "manufacturer":
                    poscar_manufacturer = j
                    cont = cont + 1
                if col.value == "model":
                    poscar_model = j
                    cont = cont + 1
                if col.value == "from":
                    poscarfrom = j
                    cont = cont + 1
                if col.value == "to":
                    poscarto = j
                    cont = cont + 1
                if col.value == "chasis":
                    postransmission = j
                    cont = cont + 1
                j=j+1
            i=i+1

        print(cont)
        if cont > 0:
            i=0
            for fil in maxCol:
                j=0
                if i>0:
                    car1 = car()
                for col in fil:
                    if i>0:
                        if j == poscar_manufacturer:
                            car1.car_manufacturer = col.value
                        if j == poscar_model:
                            car1.car_model = col.value
                        if j == poscarfrom:
                            car1.carfrom = col.value
                        if j == poscarto:
                            car1.carto = col.value
                        if j == postransmission:
                            car1.transmission = col.value
                        car1.save()
                    j=j+1
                i=i+1

    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/fillspare.html",dic)

def importEngine(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    if "phot" in request.FILES:

        FILE_PATH = request.FILES['phot']

        # FILE_PATH = "prueba2.xlsx"

        workbook = load_workbook(FILE_PATH)
        sheet = workbook.active

        maxCol = []

        for col in sheet.iter_rows():
            maxCol.append(col)
        
        i=0
        engLitres = -1
        engCode = -1
        engType = -1
        engValve = -1
        engPistons = -1
        cont = 0
        for fil in maxCol:
            j=0
            for col in fil:
                if col.value == "litres":
                    engLitres = j
                    cont = cont + 1
                if col.value == "ecode":
                    engCode = j
                    cont = cont + 1
                if col.value == "type":
                    engType = j
                    cont = cont + 1
                if col.value == "valve":
                    engValve = j
                    cont = cont + 1
                if col.value == "pistons":
                    engPistons = j
                    cont = cont + 1
                j=j+1
            i=i+1

        if cont > 0:
            i=0
            for fil in maxCol:
                j=0
                if i>0:
                    engine1 = engine()
                for col in fil:
                    if i>0:
                        if j == engLitres:
                            engine1.engine_l = col.value
                        if j == engCode:
                            engine1.engine_ide = col.value
                        if j == engType:
                            engine1.engine_type = col.value
                        if j == engValve:
                            engine1.engine_cylinder = col.value
                        if j == engPistons:
                            engine1.engine_pistons = col.value
                        engine1.save()
                    j=j+1
                i=i+1

    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/fillspare.html",dic)

def importSpare(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    ref2=reference.objects.values("referenceSpare").order_by("referenceSpare").distinct()

    if "phot" in request.FILES:

        FILE_PATH = request.FILES['phot']

        # FILE_PATH = "prueba3.xlsx"

        workbook = load_workbook(FILE_PATH, data_only = True)
        sheet = workbook.active

        maxCol = []

        for col in sheet.iter_rows():
            # print(col)
            maxCol.append(col)
        
        i=0
        spCode = -1
        spDesc = -1
        spPricem = -1
        spPriced = -1
        spReference = -1
        spAttribute = -1
        spDimension = -1
        spNote = -1
        spCategory = -1
        spVendor = -1
        cont = 0

        for fil in maxCol:
            j=0
            for col in fil:
                if col.value == "CODE":
                    spCode = j
                    cont = cont + 1
                if col.value == "DESCRIPTION":
                    spDesc = j
                    cont = cont + 1
                if col.value == "PRICEM":
                    spPricem = j
                    cont = cont + 1
                if col.value == "PRICED":
                    spPriced = j
                    cont = cont + 1
                if col.value == "REFERENCE":
                    spReference = j
                    cont = cont + 1
                if col.value == "ATTRIBUTE":
                    spAttribute = j
                    cont = cont + 1
                if col.value == "DIMENSION":
                    print("Entra en dimension j")
                    spDimension = j
                    cont = cont + 1
                if col.value == "CATEGORY":
                    spCategory = j
                    cont = cont + 1
                if col.value == "VENDOR":
                    spVendor = j
                    cont = cont + 1
                if col.value == "NOTE":
                    spNote = j
                    cont = cont + 1
                j=j+1
            i=i+1

        if cont > 0:
            i=0
            CodeAux = ""
            refName = ""
            refDesc = ""
            AtrName = ""
            AtrDesc = ""
            DimName = ""
            DimDesc = ""
            VenName = ""

            varRefAux = ""
            varAtrAux = ""
            varDimAux = ""
            for fil in maxCol:
                varRefAux = ""
                varAtrAux = ""
                varDimAux = ""
                bandera = True
                j=0
                if i>0:
                    print("Columna: "+str(i)+"----------------------------------------")
                    spare1 = spare()
                    
                for col in fil:

                    if i>0:
                        if j == spCode:
                            print("Entra en codigo.....")
                            if col.value == None:
                                print("Codigo: "+CodeAux)
                                bandera = False
                            else:
                                # spare1 = spare()
                                print("Codigo: "+str(col.value))
                                CodeAux = col.value
                                spare1.spare_code = col.value
                                bandera = True
                        if j == spDesc:
                            print("Entra en descripcion.....")
                            print("Descripción: "+str(col.value))
                            if col.value != None:
                                spare1.spare_name = col.value
                        if j == spPricem:
                            print("Entra en Price M.....")
                            # print(get_column_letter(col.value))
                            print("Price M: "+str(col.value))
                            if col.value != None:
                                spare1.price_m = col.value
                        if j == spPriced:
                            print("Price D: "+str(col.value))
                            if col.value != None:
                                spare1.price_d = col.value
                        if j == spNote:
                            print("Note: "+str(col.value))
                            if col.value != None:
                                spare1.note = col.value
                        if j == spCategory:
                            print("Entra en category.....")
                            if col.value != None:
                                print("Category: "+str(col.value))
                                if category.objects.filter(category=col.value):
                                    category1 = category.objects.get(category=col.value)
                                else:
                                    category1 = category()
                                    category1.category = col.value
                                    category1.save()
                                spare1.spare_category = category1
                        if j == spVendor:
                            print("Entra a vendor....")
                            if col.value != None:
                                print("Vendor: "+str(col.value))
                                # if vendor.objects.filter(category=col.value):
                                #     vendor1 = vendor.objects.get(category=col.value)
                                # else:
                                #     vendor1 = vendor()
                                #     vendor1.vendorName = col.value
                                #     vendor1.save()
                                # spare1.spare_vendor = vendor1
                                VenName = col.value
                            else:
                                VenName = None

                        if j == spReference:
                            print("Entra en referencia.....")
                            if col.value != None:
                                varRefAux = col.value.split("\n")
                                print(varRefAux)
                                print(len(varRefAux))
                                # for varA in varRefAux:

                                #     varA = col.value.split("=")
                                #     print(varA)
                                #     print(len(varA))
                                #     print(varA[0])
                                #     refName = varA[0]
                                #     if len(varA)>1:
                                #         print(varA[1])
                                #         refDesc = varA[1]
                                    
                                #     print("Reference: "+str(col.value))
                            else:
                                refName = None
                                refDesc = None
                        if j == spAttribute:
                            print("Entra en atributos.....")
                            if col.value != None:
                                varAtrAux = col.value.split("\n")

                                # varA = col.value.split("=")
                                # print(varA[0])
                                # AtrName = varA[0]
                                # print(varA[1])
                                # AtrDesc = varA[1]
                            else:
                                AtrName = None
                                AtrDesc = None
                        if j == spDimension:
                            print("Entra en dimensiones.....")
                            if col.value != None:
                                varDimAux = col.value.split("\n")
                                # varA = col.value.split("=")
                                # print(varA[0])
                                # DimName = varA[0]
                                # print(varA[1])
                                # DimDesc = varA[1]
                            else:
                                DimName = None
                                DimDesc = None
                        
                    j=j+1
                print(bandera)
                print(i)
                if bandera == True and i>0:
                    print("Guarda spare")
                    spare1.save()
                    # Agregamos referencias
                    print("Agregamos referencias")
                    for var in varRefAux:
                        varA = var.split("=")
                        # print(varA)
                        # print(len(varA))
                        # print(varA[0])
                        refName = varA[0]
                        if len(varA)>1:
                            # print(varA[1])
                            refDesc = varA[1]
                        
                        print("Reference: "+str(var))

                        if refName != None:
                            reference1 = reference()
                            print("Agregamos la referencia.....")
                            # print(CodeAux)
                            auxSp = spare.objects.filter(spare_code=CodeAux)
                            # print("Crea el spare:.....")
                            # print(auxSp)
                            varId=0
                            for sp in auxSp:
                                varId = sp.id
                            targetSpare = spare.objects.get(id=varId)
                            reference1.referenceSpare = targetSpare
                            reference1.referenceCode = refName
                            reference1.referenceNote = refDesc
                            reference1.save()
                    # Agregamos atributos
                    print("Agregamos atributos")
                    for var in varAtrAux:
                        print(var)
                        varA = var.split("=")
                        AtrName = varA[0]
                        print(AtrName)
                        AtrDesc = varA[1]
                        print(AtrDesc)

                        if AtrName != None:
                            print("Tiene un atributo para agregar.....")
                            if AtrName != "":
                                print("Agregamos el atributo.....")
                                atribute1 = atribute()
                                auxSp = spare.objects.filter(spare_code=CodeAux)
                                print(auxSp)
                                varId=0
                                for sp in auxSp:
                                    varId = sp.id
                                targetSpare = spare.objects.get(id=varId)
                                atribute1.atributeSpare = targetSpare
                                atribute1.atributeName = AtrName
                                atribute1.atributeVal = AtrDesc
                                atribute1.save()
                    # Agregamos dimensiones
                    for var in varDimAux:
                        varA = var.split("=")
                        DimName = varA[0]
                        DimDesc = varA[1]
                        if DimName != None:
                            print("Tiene una dimension para agregar")
                            if DimName != "":
                                print("Agregamos la dimension.....")
                                dimension1 = dimension()
                                auxSp = spare.objects.filter(spare_code=CodeAux)
                                varId=0
                                for sp in auxSp:
                                    varId = sp.id
                                targetSpare = spare.objects.get(id=varId)
                                dimension1.dimensionSpare = targetSpare
                                dimension1.atributeName = DimName
                                dimension1.atributeVal = DimDesc
                                dimension1.save()
                    # Agregamos vendor
                    if VenName != None:
                        print("Agregamos vendor")
                        if vendor.objects.filter(vendorName=VenName):
                            vendor1 = vendor.objects.get(vendorName=VenName)
                        else:
                            vendor1 = vendor()
                            vendor1.vendorName = VenName
                            vendor1.save()
                        spare1.spare_vendor.add(vendor1)

                        # dimension1 = dimension()
                        # auxSp = spare.objects.filter(spare_code=CodeAux)
                        # varId=0
                        # for sp in auxSp:
                        #     varId = sp.id
                        # targetSpare = spare.objects.get(id=varId)
                        # dimension1.dimensionSpare = targetSpare
                        # dimension1.atributeName = DimName
                        # dimension1.atributeVal = DimDesc
                        # dimension1.save()
                else:
                    print("No guarda Spare")
                    # Pero puede guardar referencias
                    if refName != None and i>0:
                        print("Hay reference Code.....")
                        print(auxSp)
                        # reference1 = reference.objects.get(referenceSpare__spare_code=CodeAux)
                        reference1 = reference()
                        auxSp = spare.objects.filter(spare_code=CodeAux)
                        varId=0
                        for sp in auxSp:
                            varId = sp.id
                        targetSpare = spare.objects.get(id=varId)
                        reference1.referenceSpare = targetSpare
                        reference1.referenceCode = refName
                        reference1.referenceNote = refDesc
                        reference1.save()
                    if AtrName != None and i>0:
                        if AtrName != "":
                            print("Hay Atributos.....")
                            print(auxSp)
                            # reference1 = reference.objects.get(referenceSpare__spare_code=CodeAux)
                            atribute1 = atribute()
                            auxSp = spare.objects.filter(spare_code=CodeAux)
                            varId=0
                            for sp in auxSp:
                                varId = sp.id
                            targetSpare = spare.objects.get(id=varId)
                            atribute1.atributeSpare = targetSpare
                            atribute1.atributeName = AtrName
                            atribute1.atributeVal = AtrDesc
                            atribute1.save()
                    if DimName != None and i>0:
                        if DimName != "":
                            print("Hay dimensiones.....")
                            print(auxSp)
                            # reference1 = reference.objects.get(referenceSpare__spare_code=CodeAux)
                            dimension1 = dimension()
                            auxSp = spare.objects.filter(spare_code=CodeAux)
                            varId=0
                            for sp in auxSp:
                                varId = sp.id
                            targetSpare = spare.objects.get(id=varId)
                            dimension1.dimensionSpare = targetSpare
                            dimension1.atributeName = DimName
                            dimension1.atributeVal = DimDesc
                            dimension1.save()
                    if VenName != None and i>0:
                        print("Hay vendor.....")
                        if vendor.objects.filter(vendorName=VenName):
                            vendor1 = vendor.objects.get(vendorName=VenName)
                        else:
                            vendor1 = vendor()
                            vendor1.vendorName = VenName
                            vendor1.save()
                        spare1.spare_vendor.add(vendor1)
                i=i+1

    dic={"refSpare":ref2,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/fillspare.html",dic)

def register(request):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")


    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form is valid")
            username = form.cleaned_data["username"]
            userAux=User.objects.get(username=form.cleaned_data["username"])
            print(username)
            print(form)
            print(type(form))
            profileAux = Profile()
            profileAux.ventas = False
            profileAux.bodega = False
            profileAux.mayorista = False
            profileAux.detal = True
            profileAux.user = userAux
            profileAux.save()
            messages.success(request,f"User {username} created")
            return redirect("home")
    else:
        form = UserRegisterForm()
    
    dic={"form":form,"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/register.html",dic)

def cart(request,val):

    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    spCartAll=spareCart.objects.all()
    # spCart=spareCart.objects.values("spareId","nameUser").distinct()
    spares = spare.objects.all().order_by("spare_name","spare_code","spare_brand")

    # print("User: "+str(val))
    spCartPost=spareCart.objects.filter(spareId=request.POST.get("cartN"))
    spCart = spareCart.objects.filter(nameUser=val).values("spareId","nameUser").distinct().order_by("spareId")
    # print("Cart")
    # print(spCartMain)
    cartIdPasar = request.POST.get("cartN")
    
    if request.method == "POST":
        print("Entra al POST")
        print(request.POST)
        if request.POST.get("cartN") == None:
            cartIdPasar = request.POST.get("cartPasar")
        else:
            cartIdPasar = request.POST.get("cartN")
        spCartPost = spareCart.objects.filter(spareId=request.POST.get("cartN"),nameUser=val)
        spCart = spareCart.objects.values("spareId","nameUser").filter(nameUser=val).distinct().order_by("spareId")

        # print(request.POST)
        if request.POST.get("cartOpen"):
            print("Manda a abrir")
        if request.POST.get("cartDelete"):
            print("Manda a borrar")
            cartDelete=spareCart.objects.filter(spareId=request.POST.get("cartN"))
            print(cartDelete)
            cartDelete.delete()
        # spCart = spareCart.objects.values("spareId","nameUser").filter(spareId=request.POST.get("cartN"),nameUser=val).distinct()

        delist = request.POST.getlist("toDel")
        if delist:
            print("Entra a delist para borrar individualmente")
            cartElementDelete=spareCart.objects.filter(spareId=request.POST.get("cartPasar"))
            for el in cartElementDelete:
                for de in delist:
                    if el.spareCode == de:
                        print("Debe borrar")
                        print(de)
                        el.delete()
            spCartPost = spareCart.objects.filter(spareId=request.POST.get("cartPasar"))
            

    dic={"cartIdPasar":cartIdPasar,"spare":spares,"spCartMain":spCartPost,"spCartAll":spCartAll,"spCart":spCart,"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/cart.html",dic)

def listAdmin(request):
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    spCartAll=spareCart.objects.all()
    allUser=User.objects.all()

    dic={"allUser":allUser,"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/listAdmin.html",dic)

def userProfile(request,val):
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    spCartAll=spareCart.objects.all()
    allUser=User.objects.all()
    userP=User.objects.filter(id=val)

    dic={"userP":userP,"allUser":allUser,"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    if request.method == "POST":

        print(request.POST)
        userP=User.objects.get(id=val)
        print(type(userP))
        print(userP)
        # userPa=User.objects.filter(id=val)
        # print(userP.profile.all)
        profileP=Profile.objects.filter(user=userP)
        print("Obtiene profileP")
        print(profileP)
        # print(userP)
        # print(userP.is_superuser)
        if request.POST.get("superuser"):
            print("Es superuser")
            userP.is_superuser=True
        else:
            userP.is_superuser=False

        if profileP:
            if request.POST.get("ventas"):
                print("Es ventas")
                userP.profile.ventas=True
            else:
                userP.profile.ventas=False
            if request.POST.get("bodega"):
                print("Es bodega")
                userP.profile.bodega=True
            else:
                userP.profile.bodega=False
            if request.POST.get("mayorista"):
                print("Es mayorista")
                userP.profile.mayorista=True
            else:
                userP.profile.mayorista=False
            if request.POST.get("detal"):
                print("Es detal")
                userP.profile.detal=True
            else:
                userP.profile.detal=False
        else:
            profileAux=Profile()
            profileAux.user=userP
            if request.POST.get("ventas"):
                print("Es ventas")
                profileAux.ventas=True
            else:
                profileAux.ventas=False
            if request.POST.get("bodega"):
                print("Es bodega")
                profileAux.bodega=True
            else:
                profileAux.bodega=False
            if request.POST.get("mayorista"):
                print("Es mayorista")
                profileAux.mayorista=True
            else:
                profileAux.mayorista=False
            if request.POST.get("detal"):
                print("Es detal")
                profileAux.detal=True
            else:
                profileAux.detal=False
            profileAux.save()
        userP.save()
        userP.profile.save()

        return render(request,"spareapp/listAdmin.html",dic)


    return render(request,"spareapp/userProfile.html",dic)

def deleteuser(request,val):
    dim=dimension.objects.values("atributeName").distinct()
    dim2=dimension.objects.all()
    atr=atribute.objects.values("atributeName").distinct()
    atr2=atribute.objects.all()
    allSparesall=spare.objects.all()
    allCategories=category.objects.all()
    allEngines=engine.objects.all()
    onlyManufCars=car.objects.all().values("car_manufacturer").order_by("car_manufacturer").distinct()
    manu=car.objects.values("car_manufacturer").order_by("car_manufacturer").distinct()
    allCars=car.objects.all()
    allSpares=spare.objects.values("spare_name","spare_category").order_by("spare_name").distinct()
    allVendors=vendor.objects.all()
    ref=reference.objects.all().order_by("referenceSpare")
    spCartAll=spareCart.objects.all()
    allUser=User.objects.all()

    userAux=User.objects.filter(id=val)
    print(userAux)
    userAux.delete()

    dic={"allUser":allUser,"manu":manu,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}

    return render(request,"spareapp/listAdmin.html",dic)

# ------------------------------ Contabilidad -----------------------------------

def contBase(request):

    return render(request,"spareapp/contBase.html")

def contDay(request):

    tod = datetime.now().date()

    tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo")

    allTypes = factType.objects.all()

    contStart = 0
    contPagos = 0
    contRetiros = 0
    contStart = 0
    contTotal = 0

    if tableAux:

        print("Existe tabla")

        for typ in allTypes:

            for tab in tableAux:

                if tab.tabTipo == typ:

                    tableAuxGet = mainTable.objects.get(fecha__date=tod,tabTipo__nombre=typ)

                    facturaAuxIngreso = factura.objects.filter(fechaCreado__date=tod,refCategory__ingreso=True,refType__nombre=typ)
                    contIngreso = 0

                    for ing in facturaAuxIngreso:
                        contIngreso = contIngreso+ing.monto

                    tableAuxGet.tabPagos = contIngreso

                    facturaAuxEgreso = factura.objects.filter(fechaCreado__date=tod,refCategory__egreso=True,refType__nombre=typ)
                    contEgreso = 0

                    for ing in facturaAuxEgreso:
                        contEgreso = contEgreso+ing.monto

                    tableAuxGet.tabRetiros = contEgreso

                    tableAuxGet.tabTotal = tableAuxGet.tabStart+contIngreso-contEgreso

                    tableAuxGet.save()

        for tab in tableAux:

            if tab.tabStart > 0:

                contStart = contStart + tab.tabStart

            if tab.tabPagos > 0:

                contPagos = contPagos + tab.tabPagos
            
            if tab.tabRetiros > 0:

                contRetiros = contRetiros + tab.tabRetiros
        
        contTotal = contStart + contPagos - contRetiros

    else:

        print("No existe tabla")

        for typ in allTypes:
            
            tableAux = mainTable()
            tableAux.tabTipo = typ

            tableAux.tabStart = 0
            tableAux.tabPagos = 0
            tableAux.tabRetiros = 0
            total = tableAux.tabStart+tableAux.tabPagos-tableAux.tabRetiros
            tableAux.tabTotal = total

            tableAux.save()


    allFacturesToPay = factura.objects.filter(refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(refCategory__egreso=True,refCategory__limite=True)
    
    facturesToPay = len(allFacturesToPay)
    facturesToCollect = len(allFacturesToCollect)

    dic = {"contStart":contStart,"contPagos":contPagos,"contRetiros":contRetiros,"contTotal":contTotal,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect}

    return render(request,"spareapp/contDay.html",dic)

def contEntry(request):

    allTypes = factType.objects.all().order_by("nombre")
    allCategories = factCategory.objects.filter(ingreso=True).order_by("nombre")

    dic = {"allTypes":allTypes,"allCategories":allCategories}

    if request.method == "POST":

        factAux = factura()

        contNombre = request.POST.get("contNombre")
        nomAux = persona.objects.get(nombre=contNombre)
        factAux.refPersona = nomAux

        contNumFac = request.POST.get("contNumFac")
        factAux.num = contNumFac

        contTypeIng = request.POST.get("contTypeIng")
        typeAux = factType.objects.get(nombre=contTypeIng)
        factAux.refType = typeAux

        contCatIng = request.POST.get("contCatIng")
        catAux = factCategory.objects.get(nombre=contCatIng)
        factAux.refCategory = catAux

        if request.POST.get("contFechaTope") != "":
            contFechaTope = request.POST.get("contFechaTope")
            factAux.fechaTope = contFechaTope

        contMonto = request.POST.get("contMonto")
        factAux.monto = contMonto

        factAux.save()

        # -----------------------------

        tod = datetime.now().date()

        for typ in allTypes:

            tableAuxGet = mainTable.objects.get(fecha__date=tod,tabTipo__nombre=typ)

            facturaAuxIngreso = factura.objects.filter(fechaCreado__date=tod,refCategory__ingreso=True,refType__nombre=typ)
            contIngreso = 0

            for ing in facturaAuxIngreso:
                contIngreso = contIngreso+ing.monto

            tableAuxGet.tabPagos = contIngreso

            facturaAuxEgreso = factura.objects.filter(fechaCreado__date=tod,refCategory__egreso=True,refType__nombre=typ)
            contEgreso = 0

            for ing in facturaAuxEgreso:
                contEgreso = contEgreso+ing.monto

            tableAuxGet.tabRetiros = contEgreso

            tableAuxGet.tabTotal = tableAuxGet.tabStart+contIngreso-contEgreso

            tableAuxGet.save()
        
        contPagos = 0
        contRetiros = 0
        contStart = 0

        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo")

        for tab in tableAux:

            if tab.tabStart > 0:

                contStart = contStart + tab.tabStart

            if tab.tabPagos > 0:

                contPagos = contPagos + tab.tabPagos
            
            if tab.tabRetiros > 0:

                contRetiros = contRetiros + tab.tabRetiros
        
        contTotal = contStart + contPagos - contRetiros

        allFacturesToPay = factura.objects.filter(refCategory__ingreso=True,refCategory__limite=True)
        allFacturesToCollect = factura.objects.filter(refCategory__egreso=True,refCategory__limite=True)
        
        facturesToPay = len(allFacturesToPay)
        facturesToCollect = len(allFacturesToCollect)

        dic = {"contStart":contStart,"contPagos":contPagos,"contRetiros":contRetiros,"contTotal":contTotal,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"allTypes":allTypes,"allCategories":allCategories}

        return render(request,"spareapp/contDay.html",dic)

    return render(request,"spareapp/contEntry.html",dic)

def contType(request,val,val2):

    tod = datetime.now().date()

    allFacturesVal = factura.objects.filter(fechaCreado__date=tod,refType__nombre=val)

    if val2 != "today":

        tod = val2

        allFacturesVal = factura.objects.filter(fechaCreado__date=tod,refType__nombre=val)

    dic = {"val2":val2,"allFacturesVal":allFacturesVal,"val":val}

    if request.method == "POST":

        tod = datetime.now().date()
        contStart = request.POST.get("contStart")

        tableAuxGet = mainTable.objects.get(fecha__date=tod,tabTipo__nombre=val)
        tableAuxGet.tabStart = contStart

        facturaAuxIngreso = factura.objects.filter(fechaCreado__date=tod,refCategory__ingreso=True,refType__nombre=val)
        contIngreso = 0

        for ing in facturaAuxIngreso:
            contIngreso = contIngreso+ing.monto

        tableAuxGet.tabPagos = contIngreso

        facturaAuxEgreso = factura.objects.filter(fechaCreado__date=tod,refCategory__egreso=True,refType__nombre=val)
        contEgreso = 0

        for ing in facturaAuxEgreso:
            contEgreso = contEgreso+ing.monto

        tableAuxGet.tabRetiros = contEgreso

        tableAuxGet.tabTotal = float(tableAuxGet.tabStart)+contIngreso-contEgreso

        tableAuxGet.save()

        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo")

        allTypes = factType.objects.all()

        if tableAux:

            contPagos = 0
            contRetiros = 0
            contStart = 0

            for tab in tableAux:

                if tab.tabStart > 0:

                    contStart = contStart + tab.tabStart

                if tab.tabPagos > 0:

                    contPagos = contPagos + tab.tabPagos
                
                if tab.tabRetiros > 0:

                    contRetiros = contRetiros + tab.tabRetiros
            
            contTotal = contStart + contPagos - contRetiros

        allFacturesToPay = factura.objects.filter(refCategory__ingreso=True,refCategory__limite=True)
        allFacturesToCollect = factura.objects.filter(refCategory__egreso=True,refCategory__limite=True)
        
        facturesToPay = len(allFacturesToPay)
        facturesToCollect = len(allFacturesToCollect)
        
        dic = {"contStart":contStart,"contPagos":contPagos,"contRetiros":contRetiros,"contTotal":contTotal,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect}

        return render(request,"spareapp/contDay.html",dic)

    return render(request,"spareapp/contType.html",dic)

def contSpend(request):

    allTypes = factType.objects.all().order_by("nombre")
    allCategories = factCategory.objects.filter(egreso=True).order_by("nombre")

    dic = {"allTypes":allTypes,"allCategories":allCategories}

    if request.method == "POST":
        
        factAux = factura()

        contNombre = request.POST.get("contNombre")
        nomAux = persona.objects.get(nombre=contNombre)
        factAux.refPersona = nomAux

        contNumFac = request.POST.get("contNumFac")
        factAux.num = contNumFac

        contTypeIng = request.POST.get("contTypeIng")
        typeAux = factType.objects.get(nombre=contTypeIng)
        factAux.refType = typeAux

        contCatIng = request.POST.get("contCatEgr")
        catAux = factCategory.objects.get(nombre=contCatIng)
        factAux.refCategory = catAux

        if request.POST.get("contFechaTope") != "":
            contFechaTope = request.POST.get("contFechaTope")
            factAux.fechaTope = contFechaTope

        contMonto = request.POST.get("contMonto")
        factAux.monto = contMonto

        factAux.save()

        tod = datetime.now().date()

        for typ in allTypes:

            tableAuxGet = mainTable.objects.get(fecha__date=tod,tabTipo__nombre=typ)

            facturaAuxIngreso = factura.objects.filter(fechaCreado__date=tod,refCategory__ingreso=True,refType__nombre=typ)
            contIngreso = 0

            for ing in facturaAuxIngreso:
                contIngreso = contIngreso+ing.monto

            tableAuxGet.tabPagos = contIngreso

            facturaAuxEgreso = factura.objects.filter(fechaCreado__date=tod,refCategory__egreso=True,refType__nombre=typ)
            contEgreso = 0

            for ing in facturaAuxEgreso:
                contEgreso = contEgreso+ing.monto

            tableAuxGet.tabRetiros = contEgreso

            tableAuxGet.tabTotal = tableAuxGet.tabStart+contIngreso-contEgreso

            tableAuxGet.save()
        
        contPagos = 0
        contRetiros = 0
        contStart = 0

        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo")

        for tab in tableAux:

            if tab.tabStart > 0:

                contStart = contStart + tab.tabStart

            if tab.tabPagos > 0:

                contPagos = contPagos + tab.tabPagos
            
            if tab.tabRetiros > 0:

                contRetiros = contRetiros + tab.tabRetiros
        
        contTotal = contStart + contPagos - contRetiros

        allFacturesToPay = factura.objects.filter(refCategory__ingreso=True,refCategory__limite=True)
        allFacturesToCollect = factura.objects.filter(refCategory__egreso=True,refCategory__limite=True)
        
        facturesToPay = len(allFacturesToPay)
        facturesToCollect = len(allFacturesToCollect)

        dic = {"contStart":contStart,"contPagos":contPagos,"contRetiros":contRetiros,"contTotal":contTotal,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"allTypes":allTypes,"allCategories":allCategories}

        return render(request,"spareapp/contDay.html",dic)

    return render(request,"spareapp/contSpend.html",dic)

def contToPay(request):

    allFacturesPay = factura.objects.filter(refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")

    acum = 0

    for fac in allFacturesPay:

        acum = acum + fac.monto

    tod = datetime.now()

    dic = {"allFacturesPay":allFacturesPay,"montoTotal":acum}

    return render(request,"spareapp/contToPay.html",dic)

def contToCollect(request):

    allFacturesPay = factura.objects.filter(refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")

    acum = 0

    for fac in allFacturesPay:

        acum = acum + fac.monto

    tod = datetime.now()

    dic = {"allFacturesPay":allFacturesPay,"montoTotal":acum}

    return render(request,"spareapp/contToCollect.html",dic)

def contAdmin(request):

    return render(request,"spareapp/contAdmin.html")

def contAddType(request):

    if request.method == "POST":

        typeNombre = request.POST.get("typeNombre")

        if typeNombre != "":

            listType = factType.objects.filter(nombre=typeNombre)

            if (listType):

                print("Ya existe éste type")

            else:

                factTypeAux = factType()
                factTypeAux.nombre = typeNombre
                factTypeAux.save()

        return render(request,"spareapp/contAddType.html")

    return render(request,"spareapp/contAddType.html")

def contAddCategory(request):

    if request.method == "POST":

        catNombre = request.POST.get("catNombre")
        catIngreso = request.POST.get("catIngreso")
        catEgreso = request.POST.get("catEgreso")
        catExpirationDate = request.POST.get("catExpirationDate")
        listCategory = factCategory.objects.filter(nombre=catNombre)

        if (listCategory):

                print("Ya existe ésta categoría")
                
        else:

            factCatAux = factCategory()
            factCatAux.nombre = catNombre
            if catIngreso:
                factCatAux.ingreso = True
            if catEgreso:
                factCatAux.egreso = True
            if catExpirationDate:
                factCatAux.limite = True
            factCatAux.save()

        return render(request,"spareapp/contAddCategory.html")

    return render(request,"spareapp/contAddCategory.html")

def contListType(request):

    allTypes = factType.objects.all().order_by("nombre")

    dic = {"allTypes":allTypes}

    return render(request,"spareapp/contListType.html",dic)

def contListCategory(request):

    allCategories = factCategory.objects.all().order_by("nombre")

    dic = {"allCategories":allCategories}

    return render(request,"spareapp/contListCategory.html",dic)

def contDeleteType(request,val):

    allTypes = factType.objects.all()

    singleType = factType.objects.get(id=val)

    singleType.delete()

    dic = {"allTypes":allTypes}

    return render(request,"spareapp/contListType.html",dic)

def contDeleteCategory(request,val):

    allCategories = factCategory.objects.all().order_by("nombre")

    singleCategory = factCategory.objects.get(id=val)

    singleCategory.delete()

    dic = {"allCategories":allCategories}

    return render(request,"spareapp/contListCategory.html",dic)

def contEditType(request,val):

    allTypes = factType.objects.all().order_by("nombre")

    singleType = factType.objects.filter(id=val)

    if request.method == "POST":

        singleType = factType.objects.get(id=val)
        singleType.nombre = request.POST.get("typeNombre")
        singleType.save()

        dic = {"singleType":singleType,"allTypes":allTypes}

        return render(request,"spareapp/contListType.html",dic)

    dic = {"singleType":singleType,"allTypes":allTypes}

    return render(request,"spareapp/contEditType.html",dic)

def contEditCategory(request,val):

    allCategories = factCategory.objects.all().order_by("nombre")

    singleCategory = factCategory.objects.filter(id=val)

    if request.method == "POST":

        print(request.POST)

        singleCategory = factCategory.objects.get(id=val)
        singleCategory.nombre = request.POST.get("catNombre")
        if request.POST.get("catIngreso"):
            singleCategory.ingreso = True
        else:
            singleCategory.ingreso = False
        if request.POST.get("catEgreso"):
            singleCategory.egreso = True
        else:
            singleCategory.egreso = False
        if request.POST.get("catExpirationDate"):
            singleCategory.limite = True
        else:
            singleCategory.limite = False
        singleCategory.save()

        dic = {"singleCategory":singleCategory,"allCategories":allCategories}

        return render(request,"spareapp/contListCategory.html",dic)

    dic = {"singleCategory":singleCategory,"allCategories":allCategories}

    return render(request,"spareapp/contEditCategory.html",dic)

def contByDay(request):

    tod = request.POST.get("searchDate")

    tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo")

    allTypes = factType.objects.all()

    contPagos = 0
    contRetiros = 0
    contStart = 0

    for tab in tableAux:

        if tab.tabStart > 0:

            contStart = contStart + tab.tabStart

        if tab.tabPagos > 0:

            contPagos = contPagos + tab.tabPagos
        
        if tab.tabRetiros > 0:

            contRetiros = contRetiros + tab.tabRetiros
    
    contTotal = contStart + contPagos - contRetiros

    allFacturesToPay = factura.objects.filter(refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(refCategory__egreso=True,refCategory__limite=True)
    
    facturesToPay = len(allFacturesToPay)
    facturesToCollect = len(allFacturesToCollect)

    dic = {"tod":tod,"contStart":contStart,"contPagos":contPagos,"contRetiros":contRetiros,"contTotal":contTotal,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect}

    return render(request,"spareapp/contByDay.html",dic)

def contByRange(request):

    tod = request.POST.get("searchDate")

    if request.method == "POST":

        print("Entra a POST")

        contStart = 0
        contIngreso = 0
        contEgreso = 0

        # Obtengo las fechas de inicio y fin de busqueda
        dateFrom = request.POST.get("searchDateFrom")
        dateTo = request.POST.get("searchDateTo")

        # OBtengo todos los types
        allTypes = factType.objects.all()

        # tableAux = mainTable.objects.filter(fecha__date__gte=dateFrom,fecha__date__lte=dateTo)

        # Inicializo todas las facturas por el rango deseado
        allFacturesRange = ""

        # Si existe el rango, obtengo todas las facturas en dicho rango
        if dateFrom and dateTo:
            allFacturesRange = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo)

        # Obtengo todas las tablas auxiliares
        tableAux = mainTableAux.objects.all()

        # Borro todas las tablas auxiliares
        for all in tableAux:

            all.delete()

        for typ in allTypes:

            contStart = 0

            # Creo una tabla auxiliar para cada type
            tableAuxGet = mainTableAux()

            # Obtengo las tablas de dicho rango de acuerdo a ese tipo
            tableAux = mainTable.objects.filter(fecha__date__gte=dateFrom,fecha__date__lte=dateTo,tabTipo=typ)

            # print(len(tableAux))

            for ta in tableAux:

                # print(ta.tabStart)

                contStart = contStart + float(ta.tabStart)

            tableAuxGet.tabTipo = typ   

            print(tableAuxGet.tabTipo)

            tableAuxGet.tabStart = contStart

            print(tableAuxGet.tabStart)

            facturaAuxIngreso = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refCategory__ingreso=True,refType__nombre=typ)
            contIngreso = 0

            for ing in facturaAuxIngreso:
                contIngreso = contIngreso+float(ing.monto)

            tableAuxGet.tabPagos = contIngreso

            print(tableAuxGet.tabPagos)

            facturaAuxEgreso = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refCategory__egreso=True,refType__nombre=typ)
            contEgreso = 0

            for ing in facturaAuxEgreso:
                contEgreso = contEgreso+float(ing.monto)

            tableAuxGet.tabRetiros = contEgreso

            print(tableAuxGet.tabRetiros)

            # print(type(tableAuxGet.tabStart))
            # print(type(contIngreso))
            # print(type(contEgreso))

            tableAuxGet.tabTotal = contStart + float(contIngreso)-float(contEgreso)
            # tableAuxGet.tabTotal = tableAuxGet.tabStart+float(contIngreso)-float(contEgreso)

            print(tableAuxGet.tabTotal)

            tableAuxGet.save()    

        tableAux = mainTableAux.objects.all()  

        contStart = 0
        contPagos = 0
        contRetiros = 0
        contTotal = 0

        for tab in tableAux:

            if tab.tabStart > 0:

                contStart = contStart + tab.tabStart

            if tab.tabPagos > 0:

                contPagos = contPagos + tab.tabPagos
            
            if tab.tabRetiros > 0:

                contRetiros = contRetiros + tab.tabRetiros
        
        contTotal = contStart + contPagos - contRetiros

        allFacturesToPay = factura.objects.filter(refCategory__ingreso=True,refCategory__limite=True)
        allFacturesToCollect = factura.objects.filter(refCategory__egreso=True,refCategory__limite=True)
        
        facturesToPay = len(allFacturesToPay)
        facturesToCollect = len(allFacturesToCollect)

        # print(tableAux)

        # ---------------------------------

        dic = {"dateFrom":dateFrom,"dateTo":dateTo,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"contStart":contStart,"contPagos":contPagos,"contRetiros":contRetiros,"contTotal":contTotal,"tableAux":tableAux,"tod":tod}

        return render(request,"spareapp/contByRange.html",dic)   

    dic = {"tod":tod}

    return render(request,"spareapp/contByRange.html",dic)