from django.db import models
from django.core import validators
from django.conf import settings

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=128)


class Vendor(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=128)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)


class Product(models.Model):

    class Meta:
        indexes = ['barcode']

    barcode = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    expiration_days = models.IntegerField()
    size = models.IntegerField()
    units = models.CharField(max_length=64)


class VendorContact(models.Model):

    class Meta:
        indexes = ['vendor']

    email = models.EmailField()
    phone_number = models.CharField(max_length=14)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class ProductContract(models.Model):
    file = models.FileField()
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)


class ProductContractProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)


class Region(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)


class Truck(models.Model):

    class Meta:
        unique_together = (('license_plate', 'region'),)

    license_plate = models.CharField(max_length=6, validators=validators.MinLengthValidator(
        6, 'License plate cannot be less than 6 symbols'), primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=64)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


'''вверху справочники(склад данных), снизу уже то, что будет постоянно и часто использоваться'''


class Coupon(models.Model):
    barcode = models.BigIntegerField(primary_key=True)
    sale = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ActualCoupon(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    expires = models.DateField()


class ActualPriceProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.IntegerField()


class Inventory(models.Model):
    date = models.DateField(auto_now=True)


class InventoryProduct(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    counter = models.IntegerField()


class Cheque(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)  # подумай ещё
    dt = models.DateTimeField(auto_now=True)






# обдумай тоже и не ссылайся на справочник продуктов
# class ChequeProduct(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#     cheque = models.ForeignKey(Cheque, on_delete=models.RESTRICT)

# class PriceTag(models.Model):
#
#
# class Report(models.Model):
