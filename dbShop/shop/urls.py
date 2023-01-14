from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    path('addpricing', GetPricingAPI.as_view()),
    path('addproducts', AddProductsAPI.as_view())
]

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'vendor/contacts', VendorContactViewSet, basename='vendor contact')
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'products/guide', ProductViewSet, basename='product')
router.register(r'trucks', TruckViewSet, basename='truck')
router.register(r'inventories', InventoryViewSet, basename='inventory')
router.register(r'cheques', ChequeViewSet, basename='cheque')
router.register(r'products', ActualProductPriceViewSet, basename='product')
router.register(r'coupons', CouponViewSet, basename='coupon')

urlpatterns += router.urls
