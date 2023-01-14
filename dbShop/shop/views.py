from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from . import models
from . import permissions
from . import serializers
from . import tasks
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


class VendorContactViewSet(ModelViewSet):
    queryset = models.VendorContact.objects.all()
    permission_classes = (permissions.IsMerchandiser,)
    serializer_class = serializers.VendorContactSerializer
    pagination_class = LimitOffsetPagination


class RegionViewSet(ModelViewSet):
    queryset = models.Region.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.RegionSerializer
    pagination_class = LimitOffsetPagination


class TruckViewSet(ModelViewSet):
    queryset = models.Truck.objects.all()
    permission_classes = (permissions.IsDirector,)
    serializer_class = serializers.TruckSerializer
    pagination_class = LimitOffsetPagination


class InventoryViewSet(ModelViewSet):
    queryset = models.Inventory.objects.all()
    permission_classes = (permissions.IsDirector, permissions.IsStorekeeper)
    serializer_class = serializers.InventorySerializer
    pagination_class = LimitOffsetPagination


class ChequeViewSet(ModelViewSet):
    queryset = models.Cheque
    permission_classes = (permissions.IsSeller, permissions.IsDirector)
    serializer_class = serializers.ChequeSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.CreateChequeSerializer
        else:
            return self.serializer_class


class ActualProductPriceViewSet(ModelViewSet):
    queryset = models.ActualProduct
    permission_classes = (permissions.IsMerchandiserOrAuthenticatedReadOnly,)
    serializer_class = serializers.ActualProductSerializer
    pagination_class = LimitOffsetPagination


class CouponViewSet(ModelViewSet):
    queryset = models.Coupon
    permission_classes = (permissions.IsSeller, permissions.IsDirector)
    serializer_class = serializers.CouponSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.CreateCouponSerializer
        else:
            return self.serializer_class


class GetPricingAPI(APIView):
    permission_classes = (permissions.IsGK,)
    serializer_class = serializers.UploadFileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tasks.create_pricing(request.data['file'].temporary_file_path())
        return Response(status=status.HTTP_202_ACCEPTED)


class AddProductsAPI(APIView):
    permission_classes = (permissions.IsStorekeeper, permissions.IsDirector)
    serializer_class = serializers.UploadFileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tasks.get_products_from_vendor(request.data['file'].name)
        return Response(status=status.HTTP_202_ACCEPTED)
