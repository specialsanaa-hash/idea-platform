"""
مسارات API لبوابة العميل لنظام الفواتير
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientInvoiceViewSet

router = DefaultRouter()
router.register(r'invoices', ClientInvoiceViewSet, basename='client-invoice')

urlpatterns = [
    path('', include(router.urls)),
]


