from django.shortcuts import render, HttpResponse
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer, OrderModelSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from .models import OrderDetail, Product, Order
from rest_framework import viewsets
from rest_framework.decorators import action

# Create your views here.

class ProductList(viewsets.ModelViewSet):
  serializer_class = ProductSerializer
  queryset = Product.objects.all()

  def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

  def update(self, request, pk=None):
      response = {'message': 'Update function is not offered in this path.'}
      return Response(response, status=status.HTTP_403_FORBIDDEN)

  def partial_update(self, request, pk=None):
      response = {'message': 'Update function is not offered in this path.'}
      return Response(response, status=status.HTTP_403_FORBIDDEN)

  def destroy(self, request, pk=None):
      response = {'message': 'Delete function is not offered in this path.'}
      return Response(response, status=status.HTTP_403_FORBIDDEN)

  
class OrderList(viewsets.ModelViewSet):
  serializer_class = OrderSerializer
  queryset = OrderDetail.objects.all()

  def create(self, request):
        response = {'message': 'Create not allowed'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

  def update(self, request, pk=None):
      response = {'message': 'Update not allowed'}
      return Response(response, status=status.HTTP_403_FORBIDDEN)

  def partial_update(self, request, pk=None):
      response = {'message': 'Update not allowed'}
      return Response(response, status=status.HTTP_403_FORBIDDEN)

  def destroy(self, request, pk=None):
      response = {'message': 'Delete not allowed'}
      return Response(response, status=status.HTTP_403_FORBIDDEN)


class CreateOrUpdateProduct(viewsets.ModelViewSet):
  serializer_class = ProductSerializer
  queryset = Product.objects.all()
  
  def create(self, request, *args, **kwargs):
    product_data = request.data
    name = product_data.get('name')
    price = product_data.get('price')
    stock = product_data.get('stock')
    try:
      product = Product.objects.get(
        name=name,
      )
      product.name = name
      product.price = price
      product.stock = stock
      # Update the product info
      product.save(update_fields=['name', 'price', 'stock'])
      return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
      product = Product.objects.create(
        name=name,
        price=price,
        stock=stock,
      )
      return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
  
  def update(self, request, *args, **kwargs):
    product = self.get_object()
    data = request.data
    product.name = data.get('name')
    product.price = data.get('price')
    product.stock = data.get('stock')
    product.save(update_fields=['name', 'price', 'stock'])
    return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class GetProduct(viewsets.ModelViewSet):
  serializer_class = ProductSerializer
  queryset = Product.objects.all()

  @action(methods=['get'], detail=True)
  def get_product(self, request, *args, **kwargs):
    try:
      product = Product.objects.get(id=kwargs.get('pk'))
      return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
      return Response({'message': 'product id Does not exist'}, status=status.HTTP_400_BAD_REQUEST)
      

class DeleteProduct(viewsets.ModelViewSet):
  serializer_class = ProductSerializer
  queryset = Product.objects.all()
  
  def destroy(self, request, *args, **kwargs):
    product = self.get_object()
    product.delete()
    return Response({'message': 'Item correctly deleted'}, status=status.HTTP_200_OK)
  
  def update(self, request, pk=None):
    response = {'message': 'Update not allowed'}
    return Response(response, status=status.HTTP_403_FORBIDDEN)

class UpdateProductStock(viewsets.ModelViewSet):
  serializer_class = ProductSerializer
  queryset = Product.objects.all()

  @action(methods=['post'], detail=True)
  def update_product_stock(self, request,   *args, **kwargs):
    data = request.data
    try:
      product = Product.objects.get(id=kwargs.get('pk'))
      product.stock = data.get('stock')
      product.save(update_fields=['stock'])
      return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
      return Response({'message': 'product id Does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class CreateOrUpdateOrder(viewsets.ModelViewSet):
  serializer_class = OrderSerializer
  queryset = OrderDetail.objects.all()
  
  def create(self, request, *args, **kwargs):
    order_data = request.data
   
    try:
      order = Order.objects.get(id=order_data.get('order'))
    except Order.DoesNotExist:
      order = Order.objects.create()

    try:
      product = Product.objects.get(id=order_data.get('product'))

      # Multiple products in one order NOT ALLOWED:
      same_product_in_order = order.orderdetail_set.filter(product=product)
      if same_product_in_order:
        return Response({'message': 'Product Already added'}, status=status.HTTP_400_BAD_REQUEST)

      if int(order_data.get('cuantity')) > product.stock:
        return Response({'message': 'insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
      else:
        product.stock = product.stock - int(order_data.get('cuantity'))
        product.save(update_fields=['stock'])
    except Product.DoesNotExist:
      return Response({'message': 'Product Does not exist... Order Error'}, status=status.HTTP_400_BAD_REQUEST)
    
    new_order_detail = OrderDetail.objects.create(
      order=order,
      cuantity= int(order_data.get('cuantity')),
      product=product,
    )

    return Response(OrderSerializer(new_order_detail).data, status=status.HTTP_200_OK)
  
  def update(self, request, *args, **kwargs):
    order_details = self.get_object()
    data = request.data
    
    try:
      older_cuantity = int(order_details.cuantity)
      new_product = Product.objects.get(id=data.get('product'))
      new_order = Order.objects.get(id=data.get('order'))

      order_details.product.stock = order_details.product.stock + older_cuantity
      order_details.product.save(update_fields=['stock'])

      if int(data.get('cuantity')) > new_product.stock:
        return Response({'message': 'insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
      else:
        new_product.stock = new_product.stock - int(data.get('cuantity'))
        new_product.save(update_fields=['stock'])

      order_details.order = new_order
      order_details.cuantity = int(data.get('cuantity'))
      order_details.product = new_product

      order_details.save(update_fields=['order', 'cuantity', 'product'])
    except Product.DoesNotExist:
      return Response({'message': 'Product Does not exist... Order Error'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
      return Response({'message': 'Order Does not exist... Order Error'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(OrderSerializer(order_details).data, status=status.HTTP_200_OK)


class DeleteOrder(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderModelSerializer
  
  @action(methods=['delete'], detail=True)
  def delete_order(self, request, *args, **kwargs):
    try:
      order = Order.objects.get(id=kwargs.get('pk'))
      orders = order.orderdetail_set.all()
      for ord in orders.iterator():
        ord.product.stock = ord.product.stock + ord.cuantity
        ord.product.save(update_fields=['stock'])
    except Order.DoesNotExist:
      return Response({'message': 'Order Does not exist... Order Error'}, status=status.HTTP_400_BAD_REQUEST)
    
    order.delete()
    return Response({'message': 'Order correctly deleted'}, status=status.HTTP_200_OK)


class GetOrderAndDetails(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderModelSerializer
  
  @action(methods=['get'], detail=True)
  def get_order_and_details(self, request, *args, **kwargs):
    try:
      result = {}
      order = Order.objects.get(id=kwargs.get('pk'))
      orders = order.orderdetail_set.all()
      for ord in orders.iterator():
        result_aux = {}
        result_aux['product'] = ProductSerializer( ord.product).data
        result_aux['order'] = OrderModelSerializer(ord.order).data
        result_aux['cuantity'] = ord.cuantity 
        result[f'order_detail_{ord.id}'] = result_aux
      return Response(result, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
      return Response({'message': 'Order Does not exist... Order Error'}, status=status.HTTP_400_BAD_REQUEST)



