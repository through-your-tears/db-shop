import os
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from . import models


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = ('name',)


class VendorSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = models.Vendor
        fields = ('code', 'name', 'country')


class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'


class VendorContactSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.VendorContact
        fields = ('email', 'phone_number', 'vendor')


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(read_only=True)
    driver = serializers.StringRelatedField()

    class Meta:
        model = models.Truck
        fields = '__all__'


class InventoryProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = models.InventoryProduct
        fields = ('product', 'counter')


class InventorySerializer(serializers.ModelSerializer):
    products = InventoryProductSerializer(many=True, read_only=False)

    class Meta:
        model = models.Inventory
        fields = ('date', 'products')


class ChequeSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(read_only=False, many=True)

    class Meta:
        model = models.Cheque
        fields = ('seller', 'dt', 'products')


class CreateChequeSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(read_only=False, many=True, queryset=models.ActualProduct.objects.all())

    class Meta:
        model = models.Cheque
        fields = ('seller', 'dt', 'products',)


class ActualProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.ActualProduct
        fields = '__all__'


class CreateCouponSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=models.ActualProduct)

    class Meta:
        model = models.Coupon
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = models.Coupon
        fields = '__all__'


class UploadFileSerializer(serializers.Serializer):

    file = serializers.FileField()

    def validate(self, attrs):
        file = attrs.get('file', None)
        filename, file_extension = os.path.splitext(file.name)

        if file and file_extension == '.csv':
            return file
