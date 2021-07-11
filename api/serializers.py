from rest_framework import serializers
from .models import Order, OrderDetail, Product

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = '__all__' # ['id' ,'name', 'price', 'stock']

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderDetail
    fields = '__all__' 

class OrderModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'