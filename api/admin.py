from django.contrib import admin
from . models import Ingredients,BakeryItems,Inventory,Order
# Register your models here.
admin.site.register(Inventory)
admin.site.register(Ingredients)
admin.site.register(BakeryItems)
admin.site.register(Order)