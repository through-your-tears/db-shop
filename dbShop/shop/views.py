from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import models
from . import permissions
from . import serializers
# Create your views here.


class CountryViewSet(ModelViewSet):
    queryset = models.Country.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.CountrySerializer
    pagination_class = LimitOffsetPagination


class VendorViewSet(ModelViewSet):
    queryset = models.Vendor.objects.all()
    permission_classes = (permissions.IsMerchandiserOrAuthenticatedReadOnly,)
    serializer_class = serializers.VendorSerializer
    pagination_class = LimitOffsetPagination


class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    permission_classes = (permissions.IsMerchandiserOrAuthenticatedReadOnly,)
    serializer_class = serializers.ProductSerializer
    pagination_class = LimitOffsetPagination


class VendorContact(ModelViewSet):
    queryset = models.VendorContact.objects.all()
    permission_classes = (permissions.IsMerchandiser,)
    serializer_class = serializers.VendorContactSerializer
    pagination_class = LimitOffsetPagination


class Region(ModelViewSet):
    queryset = models.Region.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.RegionSerializer
    pagination_class = LimitOffsetPagination


class (ModelViewSet):
    queryset =
    permission_classes = (,)
    serializer_class =
    pagination_class = LimitOffsetPagination


class (ModelViewSet):
    queryset =
    permission_classes = (,)
    serializer_class =
    pagination_class = LimitOffsetPagination


class (ModelViewSet):
    queryset =
    permission_classes = (,)
    serializer_class =
    pagination_class = LimitOffsetPagination