from django.db import models

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=100)
  price = models.FloatField()
  stock = models.IntegerField()

class Order(models.Model):
  date_time = models.DateTimeField(auto_now=True)

class OrderDetail(models.Model):
  order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
  cuantity = models.IntegerField()
  product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)