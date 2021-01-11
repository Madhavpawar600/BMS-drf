from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.apiOverview,name='apioverview'),
    path('register/',views.register,name='register'),
    path('login/',views.Userlogin,name='login'),
    path('logout/',views.Userlogout,name='logout'),
    path('order/',views.orderItem,name='orderitem'),
    path('order_history/',views.OrderHistory,name='orderhistory'),
    path('productlist/',views.productList,name='productlist'),
    path('add_ingredients/',views.addIngredients,name='addingredients'),
    path('add_bakeryitem/',views.addBakeryItem,name='addbakeryitem'),
    path('inventory/',views.inventory,name='inventory'),
    path('inventory_add/',views.inventoryadd,name='inventoryadd'),
    path('inventory_delete/<str:pk>',views.inventorydelete,name='inventorydelete'),
    path('inventory_update/<str:pk>',views.inventoryupdate,name='inventoryupdate'),
]