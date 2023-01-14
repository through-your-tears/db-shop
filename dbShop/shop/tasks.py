from datetime import date
import csv
from dbShop.celery import app
from .models import *
from shopAuth.models import Notification, CustomUser, Role
from django.core.exceptions import ObjectDoesNotExist


@app.task
def start_inventory():
    Inventory.objects.create()
    Notification.objects.create(
        user=CustomUser.objects.get(role=Role.objects.get('director')),
        text='Сегодня началась инвентаризация',
    )
    for user in CustomUser.objects.filter(role=Role.objects.get('storekeeper')):
        Notification.objects.create(
            user=user,
            text='Сегодня началась инвентаризация',
        )


def send_stop_list():
    pass


async def create_stop_list():
    with open('stoplist.csv', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=",", lineterminator="\r")
        writer.writerow(['ProductName', 'YesterdayPrice', 'VendorPrice', 'ReceiptDate'])
    async for product in ActualProduct.objects.filter(stopped=True):
        writer.writerow([product.product.name, product.price, product.vendor_price, product.receipt_date])
    send_stop_list()


@app.task
def create_pricing(file):
    with open(file, encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                product = Product.objects.get(pk=row[0])
                shop_product = ActualProduct.objects.get(
                    product=product
                )
                yesterday_price = shop_product.price
                gk_price = int(row[1])
                stopped = False
                if (date.today() - shop_product.receipt_date) > 30:
                    ucenka = gk_price * (1 - 0.01 * (date.today() - shop_product.receipt_date - 30))
                    shop_product.price = ucenka if ucenka > gk_price / 4 else gk_price / 4
                else:
                    if shop_product.price > gk_price:
                        shop_product.price = gk_price
                    try:
                        sale = Coupon.objects.get(product=product, expires__gt=date.today())
                    except ObjectDoesNotExist:
                        sale = 0
                    shop_product.price -= shop_product.price * sale * 0.01
                if shop_product.price / product.extra_charge * 100 > shop_product.vendor_price:
                    stopped = True
                elif yesterday_price + yesterday_price / 100 * product.yesterday_price_percent < shop_product.price:
                    stopped = True
                elif yesterday_price - yesterday_price / 100 * product.yesterday_price_percent > shop_product.price:
                    stopped = True
                if stopped:
                    shop_product.stopped = True
                    shop_product.price = yesterday_price
                    shop_product.save(updated_fields=['stopped'])
                else:
                    shop_product.save(updated_fields=['price'])
            except ObjectDoesNotExist:
                pass
    create_stop_list()


@app.task
def get_products_from_vendor(file):
    ProductContract.object.create(
        file=file,
    )
    with open(file, encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ActualProduct.objects.create(
                product=Product.objects.get(pk=row[0]),
                count_storage=row[2],
                count_shop=0,
                vendor_price=row[3],
                production_date=row[4]
            )
