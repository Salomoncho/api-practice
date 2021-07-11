from api import models
import json
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class APITest(APITestCase):
  def setUp(self) :
    self.product_info_1 = {"name": "Cepillo", 'price': 13.3, 'stock': 15 }
    self.product_info_2 = {"name": "Pasta Dental", 'price': 30.2, 'stock': 20 }
    self.client.post("/create-update-product/", self.product_info_1)
    self.client.post("/create-update-product/", self.product_info_2)

  def test_create_update_product(self):
    data = {"name": "Jabon", 'price': 34, 'stock': 10 }
    response = self.client.post("/create-update-product/", data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Update with put
    data_to_update = {"name": "Cepillo", 'price': 25.5, 'stock': 17 }
    response = self.client.put("/create-update-product/1/", data_to_update)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    received_response = json.loads(response.content)
    self.assertEqual(received_response.get('price'), data_to_update['price'])
  
  def test_delete_product(self):
    product_list = models.Product.objects.all().count()
    response = self.client.delete("/delete-product/1/")
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(models.Product.objects.all().count(), product_list - 1)

  def test_get_product(self):
    response = self.client.get("/get-product/2/")
    received_response = json.loads(response.content)
    product_2 = {"id": 2, "name": "Pasta Dental", 'price': 30.2, 'stock': 20 }
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(received_response, product_2)

  def test_product_list(self):
    response = self.client.get("/product-list/")
    received_response = json.loads(response.content)
    expected_result = [
      {"id": 1,"name": "Cepillo", 'price': 13.3, 'stock': 15 },
      {"id": 2, "name": "Pasta Dental", 'price': 30.2, 'stock': 20},
    ]
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(received_response, expected_result)

  def test_update_stock(self):
    response = self.client.post("/update-stock/1/", {'stock': 300})
    received_response = json.loads(response.content)
    expected_result = {"id": 1, "name": "Cepillo", 'price': 13.3, 'stock': 300 }
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(received_response, expected_result)
  