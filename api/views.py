from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Inventory,BakeryItems,Ingredients,Order
from .serializer import InventorySerializers,UserSerializers,OrderSerializer,ProductSerializers

#views
@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'Login':'/login/',
        'Logout':'/logout',
        'Register':'/register/',
        'Products':'/productlist',
        'order':'/order',
        'order history':'/order_history',
        'Add Ingredients':'/add_ingredients',
        'Add Bakery Item':'/add_bakeryitem',
        'Inventory':'/inventory',
        'Add Item in Inventory':'/inventory_add',
        'Delete Item from Inventory':'/inventory_delelete/<id>',
        'Update Inventory':'/inventory_update/<id>',
    }
    return Response(api_urls)

@api_view(['POST'])
def register(request):
    print(request.data)
    serializer=UserSerializers(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        if user:
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Userlogin(request):
    if request.user.is_authenticated:
        return Response({'response':'already login'})
    print(request.data)
    username=request.data['username']
    password=request.data['password']
    user=authenticate(username=username,password=password)
    print(user)
    if user:
        login(request,user)
        return Response({'response':'login Successfully!!!'},status=status.HTTP_201_CREATED)
    data={'response':'invalid username/password'}
    return Response(data)


@api_view(['GET'])
def Userlogout(request):
    logout(request)
    data={'Response':'logout Successfully!!!'}
    return Response(data)


@api_view(['GET'])
def productList(request):
    if request.user.is_authenticated:
        queryset=Inventory.objects.all()
        print(queryset)
        serializer=ProductSerializers(queryset,many=True)
        return Response(serializer.data)
    else:
        return Response({'response':'Please Login First!!!'})

@api_view(['GET'])
def inventory(request):
    if request.user.is_authenticated and request.user.is_staff:
        queryset=Inventory.objects.all()
        print(queryset)
        serializer=InventorySerializers(queryset,many=True)
        return Response(serializer.data)
    else:
        return Response({'response':'Only admin have permission'})

@api_view(['POST'])
def inventoryadd(request):
    if request.user.is_authenticated and request.user.is_staff:
        try:
            bitem=BakeryItems.objects.get(item=request.data['bakeryitem'])
        except:
            return Response({'Response':'Bakery item is not present in DB'})
        
        inv=Inventory.objects.create(item=bitem,quantity=request.data['quantity'])
        inv.save()
        return Response({'Response':'Bakery Item has been added in Inventory'})
    else:
        return Response({'Response':'Only admin have permission'})

@api_view(['DELETE'])
def inventorydelete(request,pk):
    if request.user.is_authenticated and request.user.is_staff:
        inv=Inventory.objects.get(id=int(pk))
        inv.delete()
        return Response({'Response':'Bakery Item has been removed from Inventory'})
    else:
        return Response({'Response':'Only admin have permission'})

@api_view(['PUT'])
def inventoryupdate(request,pk):
    if request.user.is_authenticated and request.user.is_staff:
        inv=Inventory.objects.get(id=int(pk))
        inv.quantity=request.data['quantity']
        inv.save()
        return Response({'Response':'Successfully Updated'})
    else:
        return Response({'Response':'Only admin have permission'})

@api_view(['GET','POST'])
def orderItem(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            data={'bakeryitems':'Enter list of bakeryitems','quantity':'Enter list of quantity of bakery items'}
            return Response(data)
        elif request.method=='POST':
            bakeryitem=request.data['bakeryitems']
            quantity=request.data['quantity']
            ItemPrice={}
            print(bakeryitem,quantity)
            total_price=0
            for i in range(0,len(bakeryitem)):
                price=BakeryItems.objects.get(item=bakeryitem[i]).sprice
                total_price+=(price * int(quantity[i]))
                ItemPrice[bakeryitem[i]]=str(price) + '*' + str(quantity[i]) + '='+' '+str((price * int(quantity[i])))
                bitem=BakeryItems.objects.get(item=bakeryitem[i])
                inventory=Inventory.objects.get(item=bitem)
                inventory.quantity-=int(quantity[i])
                inventory.save()
                order=Order.objects.create(quantity=quantity[i],bakeryitem=bitem,customer=request.user)
                order.save()
            return Response({'Response':'bill','item Price':ItemPrice,'Total Price':total_price})
    else:
        return Response({'Response':'Please Login First'})

@api_view(['GET'])
def OrderHistory(request):
    if request.user.is_authenticated:
        try:
            queryset=Order.objects.filter(customer=request.user)
        except:
            return Response({'Response':'You have not purchase any item'})
        print(queryset)
        serializer=OrderSerializer(queryset,many=True)
        print(serializer)
        #if serializer.is_valid():
        return Response(serializer.data)
        #return Response(serializer.errors)
    else:
        return Response({'Response':'Please Login First'})

@api_view(['POST'])
def addIngredients(request):
    if request.user.is_authenticated and request.user.is_staff:
        ingredient=Ingredients.objects.create(name=request.data['ingredient'])
        ingredient.save()
        return Response({'Response':'New Ingredient has been added.'})
    else:
        return Response({'Response':'Only admin have permission.'})

@api_view(['POST'])
def addBakeryItem(request):
    if request.user.is_authenticated and request.user.is_staff:
        bitem=BakeryItems.objects.create(item=request.data['item'],cprice=request.data['cprice'],
                sprice=request.data['sprice'])
        for i in range(0,len(request.data['ingredient'])):
            ing=Ingredients.objects.get(name=request.data['ingredient'][i])
            bitem.ingredients.add(ing)
        bitem.save()
        return Response({'Response':'New BakeryItem has been added.'})
    else:
        return Response({'Response':'Only admin have permission.'})
