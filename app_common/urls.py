from django.urls import path
from .views import VendorListCreateAPIView, VendorDetailAPIView, PurchaseOrderListCreateAPIView, PurchaseOrderDetailAPIView, VendorPerformanceAPIView

urlpatterns = [
    # Vendor Profile Management
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),

    # Purchase Order Tracking
    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),

    # Vendor Performance Evaluation
    path('api/vendors/<int:pk>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
]