from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Ingredients(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class BakeryItems(models.Model):
    item=models.CharField(max_length=20)
    cprice=models.IntegerField()
    sprice=models.IntegerField()
    ingredients=models.ManyToManyField(Ingredients)

    def __str__(self):
        return self.item

class Inventory(models.Model):
    item=models.ForeignKey(BakeryItems,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return str(self.item)

    @property
    def bakery_item(self):
        return self.item.item

    @property
    def price(self):
        return self.item.sprice

class Order(models.Model):
    date=models.DateField(auto_now_add=True)
    bakeryitem=models.ForeignKey(BakeryItems,on_delete=models.CASCADE)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return str(self.customer)+str(self.date)

    @property
    def bakery_item(self):
        return self.bakeryitem.item

    @property
    def customer_name(self):
        return self.customer.first_name
