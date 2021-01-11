from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Inventory,BakeryItems,Order
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(
                    required=True,
                    validators=[UniqueValidator(queryset=User.objects.all())]
                    )
    username=serializers.CharField(
                    validators=[UniqueValidator(queryset=User.objects.all())]
                    )
    password=serializers.CharField(min_length=8)

    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        return user

    class Meta:
        model=User
        fields=['id','username','email','password','first_name','last_name']


class InventorySerializers(serializers.ModelSerializer):
    class Meta:
        bakery_item=serializers.ReadOnlyField()
        price=serializers.ReadOnlyField()
        model=Inventory
        fields=['id','bakery_item','price','quantity']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        bakery_item=serializers.ReadOnlyField()
        price=serializers.ReadOnlyField()
        model=Inventory
        fields=['bakery_item','price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        bakery_item=serializers.ReadOnlyField()
        customer_name=serializers.ReadOnlyField()
        model=Order
        fields=['date','bakery_item','quantity','customer_name']