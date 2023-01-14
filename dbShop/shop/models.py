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
    barcode = models.BigIntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=128)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    expiration_days = models.IntegerField()
    size = models.IntegerField()
    units = models.CharField(max_length=64)
    extra_charge = models.IntegerField(default=1000)
    yesterday_price_percent = models.IntegerField(default=90)

    def __str__(self):
        return self.name


class VendorContact(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=14)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_index=True)


class ProductContract(models.Model):
    file = models.FileField()


class Region(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)


class Truck(models.Model):

    class Meta:
        unique_together = (('license_plate', 'region'),)

    license_plate = models.CharField(max_length=6, validators=[validators.MinLengthValidator(
        6, 'License plate cannot be less than 6 symbols')], primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=64)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


'''вверху справочники(склад данных), снизу уже то, что будет постоянно и часто использоваться'''


class ActualProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    count_storage = models.IntegerField()
    count_shop = models.IntegerField()
    vendor_price = models.IntegerField()
    price = models.IntegerField(default=2147483646)
    production_date = models.DateField()
    receipt_date = models.DateField(auto_now=True)
    stopped = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class Coupon(models.Model):
    sale = models.IntegerField()
    product = models.ForeignKey(ActualProduct, on_delete=models.CASCADE, db_index=True)
    expires = models.DateField()


class Inventory(models.Model):
    date = models.DateField(auto_now=True)


class InventoryProduct(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    counter = models.IntegerField()


class Cheque(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)  # подумай ещё
    dt = models.DateTimeField(auto_now=True)


class ChequeProduct(models.Model):
    product = models.ForeignKey(ActualProduct, on_delete=models.PROTECT, db_index=True)
    cheque = models.ForeignKey(Cheque, on_delete=models.RESTRICT)
