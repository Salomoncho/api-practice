from django.test import TestCase
from api import models

class ModelsTest(TestCase):

  def setUp(self):
    self.order_1 = models.Order.objects.create()
    self.product_1 = models.Product.objects.create(
      name = 'Salomon',
      price = 105.3,
      stock = 5,
    )
    # return super().setUp()

  def test_order_model(self):
    self.order_1.refresh_from_db()
    self.assertEqual(models.Order.objects.first().id, 1)

  def test_product_model(self):
    self.product_1.refresh_from_db()
    self.assertEqual(models.Order.objects.first().id, 1)

  def test_order_detail_model(self):
    order_detail_1 = models.OrderDetail.objects.create(
      order = self.order_1,
      cuantity = 2,
      product = self.product_1,
    )
    order_detail_1.refresh_from_db()
    self.assertEqual(models.Order.objects.first().id, 1)