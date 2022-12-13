from rest_framework import serializers
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
    vendor = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = models.Product
        fields = '__all__'


class VendorContactSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = models.VendorContact
        fields = ('email', 'phone_number', 'vendor')


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = '__all__'


# обдумать
# class TruckSerializer(serializers.ModelSerializer):
#     region = serializers.PrimaryKeyRelatedField()
#     driver = serializers.StringRelatedField()
#
#     class Meta:
#         model = models.Truck
#         fields = '__all__'


class ListInventoryProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = models.InventoryProduct
        fields = ('product', 'counter')


class InventorySerializer(serializers.ModelSerializer):
    products = ListInventoryProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Inventory
        fields = ('date', )


class InventoryProductSerializer(serializers.ModelSerializer):
    inventory = serializers.PrimaryKeyRelatedField()
    product = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = models.InventoryProduct
        fields = '__all__'


# class Cheque(serializers.ModelSerializer):
#     products =
