import datetime
import requests
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_length(value):
    if len(value) != 20:
        raise ValidationError("%s is not 20 digits" % value)


class Vendor(models.Model):  # Поставщик

    vendor_name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.vendor_name


class Manufacturer(models.Model):  # Производитель
    manufacturer_name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.manufacturer_name


class Manufacturer_lot(models.Model):  # Партия производителя
    manufacturer_lot_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.manufacturer_lot_number


class Material(models.Model):  # Сырье

    code = models.CharField(max_length=6, unique=True)
    marking = models.CharField(max_length=30, blank=True)
    material_name = models.CharField(max_length=200)
    unit = models.CharField(max_length=3, default="кг")
    barcode = models.CharField(
        max_length=13, unique=True, blank=True, null=True)

    class Meta:
        ordering = ["material_name"]

    def save(self, *args, **kwargs):
        ip = "192.168.1.13:9504"
        # ip="srv-webts:9504"
        id = self.code
        request_txt = (
            "http://" + ip +
            "/MobileSMARTS/api/v1/Products('" +
            id + "')"
        )
        response = requests.get(request_txt)
        status = response.status_code
        if status == 200:
            data = response.json()
            self.marking = data['marking']
            d_barcode = data['packings'][0]['barcode']
            if len(d_barcode) == 13:
                self.barcode = d_barcode
        else:
            pass
        super(Material, self).save(*args, **kwargs)

    def __str__(self):
        return self.code + " " + self.marking + " " + self.material_name


class Lot(models.Model):  # Квазипартия
    lot_code = models.CharField(max_length=20, unique=True)
    material = models.ForeignKey(
        Material, blank=True, null=True, on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, blank=True, null=True, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(
        Manufacturer, blank=True, null=True, on_delete=models.CASCADE)
    manufacturer_lot = models.ForeignKey(
        Manufacturer_lot, blank=True, null=True, on_delete=models.CASCADE)
    lot_expire = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ip = "192.168.1.13:9504"
        # ip="srv-webts:9504"
        lot_id = self.lot_code
        request_txt = (
            "http://" + ip +
            "/MobileSMARTS/api/v1/Tables/Lotpr('" +
            lot_id + "')"
        )
        response = requests.get(request_txt)
        status = response.status_code
        if status == 200:
            data = response.json()
            self.vendor, _ = Vendor.objects.get_or_create(
                vendor_name=data['provider'])
            self.manufacturer, _ = Manufacturer.objects.get_or_create(
                manufacturer_name=data['producer'])
            self.manufacturer_lot, _ = Manufacturer_lot.objects.get_or_create(
                manufacturer_lot_number=data['pr_Lot'])
            self.lot_expire = data['expire'].split("T")[0]
        else:
            pass
        super(Lot, self).save(*args, **kwargs)

    def __str__(self):
        return self.lot_code


class Batch(models.Model):

    batch_name = models.CharField(max_length=20, unique=True)
    b_year = models.DecimalField(
        max_digits=1, decimal_places=0, blank=True, editable=False
    )
    b_month = models.CharField(max_length=1, blank=True, editable=False)
    b_number = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, editable=False
    )

    class Meta:
        ordering = ["b_year", "b_month", "b_number"]

    def save(self, *args, **kwargs):
        self.b_year = self.batch_name[-1]
        self.b_month = self.batch_name[-2]
        self.b_number = self.batch_name[:-2]
        super(Batch, self).save(*args, **kwargs)

    def __str__(self):
        return self.batch_name


# Пользователь


class W_user(models.Model):

    w_user_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.w_user_name


# Емкость тест


class Can(models.Model):

    can_id = models.CharField(max_length=20, unique=True)
    can_date = models.DateField(blank=True, editable=False)
    can_time = models.TimeField(blank=True, editable=False)
    can_device = models.CharField(max_length=3, blank=True, editable=False)
    can_batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    can_user = models.ForeignKey(W_user, on_delete=models.CASCADE)

    class Meta:
        ordering = ["can_id"]

    def save(self, *args, **kwargs):
        # Проверка на возможность преобразования
        save_date = datetime.datetime.strptime(self.can_id[3:11], "%d%m%Y")
        self.can_date = save_date.strftime("%Y-%m-%d")
        save_time = datetime.datetime.strptime(self.can_id[11:17], "%H%M%S")
        self.can_time = save_time.strftime("%H:%M:%S")
        self.can_device = self.can_id[-3:]
        super(Can, self).save(*args, **kwargs)

    def __str__(self):
        return self.can_id




""" class LLot(models.Model):

    lot_code = models.CharField(
        max_length=20, unique=True, validators=[validate_length]
    )
    lot_material = models.ForeignKey(
        Material, blank=True, null=True, on_delete=models.CASCADE
    )
    lot_vendor = models.ForeignKey(
        Vendor, blank=True, null=True, on_delete=models.CASCADE
    )
    lot_date = models.DateField(blank=True, null=True, editable=False)
    lot_producer = models.ForeignKey(
        Producer, blank=True, null=True, on_delete=models.CASCADE
    )
    lot_producer_lot = models.ForeignKey(
        Producer_lot, blank=True, null=True, on_delete=models.CASCADE
    )
    lot_expire = models.DateField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        lot_id=self.lot_code
        request_txt = (
        "http://srv-webts:9504/MobileSMARTS/api/v1/Tables/Lotpr('" + \
                                                                lot_id + "')"
    )
        response = requests.get(request_txt)
        status = response.status_code
        if status=200:
            data=response.json()
            record=data["value"][0]
            # self.lot_material=record['value']
            self.lot_vendor=
            self.lot_date=
            self.lot_producer=
            self.lot_producer_lot=
            self.lot_expire=
        super(Lot, self).save(*args, **kwargs)
    # def get_lots(self.lot_code): """


"""
    def __str__(self):
        return self.lot_code """


# Взвешивания


class Weighting(models.Model):

    weighting_id = models.ForeignKey(Can, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=3)

    class Meta:
        ordering = ["weighting_id__can_batch", "material"]

    def __str__(self):
        return (
            str(self.weighting_id)
            + " "
            + str(self.weighting_id.can_batch)
            + " "
            + str(self.material.material_name)
            + " "
            + str(self.lot)
            + " "
            + str(self.weighting_id.can_user)
            + " "
            + str(self.quantity)
        )


"""




class Lot(models.Model):

    lot_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.lot_code





class Weighting(models.Model):

    weighting_id = models.ForeignKey(Row_id, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch_pr, on_delete=models.CASCADE)
    material = models.ForeignKey(Raw_material, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    w_user = models.ForeignKey(W_user, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=3)

    class Meta:
        ordering = ['batch', 'material']

    def __str__(self):
        return str(self.weighting_id)+" "+str(self.batch)+" " +\
            str(self.material)+" "+str(self.lot)+" " + \
            str(self.w_user)+" "+str(self.quantity)


class Production2(models.Model):

    prod_batch = models.ForeignKey(Batch_pr, on_delete=models.CASCADE)
    prod_material = models.ForeignKey(Raw_material, on_delete=models.CASCADE)
    prod_decl_quantity = models.DecimalField(max_digits=7, decimal_places=3) """
