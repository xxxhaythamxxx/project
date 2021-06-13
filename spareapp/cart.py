from .models import *
from django.conf import settings
from django.contrib import messages

class Cart:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self,spare):
        if str(spare.id) not in self.cart.keys():
            spare_id = str(spare.id)
            self.cart[spare_id] = {
                "spare_photo": spare.spare_photo.url,
                "spare_code": spare.spare_code,
                "spare_brand": spare.spare_brand,
                "spare_name": spare.spare_name,
            }
        else:
            for key, value in self.cart.items():
                if key == str(spare.id):
                    print("El repuesto ya está en el carrito")
                    break
        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def remove(self,spare):
        spare_id = str(spare.id)
        if spare_id in self.cart:
            del self.cart[spare_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def __iter__(self):
        spare_ids = self.cart.keys()
        spares = spare.objects.filter(id__in = spare_ids)
        cart = self.cart.copy()
        for sp in spares:
            self.cart[str(sp.id)]["spare"] = sp
        
