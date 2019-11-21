import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_length(value):
    if len(value) != 20:
        raise ValidationError("%s is not 20 digits" % value)


# Варка


class Batch_pr(models.Model):

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
        super(Batch_pr, self).save(*args, **kwargs)

    def __str__(self):
        return self.batch_name


# Сырье


class Material(models.Model):

    code = models.CharField(max_length=6, unique=True)
    marking = models.CharField(max_length=30, blank=True)
    material_name = models.CharField(max_length=200)
    unit = models.CharField(max_length=3, default="кг")
    barcode = models.CharField(max_length=13, unique=True, blank=True, null=True)

    class Meta:
        ordering = ["material_name"]

    def __str__(self):
        return self.code + " " + self.marking + " " + self.material_name


# Пользователь


class W_user(models.Model):

    w_user_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.w_user_name


# Емкость


class Can(models.Model):

    can_id = models.CharField(max_length=20, unique=True)
    can_date = models.DateField(blank=True, editable=False)
    can_time = models.TimeField(blank=True, editable=False)
    can_device = models.CharField(max_length=3, blank=True, editable=False)
    can_batch = models.ForeignKey(Batch_pr, on_delete=models.CASCADE)
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


class Vendor(models.Model):

    vendor_name = models.CharField(max_length=40, unique=True)


class Producer(models.Model):

    producer_name = models.CharField(max_length=40, unique=True)


class Producer_lot(models.Model):

    lot_name = models.CharField(max_length=40, unique=True)


# Квазипартия
class Lot(models.Model):

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

    def __str__(self):
        return self.lot_code


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

