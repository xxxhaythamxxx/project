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
from datetime import timedelta
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse
# import numpy as np

# Create your views here.

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
    
    spCart = spareCart.objects.filter(nameUser=request.user.get_username()).values("spareId","nameUser").distinct().order_by("spareId")
    if request.user.get_username() == "":
        spCart = spareCart.objects.filter(nameUser="AnonymousUser").values("spareId","nameUser").distinct()
    dic={"spCart":spCart,"reference":ref,"allVendors":allVendors,"allAtributes":atr2,"atribute":atr,"allDimensions":dim2,"dimension":dim,"allSparesall":allSparesall,"allCategories":allCategories,"allCars":allCars,"onlyManufCars":onlyManufCars,"allEngines":allEngines,"allSpares":allSpares}


    if request.method=="POST":
        list = request.POST.getlist('toAdd')
        delist = request.POST.getlist("toDel")
        # Si es una lista que se envía para guardarla
        if list:
            # cart = spareCart()
            # Si se va a crear un nuevo carrito
            if request.POST.get("cartNumber") == "":
                randomNum = datetime.now().strftime("%Y%m%d%H%M%S")
                # cart = spareCart()
                # cart.save()
                # form = UserRegisterForm(request.POST)
                print("Voy a entrar a list")
                for a in list:
                    cart = spareCart()
                    cart.spareId = randomNum
                    # cart1 = spareCart.objects.get(id=cart.id)
                    # print(cart)
                    cart.spareCode = a
                    # cart1.spareCode.add(a)
                    # Si hay iniciada una sesion
                    if request.user.get_username() != "":
                        username = request.user.get_username()
                        cart.nameUser = username
                        # cart1.nameUser.add(username)
                    # Si no hay iniciada una sesion
                    else:
                        cart.nameUser = "AnonymousUser"
                        # cart1.nameUser.add("User")
                    cart.save()
                    # cart1.add(cart1)
            else:
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

    # Lleno las categorias basicas -------------------------------
    catAux = factCategory.objects.filter(nombre="Factura cobrada")
    if catAux:
        pass
    else:
        catA = factCategory()
        catA.nombre = "Factura cobrada"
        catA.ingreso = True
        catA.save()
    catAux = factCategory.objects.filter(nombre="Mercancia credito pagada")
    if catAux:
        pass
    else:
        catA = factCategory()
        catA.nombre = "Mercancia credito pagada"
        catA.egreso = True
        catA.save()

    tod = datetime.now().date()
    allTypes = factType.objects.all().order_by("nombre")
    editPrueba = False
    contTotal = 0
    tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")
    allFactures = factura.objects.filter(fechaCreado__date=tod) | factura.objects.filter(fechaCobrado=tod)
    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    contTotal = 0
    noIncludeTotal = 0
    noIncludeTotalGasto = 0
    contPagadoCobrado = 0

    for tab in tableAux:

        if tab.tabTipo.include == True:

            if  tab.tabTipo.facCobrada == False and tab.tabTipo.mercPagada == False:

                contTotal = contTotal + tab.tabTotal

        else:

            if  tab.tabTipo.facCobrada == False and tab.tabTipo.mercPagada == False:

                if tab.tabTipo.ingreso == True:

                    noIncludeTotal = noIncludeTotal + tab.tabTotal

                else:

                    noIncludeTotalGasto = noIncludeTotalGasto + tab.tabTotal

        if tab.tabTipo.facCobrada == True:

            contPagadoCobrado = contPagadoCobrado + tab.tabTotal

        if tab.tabTipo.mercPagada == True:

            contPagadoCobrado = contPagadoCobrado - tab.tabTotal
        
    dic = {"contPagadoCobrado":contPagadoCobrado,"noIncludeTotalGasto":noIncludeTotalGasto,"noIncludeTotal":noIncludeTotal,"allFactures":allFactures,"contTotal":contTotal,"editPrueba":editPrueba,"tod":tod,"allTypes":allTypes,"tableAux":tableAux,"facturesToCollect":facturesToCollect,"facturesToPay":facturesToPay}

    return render(request,"spareapp/contDay.html",dic)

def contEntry(request):

    allTypes = factType.objects.all().order_by("nombre").exclude(facCobrada=True).exclude(mercPagada=True).exclude(mercPagar=True).exclude(facCobrar=True).exclude(mercPagar=True)
    allCategories = factCategory.objects.filter(ingreso=True).order_by("nombre").exclude(nombre="Factura cobrada").exclude(nombre="Mercancia credito pagada")
    allCategoriesEntry = factCategory.objects.filter(ingreso=True).order_by("nombre").exclude(nombre="Factura cobrada").exclude(nombre="Mercancia credito pagada")
    allCategoriesSpending = factCategory.objects.filter(egreso=True).order_by("nombre").exclude(nombre="Factura cobrada").exclude(nombre="Mercancia credito pagada")
    allCustomers = persona.objects.all()
    tod = datetime.now().date()
    actualAux=datetime.now().date()
    actualDay=str(actualAux.year)+"-"+str('%02d' % actualAux.month)+"-"+str('%02d' % actualAux.day)
    deadlineDefault=(datetime.now()+timedelta(days=30)).date()
    actual=str(deadlineDefault.year)+"-"+str('%02d' % deadlineDefault.month)+"-"+str('%02d' % deadlineDefault.day)
    noIncludeTotal = 0
    noIncludeTotalGasto = 0
    contPagadoCobrado = 0

    dic = {"actualDay":actualDay,"actual":actual,"allCategoriesSpending":allCategoriesSpending,"allCategoriesEntry":allCategoriesEntry,"allCustomers":allCustomers,"allTypes":allTypes,"allCategories":allCategories}

    if request.method == "POST":

        actualAux=datetime.now().date()
        actualDay=str(actualAux.year)+"-"+str('%02d' % actualAux.month)+"-"+str('%02d' % actualAux.day)

        factAux = factura()

        contFecha = request.POST.get("contFechaCreado")
        factAux.fechaCreado=contFecha

        tod=contFecha

        contNombre = request.POST.get("contNombre")
        nomAux = persona.objects.get(id=contNombre)
        factAux.refPersona = nomAux

        if request.POST.get("contNumFac"):
            contNumFac = request.POST.get("contNumFac")
            factAux.num = contNumFac

        contTypeIng = request.POST.get("contTypeIng")
        typeAux = factType.objects.get(id=contTypeIng)
        factAux.refType = typeAux

        contCatIng = request.POST.get("contCatIng")
        catAux = factCategory.objects.filter(id=contCatIng)

        for cat in catAux:
            if cat.limite == True:
                factAux.pendiente = True

        catAux = factCategory.objects.get(id=contCatIng)
        factAux.refCategory = catAux

        if request.POST.get("contFechaTope") != "":
            contFechaTope = request.POST.get("contFechaTope")
            factAux.fechaTope = contFechaTope

        contMonto = request.POST.get("contMonto")
        factAux.monto = contMonto

        if request.POST.get("contItbm") == "":
            contIva = float(0)
        else:
            contIva = request.POST.get("contItbm")
        factAux.iva = contIva

        contTotal = request.POST.get("contTotal")
        factAux.total = contTotal

        factAux.note = request.POST.get("contNota")

        factAux.save()

        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")

        allTypes = factType.objects.all().order_by("nombre")

        for ty in allTypes:

            if  tableAux:

                tableAuxType = mainTable.objects.get(fecha__date=tod,tabTipo__nombre=ty)
            
            else:

                tableAuxType = mainTable()
                tableAuxType.fecha=tod
                tableAuxType.tabTipo = ty
                tableAuxType.tabTotal = 0

            allFacturesCash = factura.objects.filter(fechaCreado__date=tod,refType=ty).order_by("fechaCreado")
            
            acum = 0

            for fac in allFacturesCash:

                acum = acum + fac.total

            tableAuxType.tabTotal = float(acum)

            if ty.facCobrar == True:

                allFacturesPay = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")

                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total
                
                tableAuxType.tabTotal = float(acum2)
            
            if ty.mercPagar == True:

                allFacturesPay = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")

                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total
                
                tableAuxType.tabTotal = float(acum2)

            if ty.facCobrada == True:

                allFacturesPay = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")

                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total
                
                tableAuxType.tabTotal = float(acum2)

            if ty.mercPagada == True:

                allFacturesPay = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")

                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total
                
                tableAuxType.tabTotal = float(acum2)

            if ty.visa == True:

                allFacturesVisa = factura.objects.filter(fechaCreado__date=tod,refType__nombre=ty).order_by("fechaCreado")

                acum = 0

                for fac in allFacturesVisa:

                    if fac.monto == fac.total:

                        itbm = 0
                        
                    else:

                        itbm = fac.iva

                    retencion = float(itbm/2)
                    interes = float(fac.total)*0.0225*1.07

                    acum = acum + (fac.total)
                    
                tableAuxType.tabTotal = float(acum)
            
            if ty.clave == True:

                allFacturesClave = factura.objects.filter(fechaCreado__date=tod,refType__nombre=ty).order_by("fechaCreado")

                acum = 0

                for fac in allFacturesClave:

                    if fac.monto == fac.total:

                        itbm = 0
                        
                    else:

                        itbm = fac.iva

                    retencion = float(itbm/2)
                    interes = float(fac.total)*0.02*1.07

                    acum = acum + (fac.total)

                tableAuxType.tabTotal = float(acum)

            tableAuxType.save()
        
        allTypes = factType.objects.all().order_by("nombre").exclude(facCobrada=True).exclude(mercPagada=True).exclude(mercPagar=True)

        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")

        if request.POST.get("entryOption")=="otro":

            tod = datetime.now().date()
            allTypes = factType.objects.all().order_by("nombre")
            contTotal = 0
            tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")
            allFactures = factura.objects.filter(fechaCreado__date=tod) | factura.objects.filter(fechaCobrado=tod)
            allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
            allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
            facturesToCollect = len(allFacturesToPay)
            facturesToPay = len(allFacturesToCollect)

            contTotal = 0
            noIncludeTotal = 0
            noIncludeTotalGasto = 0
            contPagadoCobrado = 0

            for tab in tableAux:

                if tab.tabTipo.include == True:

                    if  tab.tabTipo.facCobrada == False and tab.tabTipo.mercPagada == False:

                        contTotal = contTotal + tab.tabTotal

                else:

                    if  tab.tabTipo.facCobrada == False and tab.tabTipo.mercPagada == False:

                        if tab.tabTipo.ingreso == True:

                            noIncludeTotal = noIncludeTotal + tab.tabTotal

                        else:

                            noIncludeTotalGasto = noIncludeTotalGasto + tab.tabTotal

                if tab.tabTipo.facCobrada == True:

                    contPagadoCobrado = contPagadoCobrado + tab.tabTotal

                if tab.tabTipo.mercPagada == True:

                    contPagadoCobrado = contPagadoCobrado - tab.tabTotal
                    
            dic = {"contPagadoCobrado":contPagadoCobrado,"noIncludeTotalGasto":noIncludeTotalGasto,"noIncludeTotal":noIncludeTotal,"allFactures":allFactures,"contTotal":contTotal,"tod":tod,"allTypes":allTypes,"tableAux":tableAux,"facturesToCollect":facturesToCollect,"facturesToPay":facturesToPay}

            return render(request,"spareapp/contDay.html",dic)

        dic = {"contPagadoCobrado":contPagadoCobrado,"noIncludeTotal":noIncludeTotal,"noIncludeTotalGasto":noIncludeTotalGasto,"actualDay":actualDay,"actual":actual,"tableAux":tableAux,"allCustomers":allCustomers,"tod":tod,"allTypes":allTypes,"allCategories":allCategories}
    
    return render(request,"spareapp/contEntry.html",dic)

def contType(request,val,val2):

    allTypes = factType.objects.all().order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)
    todos = factType.objects.all()
    tod = datetime.now().date()
    montoTotal = 0
    itbmTotal = 0
    totalTotal = 0

    allFacturesVal = factura.objects.filter(fechaCreado__date=tod,refType__nombre=val)
    typeAux = factType.objects.get(nombre=val)

    if val2 != "today":

        tod = val2

        for t in todos:
            s=t.nombre
            if s:
                out = s.translate(str.maketrans('', '', '/'))
                if val.upper()==out.upper():
                    allFacturesVal = factura.objects.filter(fechaCreado__date=tod,refType__nombre=s)

    if typeAux.facCobrada == True:

        allFacturesVal = factura.objects.filter(refCategory__ingreso=True,fechaCobrado=tod,refCategory__nombre="Factura cobrada")

    if typeAux.mercPagada == True:

        allFacturesVal = factura.objects.filter(refCategory__egreso=True,fechaCobrado=tod,refCategory__nombre="Mercancia credito pagada")

    if typeAux.facCobrar == True:

        allFacturesVal = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__ingreso=True)
        allTypes = factType.objects.filter(ingreso=True).order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)

    if typeAux.mercPagar == True:

        allFacturesVal = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__egreso=True)
        allTypes = factType.objects.filter(gasto=True).order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)

    itbm7 = {}
    
    for fac in allFacturesVal:

        montoTotal = montoTotal + fac.monto
        itbmTotal = itbmTotal + float(fac.iva)
        totalTotal = totalTotal + fac.total

    typeDate = val2

    dic = {"allTypes":allTypes,"montoTotal":montoTotal,"itbmTotal":itbmTotal,"totalTotal":totalTotal,"itbm7":itbm7,"typeDate":typeDate,"val2":val2,"allFacturesVal":allFacturesVal,"val":val}

    return render(request,"spareapp/contType.html",dic)

def contTypeTarjeta(request,val,val2):

    tod = datetime.now().date()
    typeAux = factType.objects.get(nombre=val)

    montoTotal = 0
    itbmTotal = 0
    totalTotal = 0
    interesTotal = 0
    retencionTotal = 0
    netoTotal = 0

    allFacturesVal = factura.objects.filter(fechaCreado__date=tod,refType__nombre=val)

    if val2 != "today":

        tod = val2

        allFacturesVal = factura.objects.filter(fechaCreado__date=tod,refType__nombre=val)

    itbm7 = {}

    for fac in allFacturesVal:

        itbmMonto = float(fac.iva)

        if typeAux.visa == True:

            neto = float((fac.total)-(float(fac.total)*0.0225*1.07)-(float(itbmMonto)/2))
            interesTotal = interesTotal + float(float(fac.total)*0.0225*1.07)
            retencionTotal = retencionTotal + float(itbmMonto/2)
            netoTotal = netoTotal + neto
            itbm7[fac.id] = [float(itbmMonto),float(float(fac.total)*0.0225*1.07),float(float(itbmMonto)/2),float(neto)]

        else:

            neto = float((fac.total)-(float(fac.total)*0.02*1.07)-(float(itbmMonto)/2))
            interesTotal = interesTotal + float(float(fac.total)*0.02*1.07)
            retencionTotal = retencionTotal + float(itbmMonto/2)
            netoTotal = netoTotal + neto
            itbm7[fac.id] = [float(fac.monto)*0.07,float(float(fac.total)*0.02*1.07),float(float(itbmMonto)/2),float(neto)]

    for fac in allFacturesVal:

        # if fac.refCategory.ingreso == True:

        montoTotal = montoTotal + fac.monto
        itbmTotal = itbmTotal + float(fac.iva)
        totalTotal = totalTotal + fac.total

    typeDate = val2

    dic = {"netoTotal":netoTotal,"retencionTotal":retencionTotal,"interesTotal":interesTotal,"montoTotal":montoTotal,"itbmTotal":itbmTotal,"totalTotal":totalTotal,"itbm7":itbm7,"typeDate":typeDate,"val2":val2,"allFacturesVal":allFacturesVal,"val":val}

    return render(request,"spareapp/contTypeTarjeta.html",dic)

def contTypeRange(request,val,val2,val3):

    allTypes = factType.objects.all().order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)
    tod = datetime.now().date()
    typeAux = factType.objects.get(nombre=val)

    montoTotal = 0
    itbmTotal = 0
    totalTotal = 0

    todos = factType.objects.all()

    for t in todos:
            s=t.nombre
            if s:
                out = s.translate(str.maketrans('', '', '/'))
                if val.upper()==out.upper():
                    allFacturesVal = factura.objects.filter(refType__nombre=s,fechaCreado__date__gte=val2,fechaCreado__date__lte=val3)

    if typeAux.facCobrada == True:

        allFacturesVal = factura.objects.filter(refCategory__ingreso=True,fechaCobrado__lte=val3,fechaCobrado__gte=val2,refCategory__nombre="Factura cobrada")

    if typeAux.mercPagada == True:

        allFacturesVal = factura.objects.filter(refCategory__egreso=True,fechaCobrado__lte=val3,fechaCobrado__gte=val2,refCategory__nombre="Mercancia credito pagada")

    if typeAux.facCobrar == True:

        allFacturesVal = factura.objects.filter(fechaCreado__date__lte=val3,fechaCreado__date__gte=val2,pendiente=True,refCategory__ingreso=True)
        allTypes = factType.objects.filter(ingreso=True).order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)

    if typeAux.mercPagar == True:

        allFacturesVal = factura.objects.filter(fechaCreado__date__lte=val3,fechaCreado__date__gte=val2,pendiente=True,refCategory__egreso=True)
        allTypes = factType.objects.filter(gasto=True).order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)


    itbm7 = {}

    for fac in allFacturesVal:

        if fac.refCategory.ingreso == True:

            if fac.monto == fac.total:

                itbm7[fac.id] = float(0)

            else:

                itbm7[fac.id] = float(fac.monto)*0.07
    
    for fac in allFacturesVal:

        montoTotal = montoTotal + fac.monto
        itbmTotal = itbmTotal + float(fac.iva)
        totalTotal = totalTotal + fac.total

    typeDate = "From "+val2+", to "+val3

    dic = {"allTypes":allTypes,"totalTotal":totalTotal,"itbmTotal":itbmTotal,"montoTotal":montoTotal,"itbm7":itbm7,"typeDate":typeDate,"val3":val3,"val2":val2,"allFacturesVal":allFacturesVal,"val":val}

    return render(request,"spareapp/contType.html",dic)

def contTypeRangeTarjeta(request,val,val2,val3):

    tod = datetime.now().date()
    typeAux = factType.objects.get(nombre=val)

    montoTotal = 0
    itbmTotal = 0
    totalTotal = 0
    interesTotal = 0
    retencionTotal = 0
    netoTotal = 0

    allFacturesVal = factura.objects.filter(refType__nombre=val,fechaCreado__date__gte=val2,fechaCreado__date__lte=val3)

    itbm7 = {}

    netoTotal = 0

    for fac in allFacturesVal:

        if fac.monto == fac.total:

            itbmMonto = float(0)

        else:

            itbmMonto = float(fac.monto)*0.07

        if typeAux.visa == True:

            neto = float((fac.total)-(float(fac.total)*0.0225*1.07)-(float(itbmMonto)/2))
            interesTotal = interesTotal + float(float(fac.total)*0.0225*1.07)
            retencionTotal = retencionTotal + float(itbmMonto/2)
            netoTotal = netoTotal + neto
            itbm7[fac.id] = [float(itbmMonto),float(float(fac.total)*0.0225*1.07),float(float(itbmMonto)/2),float(neto)]

        else:

            neto = float((fac.total)-(float(fac.total)*0.02*1.07)-(float(itbmMonto)/2))
            interesTotal = interesTotal + float(float(fac.total)*0.02*1.07)
            retencionTotal = retencionTotal + float(itbmMonto/2)
            netoTotal = netoTotal + neto
            itbm7[fac.id] = [float(fac.monto)*0.07,float(float(fac.total)*0.02*1.07),float(float(itbmMonto)/2),float(neto)]

    for fac in allFacturesVal:

        montoTotal = montoTotal + fac.monto
        if fac.monto == fac.total:
            itbmTotal = itbmTotal + float(0)
        else:
            itbmTotal = itbmTotal + float(fac.monto)*0.07
        totalTotal = totalTotal + fac.total

    typeDate = "From "+val2+", to "+val3

    dic = {"netoTotal":netoTotal,"retencionTotal":retencionTotal,"interesTotal":interesTotal,"totalTotal":totalTotal,"itbmTotal":itbmTotal,"montoTotal":montoTotal,"itbm7":itbm7,"typeDate":typeDate,"val3":val3,"val2":val2,"allFacturesVal":allFacturesVal,"val":val}

    return render(request,"spareapp/contTypeTarjeta.html",dic)

def contToCollect(request):

    allFacturesPay = factura.objects.filter(pendiente=True,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")
    allTypes = factType.objects.filter(ingreso=True).order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)
    
    deadlineDic = {}

    for all in allFacturesPay:

        deadline = all.fechaTope - all.fechaCreado.date()
        deadline = deadline.days
        deadlineDic[all.id] = deadline

    acum = 0
    acum2 = 0

    for fac in allFacturesPay:

        acum = acum + fac.monto
        acum2 = acum2 + fac.total

    tod = datetime.now()

    dic = {"allTypes":allTypes,"deadlineDic":deadlineDic,"allFacturesPay":allFacturesPay,"totalTotal":acum2,"montoTotal":acum}

    return render(request,"spareapp/contToCollect.html",dic)

def contToPay(request):

    allFacturesPay = factura.objects.filter(pendiente=True,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")
    allTypes = factType.objects.filter(gasto=True).order_by("nombre").exclude(facCobrada=True).exclude(facCobrar=True).exclude(mercPagada=True).exclude(mercPagar=True)

    deadlineDic = {}

    for all in allFacturesPay:

        deadline = all.fechaTope - all.fechaCreado.date()
        deadline = deadline.days
        deadlineDic[all.id] = deadline

    acum = 0
    acum2 = 0

    for fac in allFacturesPay:

        acum = acum + fac.monto
        acum2 = acum2 + fac.total

    tod = datetime.now()

    dic = {"allTypes":allTypes,"deadlineDic":deadlineDic,"allFacturesPay":allFacturesPay,"totalTotal":acum2,"montoTotal":acum}

    return render(request,"spareapp/contToPay.html",dic)

def contAdmin(request):

    return render(request,"spareapp/contAdmin.html")

def contAddType(request):

    tod = datetime.now().date()

    if request.method == "POST":

        typeNombre = request.POST.get("typeNombre")

        if typeNombre != "":

            listType = factType.objects.filter(nombre=typeNombre)

            if (listType):

                print("Ya existe éste type")

            else:

                factTypeAux = factType()
                factTypeAux.nombre = typeNombre
                if request.POST.get("typeInclude") == "on":
                    factTypeAux.include = True
                else:
                    factTypeAux.include = False
                factTypeAux.save()

                tableAux = mainTable.objects.filter(fecha__date=tod)

                if tableAux:

                    print("Hay tabla hoy")

                    tableNew = mainTable()
                    tableNew.fecha=tod
                    typeAux = factType.objects.get(nombre=typeNombre)
                    tableNew.tabTipo=typeAux
                    tableNew.tabTotal=0
                    tableNew.save()

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
    facAux = ""
    deleteAux = {}

    for ty in allTypes:

        facAux = factura.objects.filter(refType=ty)
        if facAux:
            deleteAux[ty.id] = "on"
        else:
            deleteAux[ty.id] = "off"

    if request.method == "POST":

        for cat in request.POST.getlist("typId"):

            singleType = factType.objects.get(id=cat)

            if request.POST.get("typNom"+cat):

                singleType.nombre = request.POST.get("typNom"+cat)

            if request.POST.get("facCobrar"+cat):

                singleType.facCobrar = True
            
            else:

                singleType.facCobrar = False

            if request.POST.get("facCobrada"+cat):

                singleType.facCobrada = True
            
            else:

                singleType.facCobrada = False

            if request.POST.get("mercPagar"+cat):

                singleType.mercPagar = True
            
            else:

                singleType.mercPagar = False

            if request.POST.get("mercPagada"+cat):

                singleType.mercPagada = True
            
            else:

                singleType.mercPagada = False

            if request.POST.get("visa"+cat):

                singleType.visa = True
            
            else:

                singleType.visa = False

            if request.POST.get("clave"+cat):

                singleType.clave = True
            
            else:

                singleType.clave = False

            if request.POST.get("typInclude"+cat):

                singleType.include = True
            
            else:

                singleType.include = False

            if request.POST.get("ingreso"+cat):

                singleType.ingreso = True
                singleType.gasto = False
            
            else:

                singleType.ingreso = False
                singleType.gasto = True
                
            singleType.save()

    allTypes = factType.objects.all().order_by("nombre")

    dic = {"deleteAux":deleteAux,"allTypes":allTypes}

    return render(request,"spareapp/contListType.html",dic)

def contListCategory(request):

    allCategories = factCategory.objects.all().order_by("nombre")
    deleteAux = {}
    facAux = ""

    for cat in allCategories:

        facAux = factura.objects.filter(refCategory=cat)
        if facAux:
            deleteAux[cat.id] = "on"
        else:
            deleteAux[cat.id] = "off"

    if request.method == "POST":

        allCategories = factCategory.objects.all().order_by("nombre")

        for cat in request.POST.getlist("catId"):

            singleCategory = factCategory.objects.get(id=cat)

            if request.POST.get("contNom"+cat):

                singleCategory.nombre = request.POST.get("contNom"+cat)

            if request.POST.get("catEntry"+cat):

                singleCategory.ingreso = True
                singleCategory.egreso = False
            
            else:

                singleCategory.ingreso = False
                singleCategory.egreso = True

            if request.POST.get("catExpiration"+cat):
                singleCategory.limite = True
            else:
                singleCategory.limite = False
            
            singleCategory.save()

    # allCategories = factCategory.objects.all().order_by("nombre")

    dic = {"deleteAux":deleteAux,"allCategories":allCategories}

    return render(request,"spareapp/contListCategory.html",dic)

def contDeleteType(request,val):

    singleType = factType.objects.get(id=val)

    singleType.delete()

    allTypes = factType.objects.all()

    dic = {"allTypes":allTypes}

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def contDeleteCategory(request,val):

    singleCategory = factCategory.objects.get(id=val)

    singleCategory.delete()

    allCategories = factCategory.objects.all().order_by("nombre")

    dic = {"allCategories":allCategories}

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def contEditType(request,val):

    allTypes = factType.objects.all().order_by("nombre")

    singleType = factType.objects.filter(id=val)

    if request.method == "POST":

        singleType = factType.objects.get(id=val)
        singleType.nombre = request.POST.get("typeNombre")
        if request.POST.get("typeInclude"):
            singleType.include = True
        else:
            singleType.include = False
        singleType.save()

        dic = {"singleType":singleType,"allTypes":allTypes}

        return render(request,"spareapp/contListType.html",dic)

    dic = {"singleType":singleType,"allTypes":allTypes}

    return render(request,"spareapp/contEditType.html",dic)

def contEditCategory(request,val):

    allCategories = factCategory.objects.all().order_by("nombre")

    singleCategory = factCategory.objects.filter(id=val)

    if request.method == "POST":

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

    editPrueba = False

    tod = request.POST.get("searchDate")

    if request.POST.get("adjustButton"):

        editPrueba = True

    if request.POST.get("acceptButton"):

        allTypes = factType.objects.all().order_by("nombre")

        for ty in allTypes:

            tableAuxTy = mainTable.objects.get(fecha__date=tod,tabTipo=ty)

            if tableAuxTy.tabTipo.manual == True:

                tableAuxTy.tabTotal = request.POST.get(str(ty).replace(" ", "")+"Total")
            
            tableAuxTy.save()

    tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")

    contTotal = 0
    noIncludeTotal = 0
    noIncludeTotalGasto = 0
    contPagadoCobrado = 0

    for tab in tableAux:

        if tab.tabTipo.include == True:

            if  tab.tabTipo.facCobrada == False and tab.tabTipo.mercPagada == False:

                contTotal = contTotal + tab.tabTotal

        else:

            if  tab.tabTipo.facCobrada == False and tab.tabTipo.mercPagada == False:

                if tab.tabTipo.ingreso == True:

                    noIncludeTotal = noIncludeTotal + tab.tabTotal

                else:

                    noIncludeTotalGasto = noIncludeTotalGasto + tab.tabTotal

        if tab.tabTipo.facCobrada == True:

            contPagadoCobrado = contPagadoCobrado + tab.tabTotal

        if tab.tabTipo.mercPagada == True:

            contPagadoCobrado = contPagadoCobrado - tab.tabTotal
                

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"contPagadoCobrado":contPagadoCobrado,"noIncludeTotalGasto":noIncludeTotalGasto,"noIncludeTotal":noIncludeTotal,"editPrueba":editPrueba,"contTotal":contTotal,"tod":tod,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect}

    return render(request,"spareapp/contDay.html",dic)

def contByRange(request):

    tod = request.POST.get("searchDate")

    if request.method == "POST":

        dateFrom = request.POST.get("searchDateFrom")
        dateTo = request.POST.get("searchDateTo")
        allTypes = factType.objects.all()

        # Inicializo todas las facturas por el rango deseado
        allFacturesRange = ""

        if dateFrom and dateTo:
            allFacturesRange = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo)

        tableAux = mainTableAux.objects.all()

        for all in tableAux:

            all.delete()

        contTotal = 0
        noIncludeTotal = 0
        noIncludeTotalGasto = 0
        contPagadoCobrado = 0

        for typ in allTypes:

            tableAuxGet = mainTableAux()

            tableAuxGet.tabTipo = typ  

            tableAux = mainTable.objects.filter(fecha__date__gte=dateFrom,fecha__date__lte=dateTo,tabTipo=typ)

            contSubTotal = 0

            for ta in tableAux:

                if typ.include == True:

                    if  typ.facCobrada == False and typ.mercPagada == False:

                        contTotal = float(contTotal) + float(ta.tabTotal)

                else:

                    if  typ.facCobrada == False and typ.mercPagada == False:

                        if typ.ingreso == True:

                            noIncludeTotal = noIncludeTotal + float(ta.tabTotal)

                        else:

                            noIncludeTotalGasto = noIncludeTotalGasto + float(ta.tabTotal)

                if ta.tabTipo.facCobrada == True:

                    contPagadoCobrado = contPagadoCobrado + ta.tabTotal

                if ta.tabTipo.mercPagada == True:

                    contPagadoCobrado = contPagadoCobrado - ta.tabTotal

                contSubTotal = float(contSubTotal) + float(ta.tabTotal)

            tableAuxGet.tabTotal = contSubTotal

            tableAuxGet.save()    

        tableAux = mainTableAux.objects.all().order_by("tabTipo__nombre")  

        allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
        allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
        
        facturesToCollect = len(allFacturesToPay)
        facturesToPay = len(allFacturesToCollect)

        dic = {"contPagadoCobrado":contPagadoCobrado,"noIncludeTotalGasto":noIncludeTotalGasto,"noIncludeTotal":noIncludeTotal,"tod":tod,"dateFrom":dateFrom,"dateTo":dateTo,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"contTotal":contTotal,"tableAux":tableAux,"tod":tod}

    return render(request,"spareapp/contByRange.html",dic)

def contCollectFac(request,val):

    acum = 0

    tod = datetime.now().date()
    allTypes = factType.objects.all().order_by("nombre")
    factAux = factura.objects.filter(id=val)
    tableAux = mainTable.objects.filter(fecha__date=tod)

    # typeAux = request.POST.get("contTypeIng")
    typeAux = factType.objects.get(facCobrada=True)
    # typeAux = factType.objects.get(id=typeAux)

    if factAux:

        factErase = factura.objects.get(id=val)
        factErase.pendiente = False
        factErase.fechaCobrado = tod
        factErase.save()

        tablePast = mainTable.objects.filter(fecha__date=factErase.fechaCreado)

        # Borro la factura pendiente en el pasado
        for ty in allTypes:

            aux = mainTable.objects.get(tabTipo=ty,fecha__date=factErase.fechaCreado)

            if ty.facCobrar == True:

                allFacturesToCollect = factura.objects.filter(fechaCreado__date=factErase.fechaCreado,pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
                totalFact = 0

                for fac in allFacturesToCollect:

                    totalFact = totalFact + float(fac.total)

                aux.tabTotal = totalFact

            aux.save()

        reciboCollect = factura()
        reciboCollect.fechaCreado=tod
        reciboCollect.num = factErase.num
        reciboCollect.refPersona = factErase.refPersona
        reciboCollect.refType = typeAux
        auxCat = factCategory.objects.get(nombre="Factura cobrada")
        reciboCollect.refCategory = auxCat
        reciboCollect.fechaTope = factErase.fechaTope
        reciboCollect.fechaCobrado = tod
        reciboCollect.iva = factErase.iva
        reciboCollect.monto = factErase.monto
        reciboCollect.total = factErase.total
        reciboCollect.note=request.POST.get("contNota")
        reciboCollect.pendiente = False
        reciboCollect.save()

        if tableAux:

            for ty in allTypes:

                aux = mainTable.objects.get(tabTipo=ty,fecha__date=tod)

                allFacturesCash = factura.objects.filter(fechaCreado__date=tod,refType=ty).order_by("fechaCreado")
                acum = 0
                for fac in allFacturesCash:
                    acum = acum + fac.total
                
                aux.tabTotal = float(acum)

                if ty.mercPagar == True:

                    allFacturesToCollect = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__egreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    aux.tabTotal = totalFact
                
                if ty.mercPagada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__egreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    aux.tabTotal = totalFact

                if ty.facCobrada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__ingreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)

                    aux.tabTotal = totalFact

                if ty.facCobrar == True:

                    allFacturesToCollect = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__ingreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)

                    aux.tabTotal = totalFact

                aux.save()

        else:

            for ty in allTypes:

                tableNew = mainTable()
                tableNew.fecha = tod
                tableNew.tabTipo = ty

                allFacturesCash = factura.objects.filter(fechaCreado__date=tod,refType=ty).order_by("fechaCreado")
                acum = 0
                for fac in allFacturesCash:
                    acum = acum + fac.total
                
                tableNew.tabTotal = float(acum)

                if ty.mercPagar == True:

                    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    tableNew.tabTotal = totalFact
                
                if ty.mercPagada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__egreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    tableNew.tabTotal = totalFact

                if ty.facCobrada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__ingreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    tableNew.tabTotal = totalFact

                tableNew.save()

    tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo")

    contTotal = 0

    for tab in tableAux:

        if tab.tabTipo.facCobrada != True:

            contTotal = contTotal + tab.tabTotal

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    editPrueba = False

    dic = {"contTotal":contTotal,"factAux":factAux,"tod":tod,"allTypes":allTypes,"editPrueba":editPrueba,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect}

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def contPayFac(request,val):

    acum = 0

    tod = datetime.now().date()
    allTypes = factType.objects.all().order_by("nombre")
    factAux = factura.objects.filter(id=val)
    tableAux = mainTable.objects.filter(fecha__date=tod)

    typeAux = request.POST.get("contTypeIng")
    typeAux = factType.objects.get(id=typeAux)

    if factAux:

        factErase = factura.objects.get(id=val)
        factErase.pendiente = False
        factErase.fechaCobrado = tod
        factErase.save()

        for ty in allTypes:

            aux = mainTable.objects.get(tabTipo=ty,fecha__date=factErase.fechaCreado)

            if ty.mercPagar == True:

                allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)

                totalFact = 0

                for fac in allFacturesToCollect:

                    totalFact = totalFact + float(fac.total)

                aux.tabTotal = totalFact

            aux.save()

        reciboCollect = factura()
        reciboCollect.fechaCreado = tod
        reciboCollect.num = factErase.num
        reciboCollect.refPersona = factErase.refPersona
        reciboCollect.refType = typeAux
        auxCat = factCategory.objects.get(nombre="Mercancia credito pagada")
        reciboCollect.refCategory = auxCat
        reciboCollect.fechaTope = factErase.fechaTope
        reciboCollect.fechaCobrado = tod
        reciboCollect.iva = factErase.iva
        reciboCollect.monto = factErase.monto
        reciboCollect.note = request.POST.get("contNota")
        reciboCollect.total = factErase.total
        reciboCollect.pendiente = False
        reciboCollect.save()

        if tableAux:

            for ty in allTypes:

                aux = mainTable.objects.get(tabTipo=ty,fecha__date=tod)

                allFacturesCash = factura.objects.filter(fechaCreado__date=tod,refType=ty).order_by("fechaCreado")
                acum = 0
                for fac in allFacturesCash:
                    acum = acum + fac.total
                aux.tabTotal = float(acum)

                if ty.facCobrar == True:

                    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    aux.tabTotal = totalFact
                
                if ty.facCobrada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__ingreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    aux.tabTotal = totalFact

                if ty.mercPagada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__egreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)

                    aux.tabTotal = totalFact

                if ty.mercPagar == True:

                    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)

                    aux.tabTotal = totalFact

                aux.save()

        else:

            for ty in allTypes:

                tableNew = mainTable()
                tableNew.fecha = tod
                tableNew.tabTipo = ty

                allFacturesCash = factura.objects.filter(fechaCreado__date=tod,refType=ty).order_by("fechaCreado")
                acum = 0
                for fac in allFacturesCash:
                    acum = acum + fac.total
                tableNew.tabTotal = float(acum)

                if ty.facCobrar == True:

                    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    tableNew.tabTotal = totalFact
                
                if ty.facCobrada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__ingreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    tableNew.tabTotal = totalFact

                if ty.mercPagada == True:

                    allFacturesToCollect = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__egreso=True,refCategory__limite=True)

                    totalFact = 0

                    for fac in allFacturesToCollect:

                        totalFact = totalFact + float(fac.total)
                    
                    tableNew.tabTotal = totalFact

                tableNew.save()

    tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo")

    contTotal = 0

    for tab in tableAux:

        if tab.tabTipo.mercPagada != True:

            contTotal = contTotal + tab.tabTotal

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    editPrueba = False

    dic = {"contTotal":contTotal,"factAux":factAux,"tod":tod,"allTypes":allTypes,"editPrueba":editPrueba,"tableAux":tableAux,"allFacturesToPay":allFacturesToPay,"allFacturesToCollect":allFacturesToCollect,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect}

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # --------------------------------

def contAddPerson(request):

    if request.method == "POST":

        nombreaux = request.POST.get("custName")
        identificacionaux = request.POST.get("custId")

        personProbar = persona.objects.filter(nombre=nombreaux,documento=identificacionaux)

        if personProbar:

            print("Ya existe")

        else:

            personAux = persona()
            personAux.nombre = nombreaux
            personAux.documento = identificacionaux
            personAux.save()

            personLast = persona.objects.filter(id=personAux.id)
            lastPerson = list(personLast.values())
            
            return JsonResponse({'lastPerson':lastPerson})

    return render(request,"spareapp/contDay.html")

def accountStat(request):

    allCustomers = persona.objects.all()
    cont = 0
    pos = 0
    balance = {}
    balanceTotal = 0
    factureName = None
    dayFrom = ""
    dayTo = ""

    if request.method == "POST":

        auxNombre = request.POST.get("contNombre")
        factureName = factura.objects.filter(refPersona__id=auxNombre).order_by("fechaCreado","id")
        if factureName:
            dayFrom = factureName[0].fechaCreado.date()
            dayTo = factureName[len(factureName)-1].fechaCreado.date()
        cont = 0
        
        for fac in factureName:

            if fac.refCategory.ingreso:

                cont = cont

                if fac.refType.facCobrar==True:

                    cont = cont + fac.total
                
                if fac.refCategory.nombre=="Factura cobrada":

                    cont = cont - fac.total
            
            else:

                cont = cont

                if fac.refType.mercPagar==True:

                    cont = cont - fac.total
                
                if fac.refCategory.nombre=="Mercancia credito pagada":

                    cont = cont + fac.total

            if fac.pendiente == True and  fac.refType.gasto == True:
                balance[fac.id] = [cont,fac.total*(-1)]
            else:
                balance[fac.id] = [cont,fac.total]

        balanceTotal = cont

        factureName = factura.objects.filter(refPersona__id=auxNombre).order_by("fechaCreado","id")

        if request.POST.get("search") == "balance":


            for key in balance:

                if balance[key]==0:
                    pos = key
            
            facActAux = factura.objects.filter(id=pos)

            if facActAux:
            
                facAct = factura.objects.get(id=pos)
                factureName = factura.objects.filter(id__gte=facAct.id,fechaCreado__gte=facAct.fechaCreado,refPersona__id=auxNombre).order_by("fechaCreado","id")
            
            else:

                factureName = None

        if request.POST.get("search") == "month":

            mes = datetime.now().date().month
            date_today = datetime.now()
            dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
            dateFrom = dateFrom.date()

            mes = datetime.now().date().month
            dayFrom = dateFrom
            dayTo = datetime.now().date()
            anio = datetime.now().date().year
            factureName = factura.objects.filter(fechaCreado__month=mes,fechaCreado__year=anio,refPersona__id=auxNombre).order_by("fechaCreado")

        if request.POST.get("search") == "range":

            dateFrom = request.POST.get("searchDateFrom")
            dateTo = request.POST.get("searchDateTo")

            fecha_from = datetime.strptime(dateFrom, '%Y-%m-%d')
            fecha_to = datetime.strptime(dateTo, '%Y-%m-%d')

            dayFrom = fecha_from.date()
            dayTo = fecha_to.date()

            if dateFrom and dateTo:
                
                factureName = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refPersona__id=auxNombre).order_by("fechaCreado")
    
    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"dayFrom":dayFrom,"dayTo":dayTo,"balanceTotal":balanceTotal,"balance":balance,"allCustomers":allCustomers,"factureName":factureName}

    return render(request,"spareapp/accountStat.html",dic)

def contLastMonth(request):

    tod = datetime.now().date()
    mes = datetime.now().date().month
    anio = datetime.now().date().year
    if mes == 1:
        mes = 12
        anio = anio - 1
    else:
        mes = mes - 1
    editPrueba = False
    allTypes = factType.objects.all().order_by("nombre")
    tableAux = mainTableAux.objects.all()

    date_today = datetime.now()
    dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
    dateFrom = dateFrom.date()

    now = datetime.now()
    start_month = datetime(now.year, now.month-1, 1)
    date_on_next_month = start_month + timedelta(35)
    start_next_month = datetime(date_on_next_month.year, date_on_next_month.month, 1)
    dateTo = start_next_month - timedelta(1)
    dateTo = dateTo.date()

    for all in tableAux:

        all.delete()

    contTotal = 0
    noIncludeTotal = 0
    noIncludeTotalGasto = 0
    contPagadoCobrado = 0

    for typ in allTypes:

        tableAuxGet = mainTableAux()
        tableAuxGet.tabTipo = typ
        tableAux = mainTable.objects.filter(tabTipo=typ,fecha__date__month=mes,fecha__date__year=anio)
        cont = 0

        for tab in tableAux:

            cont = cont + float(tab.tabTotal)

            if typ.include == True:

                if  typ.facCobrada == False and typ.mercPagada == False:

                    contTotal = float(contTotal) + float(tab.tabTotal)

            else:

                if  typ.facCobrada == False and typ.mercPagada == False:

                    if typ.ingreso == True:

                        noIncludeTotal = noIncludeTotal + float(tab.tabTotal)

                    else:

                        noIncludeTotalGasto = noIncludeTotalGasto + float(tab.tabTotal)

            if tab.tabTipo.facCobrada == True:

                contPagadoCobrado = contPagadoCobrado + tab.tabTotal

            if tab.tabTipo.mercPagada == True:

                contPagadoCobrado = contPagadoCobrado - tab.tabTotal

        tableAuxGet.tabTotal = cont
        tableAuxGet.save()

    tableAux = mainTableAux.objects.all().order_by("tabTipo__nombre")

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    editPrueba = False

    dic = {"contPagadoCobrado":contPagadoCobrado,"noIncludeTotalGasto":noIncludeTotalGasto,"noIncludeTotal":noIncludeTotal,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"editPrueba":editPrueba,"contTotal":contTotal,"dateTo":dateTo,"dateFrom":dateFrom,"editPrueba":editPrueba,"tableAux":tableAux}

    # return render(request,"spareapp/contDay.html",dic)
    return render(request,"spareapp/contByRange.html",dic)

def contThisMonth(request):

    tod = datetime.now().date()
    mes = datetime.now().date().month
    anio = datetime.now().date().year
    allTypes = factType.objects.all().order_by("nombre")
    tableAux = mainTableAux.objects.all()

    editPrueba = False
    allTypes = factType.objects.all().order_by("nombre")
    tableAux = mainTableAux.objects.all()

    date_today = datetime.now()
    dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
    dateFrom = dateFrom.date()

    dateTo = tod

    for all in tableAux:

        all.delete()

    contTotal = 0
    noIncludeTotal = 0
    noIncludeTotalGasto = 0
    contPagadoCobrado = 0

    for typ in allTypes:

        tableAuxGet = mainTableAux()
        tableAuxGet.tabTipo = typ
        tableAux = mainTable.objects.filter(tabTipo=typ,fecha__date__month=mes,fecha__date__year=anio)
        cont = 0

        for tab in tableAux:

            cont = cont + float(tab.tabTotal)

            if typ.include == True:

                if  typ.facCobrada == False and typ.mercPagada == False:

                    contTotal = float(contTotal) + float(tab.tabTotal)

            else:

                if  typ.facCobrada == False and typ.mercPagada == False:

                    if typ.ingreso == True:

                        noIncludeTotal = noIncludeTotal + float(tab.tabTotal)

                    else:

                        noIncludeTotalGasto = noIncludeTotalGasto + float(tab.tabTotal)

            if tab.tabTipo.facCobrada == True:

                contPagadoCobrado = contPagadoCobrado + tab.tabTotal

            if tab.tabTipo.mercPagada == True:

                contPagadoCobrado = contPagadoCobrado - tab.tabTotal

        tableAuxGet.tabTotal = cont
        tableAuxGet.save()

    tableAux = mainTableAux.objects.all().order_by("tabTipo__nombre")

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"contPagadoCobrado":contPagadoCobrado,"noIncludeTotalGasto":noIncludeTotalGasto,"noIncludeTotal":noIncludeTotal,"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"contTotal":contTotal,"editPrueba":editPrueba,"dateTo":dateTo,"dateFrom":dateFrom,"editPrueba":editPrueba,"tableAux":tableAux}

    return render(request,"spareapp/contByRange.html",dic)

def editeFact(request,val,val2):

    # http://localhost:8000/contType/CASH%3F2021-11-13

    # contType/CASH%3F2021-11-13
    # http://localhost:8000/editeFact/485/contTypeCASH%3F2021-11-13

    # http://localhost:8000/editeFact/485/contTypeCASH%3F2021-11-13

    urlFinal = ""
    if val2.find("contType")>-1:
        typeA = val2.replace("contType","")
        urlFinal = "/contType/"+typeA
    if val2.find("contTypeTarjeta")>-1:
        typeA = val2.replace("contTypeTarjeta","")
        urlFinal = "/contTypeTarjeta/"+typeA
    if val2.find("accountDay")>-1:
        typeA = val2.replace("accountDay","")
        urlFinal = "/accountDay"
    if val2.find("accountStat")>-1:
        fAux = factura.objects.get(id=val)
        pAux = fAux.refPersona.id
        typeA = val2.replace("accountStat","")
        urlFinal = "/contIndividual/"+str(pAux)
    if val2.find("contIndividual")>-1:
        fAux = factura.objects.get(id=val)
        pAux = fAux.refPersona.id
        typeA = val2.replace("contIndividual","")
        urlFinal = "/contIndividual/"+str(pAux)
    if val2.find("contListByType")>-1:
        fAux = factura.objects.get(id=val)
        typeA = val2.replace("contListByType","")
        urlFinal = "/contListByType/"+typeA
    if val2.find("contListByCategory")>-1:
        typeA = val2.replace("contListByCategory","")
        urlFinal = "/contListByCategory/"+typeA
    check = False
    allCustomers = persona.objects.all()
    allTypes = factType.objects.all()
    # DEPENDE DEL TYPE SALEN UNOS U OTROS
    facAux = factura.objects.filter(id=val)
    facTotal = 0
    auxFacGet = factura.objects.get(id=val)
    todold = auxFacGet.fechaCreado.date()
    actual=str(auxFacGet.fechaCreado.date().year)+"-"+str('%02d' % auxFacGet.fechaCreado.date().month)+"-"+str('%02d' % auxFacGet.fechaCreado.date().day)
    # actual=auxFacGet.fechaCreado.date()
    if auxFacGet.monto == auxFacGet.total:
        check = False
    else:
        check = True

    if facAux[0].refCategory.ingreso == True:

        allCategories = factCategory.objects.filter(ingreso=True)

    else:

        allCategories = factCategory.objects.filter(egreso=True)

    if request.method == "POST":

        returnPath = request.POST.get("returnPath")
        # ---------------------------------------------------
        fechaAct = request.POST.get("searchDateFrom")
        contNombre = request.POST.get("contNombre")
        nomAux = persona.objects.get(id=contNombre)
        factAux = factura.objects.get(id=request.POST.get("facId"))
        fechaAct = datetime.strptime(fechaAct,'%Y-%m-%d')
        if factAux.fechaCreado.date() != fechaAct.date():
            factAux.fechaCreado = fechaAct
        else:
            print("Iguales")
        factAux.refPersona = nomAux

        if request.POST.get("contNumFac"):
            contNumFac = request.POST.get("contNumFac")
            factAux.num = contNumFac

        contTypeIng = request.POST.get("contTypeIng")
        typeAux = factType.objects.get(id=contTypeIng)
        factAux.refType = typeAux

        contCatIng = request.POST.get("contCatIng")
        catAux = factCategory.objects.filter(id=contCatIng)
        
        # Revisa si la categoria tiene limite
        # for cat in catAux:
        #     if cat.limite == True:
        #         factAux.pendiente = True

        catAux = factCategory.objects.get(id=contCatIng)
        factAux.refCategory = catAux

        if request.POST.get("contFechaTope") != "":
            contFechaTope = request.POST.get("contFechaTope")
            factAux.fechaTope = contFechaTope

        contMonto = request.POST.get("contMonto")
        factAux.monto = contMonto

        if request.POST.get("contItbm") == "":
            contIva = float(0)
        else:
            contIva = request.POST.get("contItbm")
        factAux.iva = contIva

        contTotal = request.POST.get("contTotal")
        factAux.total = contTotal

        factAux.note = request.POST.get("contNota")

        factAux.save()

        # Para la fecha nueva -----------------------------------------------------------

        tod = factAux.fechaCreado.date()
        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")

        allTypes = factType.objects.all().order_by("nombre")

        for ty in allTypes:

            if  tableAux:

                tableAuxType = mainTable.objects.get(fecha__date=tod,tabTipo__nombre=ty)

            else:

                tableAuxType = mainTable()
                tableAuxType.fecha = tod
                tableAuxType.tabTipo = ty
                tableAuxType.tabTotal = 0

            allFacturesCash = factura.objects.filter(fechaCreado__date=tod,refType=ty).order_by("fechaCreado")
            acum = 0

            for fac in allFacturesCash:

                acum = acum + fac.total
            tableAuxType.tabTotal = float(acum)

            if ty.facCobrar == True:

                allFacturesPay = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")
                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total

                tableAuxType.tabTotal = float(acum2)
            
            if ty.mercPagar == True:

                allFacturesPay = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")

                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total
                
                tableAuxType.tabTotal = float(acum2)

            if ty.facCobrada == True:

                allFacturesPay = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")
                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total

                tableAuxType.tabTotal = float(acum2)

            if ty.mercPagada == True:

                allFacturesPay = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")
                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total

                tableAuxType.tabTotal = float(acum2)
            
            if ty.visa == True:

                allFacturesVisa = factura.objects.filter(fechaCreado__date=tod,refType__nombre=ty).order_by("fechaCreado")

                acum = 0

                for fac in allFacturesVisa:

                    if fac.monto == fac.total:

                        itbm = 0
                        
                    else:

                        itbm = fac.iva

                    retencion = float(itbm/2)
                    interes = float(fac.total)*0.0225*1.07

                    acum = acum + (fac.total)

                tableAuxType.tabTotal = float(acum)
            
            if ty.clave == True:

                allFacturesClave = factura.objects.filter(fechaCreado__date=tod,refType__nombre=ty).order_by("fechaCreado")

                acum = 0

                for fac in allFacturesClave:

                    if fac.monto == fac.total:

                        itbm = 0
                        
                    else:

                        itbm = fac.iva

                    retencion = float(itbm/2)
                    interes = float(fac.total)*0.02*1.07

                    acum = acum + (fac.total)

                tableAuxType.tabTotal = float(acum)

            tableAuxType.save()

        # Fin fecha nueva ---------------------------------------------------------

        # Para la fecha vieja -----------------------------------------------------------

        tod = todold
        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")
        allTypes = factType.objects.all().order_by("nombre")

        for ty in allTypes:

            if tableAux:

                tableAuxType = mainTable.objects.get(fecha__date=tod,tabTipo__nombre=ty.nombre)

            else:

                tableAuxType = mainTable()
                tableAuxType.tabTipo = ty
                tableAuxType.fecha = tod
                tableAuxType.tabTotal = 0

            allFacturesCash = factura.objects.filter(fechaCreado__date=tod,refType=ty).order_by("fechaCreado")
            acum = 0

            for fac in allFacturesCash:

                acum = acum + fac.total

            tableAuxType.tabTotal = float(acum)

            if ty.facCobrar == True:

                allFacturesPay = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")

                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total
                
                tableAuxType.tabTotal = float(acum2)
            
            if ty.mercPagar == True:

                allFacturesPay = factura.objects.filter(fechaCreado__date=tod,pendiente=True,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")

                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total
                
                tableAuxType.tabTotal = float(acum2)

            if ty.facCobrada == True:

                allFacturesPay = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")
                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total

                tableAuxType.tabTotal = float(acum2)

            if ty.mercPagada == True:

                allFacturesPay = factura.objects.filter(fechaCobrado=tod,pendiente=False,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")
                acum2 = 0

                for fac in allFacturesPay:

                    acum2 = acum2 + fac.total

                tableAuxType.tabTotal = float(acum2)

            if ty.visa == True:

                allFacturesVisa = factura.objects.filter(fechaCreado__date=tod,refType__nombre=ty).order_by("fechaCreado")

                acum = 0

                for fac in allFacturesVisa:

                    if fac.monto == fac.total:

                        itbm = 0
                        
                    else:

                        itbm = fac.iva

                    retencion = float(itbm/2)
                    interes = float(fac.total)*0.0225*1.07

                    if fac.refCategory.ingreso == True:

                        acum = acum + (fac.total)
                    
                    else:

                        acum = acum - (fac.total)

                tableAuxType.tabTotal = float(acum)
            
            if ty.clave == True:

                allFacturesClave = factura.objects.filter(fechaCreado__date=tod,refType__nombre=ty).order_by("fechaCreado")

                acum = 0

                for fac in allFacturesClave:

                    if fac.monto == fac.total:

                        itbm = 0
                        
                    else:

                        itbm = fac.iva

                    retencion = float(itbm/2)
                    interes = float(fac.total)*0.02*1.07

                    if fac.refCategory.ingreso == True:

                        acum = acum + (fac.total)
                    
                    else:

                        acum = acum - (fac.total)

                tableAuxType.tabTotal = float(acum)

            tableAuxType.save()

        # Fin fecha vieja ---------------------------------------------------------

        tableAux = mainTable.objects.filter(fecha__date=tod).order_by("tabTipo__nombre")

        dic = {"actual":actual,"tableAux":tableAux,"allCustomers":allCustomers,"tod":tod,"allTypes":allTypes,"allCategories":allCategories}
    
        return redirect(urlFinal)

        # ---------------------------------------------------
    
    dic = {"urlFinal":urlFinal,"actual":actual,"check":check,"allCategories":allCategories,"allTypes":allTypes,"allCustomers":allCustomers,"facAux":facAux}

    return render(request,"spareapp/editeFact.html",dic)

def contTotalDay(request):

    allTypes = factType.objects.all().order_by("nombre")
    editPrueba = False

    if request.method == "POST":

        # print(request.POST)

        fechaAux = request.POST.get("searchDate")
        tableAuxPro = mainTable.objects.filter(fecha__date=fechaAux)

        if tableAuxPro:

            print("Ya existe la tabla")

        else:

            print("No existe la tabla")

            for typ in allTypes:

                tableAux = mainTable()
                tableAux.fecha = fechaAux
                tableAux.tabTipo = typ

                if typ.manual:

                    monto = request.POST.get(str(typ.nombre).replace(" ", "")+"Total")
                    if monto:
                        tableAux.tabTotal = float(monto)
                    else:
                        tableAux.tabTotal = float(0)
                else:

                    if typ.facCobrado == True:

                        print("Factura cobrado")
                    
                    tableAux.tabTotal = float(0)
                
                tableAux.save()
                tableChange = mainTable.objects.get(id=tableAux.id)
                tableChange.fecha=fechaAux
                tableChange.save()

    dic = {"editPrueba":editPrueba,"allTypes":allTypes}

    return render(request,"spareapp/contTotalDay.html",dic)

def contIndividual(request,val):

    allCustomers = persona.objects.all().order_by("nombre")
    personaAux = persona.objects.get(id=val)
    factureName = factura.objects.filter(refPersona=personaAux).order_by("fechaCreado","id")
    print(factureName)
    balance = {}
    cont = 0
    balanceTotal = 0

    for fac in factureName:

        print(fac)

        if fac.refCategory.ingreso:

            cont = cont

            if fac.refType.facCobrar==True:

                cont = cont + fac.total
            
            if fac.refCategory.nombre=="Factura cobrada":

                cont = cont - fac.total
        
        else:

            cont = cont

            if fac.refType.mercPagar==True:

                cont = cont - fac.total
            
            if fac.refCategory.nombre=="Mercancia credito pagada":

                cont = cont + fac.total

        if fac.pendiente == True and  fac.refType.gasto == True:
            balance[fac.id] = [cont,fac.total*(-1)]
        else:
            balance[fac.id] = [cont,fac.total]

    balanceTotal = cont

    dayFrom = factureName[0].fechaCreado.date()
    dayTo = factureName[len(factureName)-1].fechaCreado.date()

    if request.method == "POST":

        auxNombre = request.POST.get("contNombre")
        factureName = factura.objects.filter(refPersona__id=auxNombre).order_by("fechaCreado","id")
        if factureName:
            dayFrom = factureName[0].fechaCreado.date()
            dayTo = factureName[len(factureName)-1].fechaCreado.date()
        cont = 0
        
        for fac in factureName:

            if fac.refCategory.ingreso:

                cont = cont

                if fac.refType.facCobrar==True:

                    cont = cont + fac.total
                
                if fac.refCategory.nombre=="Factura cobrada":

                    cont = cont - fac.total
            
            else:

                cont = cont

                if fac.refType.mercPagar==True:

                    cont = cont - fac.total
                
                if fac.refCategory.nombre=="Mercancia credito pagada":

                    cont = cont + fac.total

            if fac.pendiente == True and  fac.refType.gasto == True:
                balance[fac.id] = [cont,fac.total*(-1)]
            else:
                balance[fac.id] = [cont,fac.total]

        balanceTotal = cont

        factureName = factura.objects.filter(refPersona__id=auxNombre).order_by("fechaCreado","id")

        if request.POST.get("search") == "balance":


            for key in balance:

                if balance[key]==0:
                    pos = key
            
            facActAux = factura.objects.filter(id=pos)

            if facActAux:
            
                facAct = factura.objects.get(id=pos)
                factureName = factura.objects.filter(id__gte=facAct.id,fechaCreado__gte=facAct.fechaCreado,refPersona__id=auxNombre).order_by("fechaCreado","id")
            
            else:

                factureName = None

        if request.POST.get("search") == "month":

            mes = datetime.now().date().month
            date_today = datetime.now()
            dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
            dateFrom = dateFrom.date()

            mes = datetime.now().date().month
            dayFrom = dateFrom
            dayTo = datetime.now().date()
            anio = datetime.now().date().year
            factureName = factura.objects.filter(fechaCreado__month=mes,fechaCreado__year=anio,refPersona__id=auxNombre).order_by("fechaCreado")

        if request.POST.get("search") == "range":

            dateFrom = request.POST.get("searchDateFrom")
            dateTo = request.POST.get("searchDateTo")

            fecha_from = datetime.strptime(dateFrom, '%Y-%m-%d')
            fecha_to = datetime.strptime(dateTo, '%Y-%m-%d')

            dayFrom = fecha_from.date()
            dayTo = fecha_to.date()

            if dateFrom and dateTo:
                
                factureName = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refPersona__id=auxNombre).order_by("fechaCreado")

    balanceTotal = cont

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"dayFrom":dayFrom,"dayTo":dayTo,"allCustomers":allCustomers,"balanceTotal":balanceTotal,"balance":balance,"factureName":factureName}

    return render(request,"spareapp/accountStat.html",dic)

def factTypeES(request):

    cobrarPagar = None
    cate = None

    cateAux = factCategory.objects.filter(nombre=request.GET.get("cat"))

    if cateAux:
        cate = factCategory.objects.get(nombre=request.GET.get("cat"))

    if request.GET.get("val") == "entry":

        if cateAux and request.GET.get("cat") == "Factura cobrada":
            allCategories = factCategory.objects.filter(ingreso=True).order_by("nombre")
        else:
            allCategories = factCategory.objects.filter(ingreso=True).order_by("nombre").exclude(nombre="Factura cobrada").exclude(nombre="Mercancia credito pagada")
        if cateAux and cate.limite == True:
            allTypes = factType.objects.filter(ingreso=True).order_by("nombre").exclude(facCobrada=True).exclude(mercPagada=True).exclude(mercPagar=True)
        else:
            allTypes = factType.objects.filter(ingreso=True).order_by("nombre").exclude(facCobrada=True).exclude(mercPagada=True).exclude(mercPagar=True).exclude(facCobrar=True)
        cobrarPagar = factType.objects.filter(facCobrar=True)
    
    else:

        if cateAux and request.GET.get("cat") == "Mercancia credito pagada":
            allCategories = factCategory.objects.filter(egreso=True).order_by("nombre")
        else:
            allCategories = factCategory.objects.filter(egreso=True).order_by("nombre").exclude(nombre="Factura cobrada").exclude(nombre="Mercancia credito pagada")
        if cateAux and cate.limite == True:
            allTypes = factType.objects.filter(gasto=True).order_by("nombre").exclude(facCobrada=True).exclude(mercPagada=True).exclude(facCobrar=True)
        else:
            allTypes = factType.objects.filter(gasto=True).order_by("nombre").exclude(facCobrada=True).exclude(mercPagada=True).exclude(mercPagar=True).exclude(facCobrar=True)
        cobrarPagar = factType.objects.filter(mercPagar=True)

    allCategories = list(allCategories.values())
    allTypes = list(allTypes.values())
    cobrarPagar = list(cobrarPagar.values())

    return JsonResponse({'cobrarPagar':cobrarPagar,'allTypes':allTypes,'allCategories': allCategories})

def contListByTypeZero(request):

    allTypes = factType.objects.all().order_by("nombre")
    dayFrom = ""
    dayTo = ""
    factureName = None
    balanceTotal = 0
    itbmTotal = 0
    interesTotal = 0
    retencionTotal = 0

    if request.method == "POST":

        val = request.POST.get("contNombre")
        factureName = factura.objects.filter(refType__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
        if factureName:
            dayFrom = factureName[0].fechaCreado.date()
            dayTo = factureName[len(factureName)-1].fechaCreado.date()

        balanceTotal = 0

        if request.POST.get("search") == "month":

            mes = datetime.now().date().month
            date_today = datetime.now()
            dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
            dateFrom = dateFrom.date()
            dayFrom = dateFrom
            dayTo = datetime.now().date()

            mes = datetime.now().date().month
            anio = datetime.now().date().year
            factureName = factura.objects.filter(fechaCreado__month=mes,fechaCreado__year=anio,refType__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)

        if request.POST.get("search") == "range":

            dateFrom = request.POST.get("searchDateFrom")
            dateTo = request.POST.get("searchDateTo")

            fecha_from = datetime.strptime(dateFrom, '%Y-%m-%d')
            fecha_to = datetime.strptime(dateTo, '%Y-%m-%d')

            dayFrom = fecha_from.date()
            dayTo = fecha_to.date()

            if dateFrom and dateTo:
                
                factureName = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refType__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
        
        for fac in factureName:
            balanceTotal = balanceTotal + fac.total
            itbmTotal = itbmTotal + fac.iva
            retencionTotal = retencionTotal + float(fac.iva/2)
            if fac.refType.visa == True:
                interesTotal = interesTotal + float(float(fac.total)*0.0225*1.07)
            if fac.refType.clave == True:
                interesTotal = interesTotal + float(float(fac.total)*0.02*1.07)

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"retencionTotal":retencionTotal,"interesTotal":interesTotal,"itbmTotal":itbmTotal,"balanceTotal":balanceTotal,"dayFrom":dayFrom,"dayTo":dayTo,"factureName":factureName,"allTypes":allTypes}

    return render(request,"spareapp/contListByType.html",dic)

def contListByType(request,val):

    dayFrom = ""
    dayTo = ""
    balanceTotal = 0
    itbmTotal = 0
    interesTotal = 0
    retencionTotal = 0
    allTypes = factType.objects.all().order_by("nombre")
    factureName = factura.objects.filter(refType__nombre=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
    if factureName:
        dayFrom = factureName[0].fechaCreado.date()
        dayTo = factureName[len(factureName)-1].fechaCreado.date()

    for fac in factureName:
            balanceTotal = balanceTotal + fac.total
            itbmTotal = itbmTotal + fac.iva
            retencionTotal = retencionTotal + float(fac.iva/2)
            if fac.refType.visa == True:
                interesTotal = interesTotal + float(float(fac.total)*0.0225*1.07)
            if fac.refType.clave == True:
                interesTotal = interesTotal + float(float(fac.total)*0.02*1.07)

    if request.method == "POST":

        val = request.POST.get("contNombre")
        factureName = factura.objects.filter(refType__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
        if factureName:
            dayFrom = factureName[0].fechaCreado.date()
            dayTo = factureName[len(factureName)-1].fechaCreado.date()

        balanceTotal = 0

        if request.POST.get("search") == "month":

            mes = datetime.now().date().month
            date_today = datetime.now()
            dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
            dateFrom = dateFrom.date()
            dayFrom = dateFrom
            dayTo = datetime.now().date()

            mes = datetime.now().date().month
            anio = datetime.now().date().year
            factureName = factura.objects.filter(fechaCreado__month=mes,fechaCreado__year=anio,refType__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)

        if request.POST.get("search") == "range":

            dateFrom = request.POST.get("searchDateFrom")
            dateTo = request.POST.get("searchDateTo")

            fecha_from = datetime.strptime(dateFrom, '%Y-%m-%d')
            fecha_to = datetime.strptime(dateTo, '%Y-%m-%d')

            dayFrom = fecha_from.date()
            dayTo = fecha_to.date()

            if dateFrom and dateTo:
                
                factureName = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refCategory__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
            
        for fac in factureName:
            balanceTotal = balanceTotal + fac.total
            itbmTotal = itbmTotal + fac.iva
            retencionTotal = retencionTotal + float(fac.iva/2)
            if fac.refType.visa == True:
                interesTotal = interesTotal + float(float(fac.total)*0.0225*1.07)
            if fac.refType.clave == True:
                interesTotal = interesTotal + float(float(fac.total)*0.02*1.07)
    
    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"retencionTotal":retencionTotal,"interesTotal":interesTotal,"itbmTotal":itbmTotal,"balanceTotal":balanceTotal,"dayFrom":dayFrom,"dayTo":dayTo,"factureName":factureName,"allTypes":allTypes}

    return render(request,"spareapp/contListByType.html",dic)

def contListByCategoryZero(request):

    allCategorys = factCategory.objects.all().order_by("nombre")
    dayFrom = ""
    dayTo = ""
    balanceTotal = 0
    factureName = None

    if request.method == "POST":

        val = request.POST.get("contNombre")
        factureName = factura.objects.filter(refCategory__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
        if factureName:
            dayFrom = factureName[0].fechaCreado.date()
            dayTo = factureName[len(factureName)-1].fechaCreado.date()

        balanceTotal = 0
        
        for fac in factureName:
            balanceTotal = balanceTotal + fac.total

        if request.POST.get("search") == "month":

            mes = datetime.now().date().month
            date_today = datetime.now()
            dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
            dateFrom = dateFrom.date()
            dayFrom = dateFrom
            dayTo = datetime.now().date()

            mes = datetime.now().date().month
            anio = datetime.now().date().year
            factureName = factura.objects.filter(fechaCreado__month=mes,fechaCreado__year=anio,refCategory__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)

        if request.POST.get("search") == "range":

            dateFrom = request.POST.get("searchDateFrom")
            dateTo = request.POST.get("searchDateTo")

            fecha_from = datetime.strptime(dateFrom, '%Y-%m-%d')
            fecha_to = datetime.strptime(dateTo, '%Y-%m-%d')

            dayFrom = fecha_from.date()
            dayTo = fecha_to.date()

            if dateFrom and dateTo:
                
                factureName = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refCategory__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
    
    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"facturesToCollect":facturesToCollect,"facturesToPay":facturesToPay,"balanceTotal":balanceTotal,"dayFrom":dayFrom,"dayTo":dayTo,"factureName":factureName,"allCategorys":allCategorys}

    return render(request,"spareapp/contListByCategory.html",dic)

def contListByCategory(request,val):

    dayFrom = ""
    dayTo = ""
    balanceTotal = 0
    allCategorys = factCategory.objects.all().order_by("nombre")
    factureName = factura.objects.filter(refCategory__nombre=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)

    if factureName:
        dayFrom = factureName[0].fechaCreado.date()
        dayTo = factureName[len(factureName)-1].fechaCreado.date()

    for fac in factureName:
        balanceTotal = balanceTotal + fac.total

    if request.method == "POST":

        val = request.POST.get("contNombre")
        factureName = factura.objects.filter(refCategory__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
        if factureName:
            dayFrom = factureName[0].fechaCreado.date()
            dayTo = factureName[len(factureName)-1].fechaCreado.date()
        
        balanceTotal = 0
        
        for fac in factureName:
            balanceTotal = balanceTotal + fac.total

        if request.POST.get("search") == "month":

            mes = datetime.now().date().month
            date_today = datetime.now()
            dateFrom = date_today.replace(month=mes,day=1, hour=0, minute=0, second=0, microsecond=0)
            dateFrom = dateFrom.date()
            dayFrom = dateFrom
            dayTo = datetime.now().date()

            mes = datetime.now().date().month
            anio = datetime.now().date().year
            factureName = factura.objects.filter(fechaCreado__month=mes,fechaCreado__year=anio,refType__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)

        if request.POST.get("search") == "range":

            dateFrom = request.POST.get("searchDateFrom")
            dateTo = request.POST.get("searchDateTo")

            fecha_from = datetime.strptime(dateFrom, '%Y-%m-%d')
            fecha_to = datetime.strptime(dateTo, '%Y-%m-%d')

            dayFrom = fecha_from.date()
            dayTo = fecha_to.date()

            if dateFrom and dateTo:
                
                factureName = factura.objects.filter(fechaCreado__date__gte=dateFrom,fechaCreado__date__lte=dateTo,refCategory__id=val).order_by("fechaCreado","id").exclude(refType__facCobrar=True,pendiente=False).exclude(refType__mercPagar=True,pendiente=False)
    
    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)
            
    dic = {"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"balanceTotal":balanceTotal,"dayFrom":dayFrom,"dayTo":dayTo,"factureName":factureName,"allCategorys":allCategorys}

    return render(request,"spareapp/contListByCategory.html",dic)

def contEditPerson(request,val):

    newCust = persona.objects.filter(id=val)
    newCust = persona.objects.get(id=val)

    newCust.nombre = request.POST.get("custName")
    if request.POST.get("custId"):
        newCust.documento = request.POST.get("custId")
    newCust.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
def accountDay(request):

    tod = datetime.now().date()

    factureName = factura.objects.filter(fechaCreado=tod).order_by("refType__nombre","refCategory__nombre","total")

    if request.method == "POST":

        if request.POST.get("search") == "byDay":

            dayAux = request.POST.get("searchDateFrom")

            factureName = factura.objects.filter(fechaCreado=dayAux).order_by("refType__nombre","refCategory__nombre","total")

    cont = 0
    balance = {}
    balanceTotal = 0
    
    for fac in factureName:

        if fac.refCategory.ingreso:

            cont = cont + fac.total

        else:

            cont = cont - fac.total

        balance[fac.id] = cont

    balanceTotal = cont

    allFacturesToPay = factura.objects.filter(pendiente=True,refCategory__ingreso=True,refCategory__limite=True)
    allFacturesToCollect = factura.objects.filter(pendiente=True,refCategory__egreso=True,refCategory__limite=True)
    facturesToCollect = len(allFacturesToPay)
    facturesToPay = len(allFacturesToCollect)

    dic = {"facturesToPay":facturesToPay,"facturesToCollect":facturesToCollect,"balanceTotal":balanceTotal,"balance":balance,"factureName":factureName}

    return render(request,"spareapp/accountDay.html",dic)

def deleteFac(request,val):

    allTypes = factType.objects.all()

    facAux = factura.objects.get(id=val)

    if facAux.refCategory.nombre == "Factura cobrada":

        facAnt = factura.objects.filter(num=facAux.num,refPersona=facAux.refPersona,fechaCobrado=facAux.fechaCreado.date()).exclude(refCategory__nombre="Factura cobrada")

        if len(facAnt)==1:

            facArreglar = factura.objects.exclude(refCategory__nombre="Factura cobrada").get(num=facAux.num,refPersona=facAux.refPersona,fechaCobrado=facAux.fechaCreado.date())
            facArreglar.pendiente = True
            facArreglar.fechaCobrado = None
            facArreglar.save()
    
    if facAux.refCategory.nombre == "Mercancia credito pagada":

        facAnt = factura.objects.filter(num=facAux.num,refPersona=facAux.refPersona,fechaCobrado=facAux.fechaCreado.date()).exclude(refCategory__nombre="Mercancia credito pagada")

        if len(facAnt)==1:

            facArreglar = factura.objects.exclude(refCategory__nombre="Mercancia credito pagada").get(num=facAux.num,refPersona=facAux.refPersona,fechaCobrado=facAux.fechaCreado.date())
            facArreglar.pendiente = True
            facArreglar.fechaCobrado = None
            facArreglar.save()

    facBorrada = facAux.fechaCreado

    facAux.delete()

    for ty in allTypes:

        tableAuxType = mainTable.objects.get(fecha=facBorrada,tabTipo=ty)

        allFacturesCash = factura.objects.filter(fechaCreado=facBorrada,refType=ty).order_by("fechaCreado")
        acum = 0

        for fac in allFacturesCash:

            acum = acum + fac.total
            
        tableAuxType.tabTotal = float(acum)

        if ty.facCobrar == True:

            allFacturesPay = factura.objects.filter(fechaCreado=facBorrada,pendiente=True,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")
            acum2 = 0

            for fac in allFacturesPay:

                acum2 = acum2 + fac.total

            tableAuxType.tabTotal = float(acum2)
        
        if ty.mercPagar == True:

            allFacturesPay = factura.objects.filter(fechaCreado=facBorrada,pendiente=True,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")

            acum2 = 0

            for fac in allFacturesPay:

                acum2 = acum2 + fac.total
            
            tableAuxType.tabTotal = float(acum2)

        if ty.facCobrada == True:

            allFacturesPay = factura.objects.filter(fechaCobrado=facBorrada.date(),pendiente=False,refCategory__limite=True,refCategory__ingreso=True).order_by("fechaTope")
            acum2 = 0

            for fac in allFacturesPay:

                acum2 = acum2 + fac.total

            tableAuxType.tabTotal = float(acum2)

        if ty.mercPagada == True:

            allFacturesPay = factura.objects.filter(fechaCobrado=facBorrada.date(),pendiente=False,refCategory__limite=True,refCategory__egreso=True).order_by("fechaTope")
            acum2 = 0

            for fac in allFacturesPay:

                acum2 = acum2 + fac.total

            tableAuxType.tabTotal = float(acum2)
        
        if ty.visa == True:

            allFacturesVisa = factura.objects.filter(fechaCreado=facBorrada,refType__nombre=ty).order_by("fechaCreado")

            acum = 0

            for fac in allFacturesVisa:

                if fac.monto == fac.total:

                    itbm = 0
                    
                else:

                    itbm = fac.iva

                retencion = float(itbm/2)
                interes = float(fac.total)*0.0225*1.07

                acum = acum + (fac.total)

            tableAuxType.tabTotal = float(acum)
        
        if ty.clave == True:

            allFacturesClave = factura.objects.filter(fechaCreado=facBorrada,refType__nombre=ty).order_by("fechaCreado")

            acum = 0

            for fac in allFacturesClave:

                if fac.monto == fac.total:

                    itbm = 0
                    
                else:

                    itbm = fac.iva

                retencion = float(itbm/2)
                interes = float(fac.total)*0.02*1.07

                acum = acum + (fac.total)

            tableAuxType.tabTotal = float(acum)

        tableAuxType.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # return render(request,"spareapp/accountStat.html")


    # {% for tab in tableAux %}
    #             <!-- <tr data-bs-toggle="collapse" data-bs-target="#accordion{{tab.tabTipo|cut:' '}}" class="clickable"> -->
    #             <tr>
    #                 <td class="p-2"><a href="{% url 'contType' tab.tabTipo tod %}">{{tab.tabTipo}}</a></td>
    #                 <td class="p-2">${{tab.tabTotal|floatformat:2}}</td>
    #             </tr>
    #             <!-- {% for fact in allFactures %}
    #             {% if tab.tabTipo == fact.refType %}
    #             <tr style="background-color: rgb(207, 207, 207);">
    #                 <td id="accordion{{tab.tabTipo|cut:' '}}" class="collapse p-2"><a href="">Facture number: {{fact.num}}</a></td>
    #                 <td id="accordion{{tab.tabTipo|cut:' '}}" class="collapse p-2">${{fact.total}}</td>
    #             </tr>
    #             {% endif %}
    #             {% endfor %} -->
    #             {% endfor %}
    
    # <label class="form-check mb-2">Facture type</label>
    # <input onclick="factTypeFun('entry');" class="form-check-input" id="contFacType1" type="radio" name="contFacType" checked>
    # <label class="form-check-label" for="contFacType1">Entry</label>
    # <input onclick="factTypeFun('spending');" class="form-check-input" id="contFacType2" type="radio" name="contFacType">
    # <label class="form-check-label" for="contFacType2">Spending</label>




# CONTDAY ANTES DE SEPARAR EN DOS TABLAS

# {% extends "spareapp/contBase.html" %}

# {% block title %} Day {% endblock %}

# {% block content %}

# {% include "spareapp/contSuperior.html" %}

# <form method="POST" action="">
# {% csrf_token %}
# <div class="container mt-2">
#     <table style="font-size: small;" class="table-bordered invoice">
#         <thead>
#             <tr class="color text-white">
#                 <th class="p-2">Type</th>
#                 <th class="p-2">Total Remanining</th>
#             </tr>
#         </thead>

#         <tbody>

#             {% if tableAux and editPrueba == False %}

#                 {% for tab in tableAux %}
#                 <tr>
#                     {% if tab.tabTipo.include == True %}
#                     <td class="p-2"><a {% if tab.tabTipo.nombre == "TARJETA VISA" or tab.tabTipo.nombre == "TARJETA CLAVE" %} href="{% url 'contTypeTarjeta' tab.tabTipo|cut:'/' tod %}" {% else %} href="{% url 'contType' tab.tabTipo|cut:'/' tod %}" {% endif %}>{{tab.tabTipo}}</a></td>
#                     {% else %}
#                     <td class="p-2"><a {% if tab.tabTipo.nombre == "TARJETA VISA" or tab.tabTipo.nombre == "TARJETA CLAVE" %} href="{% url 'contTypeTarjeta' tab.tabTipo|cut:'/' tod %}" {% else %} href="{% url 'contType' tab.tabTipo|cut:'/' tod %}" {% endif %}>( {{tab.tabTipo}} )</a></td>
#                     {% endif %}
#                     <td class="p-2">${{tab.tabTotal|floatformat:2}}</td>
#                 </tr>
#                 {% endfor %}
                
#                 <tr>
#                     <td class="p-2 color text-white">Total</td>
#                     <td class="p-2">${{contTotal|floatformat:2}}</td>
#                 </tr>

#                 <!-- <tr>
#                     <td class="p-2 color text-white">Spending total</td>
#                     <td class="p-2">${{spendTotal|floatformat:2}}</td>
#                 </tr> -->

#             {% else %}

#                 {% if editPrueba == True %}

#                     {% for tab in tableAux %}
#                     <tr>
#                         {% if tod %}
#                         <td class="p-2"><a href="{% url 'contType' tab.tabTipo tod %}">{{tab.tabTipo}}</a></td>
#                         {% else %}
#                         <td class="p-2"><a href="{% url 'contType' tab.tabTipo 'today' %}">{{tab.tabTipo}}</a></td>
#                         {% endif %}
#                         {% if tab.tabTipo.manual == True %}
#                         <td class="p-2">$<input value="{{tab.tabTotal}}" id="{{tab.tabTipo.nombre|cut:' '}}Total" name="{{tab.tabTipo.nombre|cut:' '}}Total" type="number"></td>
#                         {% else %}
#                         <td class="p-2">$ {{tab.tabTotal|floatformat:2}}</td>
#                         {% endif %}
#                     </tr>
#                     {% endfor %}
#                     <tr>
#                         <td class="p-2 color text-white">Total</td>
#                         <td class="p-2">${{contTotal|floatformat:2}}</td>
#                     </tr>

#                 {% else %}

#                     {% for tab in allTypes %}
#                     <tr>
#                         {% if tab.include == True %}
#                         <td class="p-2"><a href="">{{tab.nombre}}</a></td>
#                         {% else %}
#                         <td class="p-2"><a href="">(  {{tab.nombre}}  )</a></td>
#                         {% endif %}
#                         {% if tab.manual == True %}
#                         <td class="p-2">$<input id="{{tab.nombre|cut:' '}}Total" name="{{tab.nombre|cut:' '}}Total" type="number"></td>
#                         {% else %}
#                         <td class="p-2">$ 0.00</td>
#                         {% endif %}
#                     </tr>
#                     {% endfor %}
#                     <tr>
#                         <td class="p-2 color text-white">Total</td>
#                         <td class="p-2">$ 0.00</td>
#                     </tr>

#                 {% endif %}

#             {% endif %}

#         </tbody>
#     </table>
# </div>



# <div class="container mt-2">
#     <table style="font-size: small;" class="table-bordered invoice">
        

#         <tbody>

#             {% if tableAux and editPrueba == False %}

#                 {% for tab in tableAux %}
#                 <tr>
#                     {% if tab.tabTipo.include == False %}
#                     <td class="p-2"><a {% if tab.tabTipo.nombre == "TARJETA VISA" or tab.tabTipo.nombre == "TARJETA CLAVE" %} href="{% url 'contTypeTarjeta' tab.tabTipo|cut:'/' tod %}" {% else %} href="{% url 'contType' tab.tabTipo|cut:'/' tod %}" {% endif %}>( {{tab.tabTipo}} )</a></td>
#                     <td class="p-2">${{tab.tabTotal|floatformat:2}}</td>
#                     {% endif %}
#                 </tr>
#                 {% endfor %}
                
#                 <tr>
#                     <td class="p-2 color text-white">Total</td>
#                     <td class="p-2">${{contTotal|floatformat:2}}</td>
#                 </tr>

#                 <!-- <tr>
#                     <td class="p-2 color text-white">Spending total</td>
#                     <td class="p-2">${{spendTotal|floatformat:2}}</td>
#                 </tr> -->

#             {% else %}

#                 {% if editPrueba == True %}

#                     {% for tab in tableAux %}
#                     <tr>
#                         {% if tod %}
#                         <td class="p-2"><a href="{% url 'contType' tab.tabTipo tod %}">{{tab.tabTipo}}</a></td>
#                         {% else %}
#                         <td class="p-2"><a href="{% url 'contType' tab.tabTipo 'today' %}">{{tab.tabTipo}}</a></td>
#                         {% endif %}
#                         {% if tab.tabTipo.manual == True %}
#                         <td class="p-2">$<input value="{{tab.tabTotal}}" id="{{tab.tabTipo.nombre|cut:' '}}Total" name="{{tab.tabTipo.nombre|cut:' '}}Total" type="number"></td>
#                         {% else %}
#                         <td class="p-2">$ {{tab.tabTotal|floatformat:2}}</td>
#                         {% endif %}
#                     </tr>
#                     {% endfor %}
#                     <tr>
#                         <td class="p-2 color text-white">Total</td>
#                         <td class="p-2">${{contTotal|floatformat:2}}</td>
#                     </tr>

#                 {% else %}

#                     {% for tab in allTypes %}
#                     <tr>
#                         {% if tab.include == False %}
#                         <td class="p-2"><a href="">(  {{tab.nombre}}  )</a></td>
                        
#                         {% if tab.manual == True %}
#                         <td class="p-2">$<input id="{{tab.nombre|cut:' '}}Total" name="{{tab.nombre|cut:' '}}Total" type="number"></td>
#                         {% else %}
#                         <td class="p-2">$ 0.00</td>
#                         {% endif %}
#                         {% endif %}
#                     </tr>
#                     {% endfor %}
#                     <tr>
#                         <td class="p-2 color text-white">Total</td>
#                         <td class="p-2">$ 0.00</td>
#                     </tr>

#                 {% endif %}

#             {% endif %}

#         </tbody>
#     </table>
# </div>
# </form>

# {% endblock %}








# <div class="container mt-2">
#     <table style="font-size: small;" class="table-bordered invoice">
#         <thead>
#             <tr class="color text-white">
#                 <th class="p-2">Tipo de pago</th>
#                 <th style="min-width: 100px;" class="p-2">Total</th>
#             </tr>
#         </thead>

#         <tbody>

#             {% if tableAux %}

#                 {% for tab in tableAux %}
#                 <tr>
#                     {% if tab.tabTipo.include == True %}
#                     <td class="p-2"><a {% if tab.tabTipo.visa == True or tab.tabTipo.clave == True %} href="{% url 'contTypeTarjeta' tab.tabTipo|cut:'/' tod %}" {% else %} href="{% url 'contType' tab.tabTipo|cut:'/' tod %}" {% endif %}>{{tab.tabTipo}}</a></td>
#                     <td class="p-2">${{tab.tabTotal|floatformat:2}}</td>
#                     {% endif %}
#                 </tr>
#                 {% endfor %}
                
#                 <tr>
#                     <td class="p-2 color text-white">Total</td>
#                     <td class="p-2">${{contTotal|floatformat:2}}</td>
#                 </tr>

#             {% else %}

#                 {% for tab in allTypes %}
#                 <tr>
#                     {% if tab.include == True %}
#                     <td class="p-2"><a href="">{{tab.nombre}}</a></td>
#                     {% if tab.manual == True %}
#                     <td class="p-2">$<input id="{{tab.nombre|cut:' '}}Total" name="{{tab.nombre|cut:' '}}Total" type="number"></td>
#                     {% else %}
#                     <td class="p-2">$ 0.00</td>
#                     {% endif %}
#                     {% endif %}
#                 </tr>
#                 {% endfor %}
#                 <tr>
#                     <td class="p-2 color text-white">Total</td>
#                     <td class="p-2">$ 0.00</td>
#                 </tr>
#             {% endif %}
#         </tbody>
#     </table>
# </div>


# <div class="container mt-2">
#     <table style="font-size: small;" class="table-bordered invoice">
#         <thead>
#             <tr class="color text-white">
#                 <th class="p-2">Tipo de pago</th>
#                 <th style="min-width: 100px;" class="p-2">Total</th>
#             </tr>
#         </thead>

#         <tbody>

#             {% if tableAux %}

#                 {% for tab in tableAux %}
#                 <tr>
#                     {% if tab.tabTipo.include == False %}
#                     <td class="p-2"><a {% if tab.tabTipo.visa == True or tab.tabTipo.clave == True %} href="{% url 'contTypeTarjeta' tab.tabTipo|cut:'/' tod %}" {% else %} href="{% url 'contType' tab.tabTipo|cut:'/' tod %}" {% endif %}>( {{tab.tabTipo}} )</a></td>
#                     <td class="p-2">${{tab.tabTotal|floatformat:2}}</td>
#                     {% endif %}
#                 </tr>
#                 {% endfor %}

#                 <tr>
#                     <td class="p-2 color text-white">Total</td>
#                     <td class="p-2">${{noIncludeTotal|floatformat:2}}</td>
#                 </tr>

#             {% else %}
                
#                 {% for tab in allTypes %}
#                 <tr>
#                     {% if tab.include == False %}
#                     <td class="p-2"><a href="">(  {{tab.nombre}}  )</a></td>
#                     {% if tab.manual == True %}
#                     <td class="p-2">$<input id="{{tab.nombre|cut:' '}}Total" name="{{tab.nombre|cut:' '}}Total" type="number"></td>
#                     {% else %}
#                     <td class="p-2">$ 0.00</td>
#                     {% endif %}
#                     {% endif %}
#                 </tr>
#                 {% endfor %}
#                 <tr>
#                     <td class="p-2 color text-white">Total</td>
#                     <td class="p-2">$ 0.00</td>
#                 </tr>

#             {% endif %}

#         </tbody>
#     </table>
# </div>