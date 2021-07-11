from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('delete-product', views.DeleteProduct, basename='delete-prod')
router.register('create-update-product', views.CreateOrUpdateProduct, basename='create-update-prod')
router.register('create-update-order', views.CreateOrUpdateOrder, basename='create-update-order')
router.register('product-list', views.ProductList, basename='product-list')
router.register('order-list', views.OrderList, basename='order-list')

urlpatterns = [
    # path('', views.ApiHome),
    path('', include(router.urls)),
    path('get-product/<int:pk>/', views.GetProduct.as_view({"get": "get_product"}),name='get-product'),
    path('update-stock/<int:pk>/', views.UpdateProductStock.as_view({'post': 'update_product_stock'}), name='update-stock'),
    path('delete-order/<int:pk>/', views.DeleteOrder.as_view({"delete": "delete_order"}), name='delete-order'),
    path('get-order-and-details/<int:pk>/', views.GetOrderAndDetails.as_view({"get": "get_order_and_details"}), name='get-order-and-details'),
]

