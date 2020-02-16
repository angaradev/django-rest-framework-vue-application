# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AngPricesAll(models.Model):
    orig_number = models.CharField(max_length=255, blank=True, null=True)
    oem_number = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=3072, blank=True, null=True)
    stock = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    kratnost = models.CharField(max_length=100, blank=True, null=True)
    car = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.IntegerField()
    subcategory_id = models.IntegerField(blank=True, null=True)
    supplier = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ang_prices_all'


class AngSuppliers(models.Model):
    name = models.CharField(max_length=255)
    folder = models.CharField(max_length=255)
    supplier_file1 = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    period_price_days = models.IntegerField()
    delivery_days = models.IntegerField()
    note = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    email2 = models.CharField(max_length=255, blank=True, null=True)
    price_orig_number = models.CharField(max_length=5, blank=True, null=True)
    price_oem_number = models.CharField(max_length=5)
    price_brand = models.CharField(max_length=5)
    price_name = models.CharField(max_length=5)
    price_stock = models.CharField(max_length=5)
    price_price = models.CharField(max_length=5)
    price_kratnost = models.CharField(max_length=4)
    price_notes = models.CharField(max_length=5)
    delimeter = models.CharField(max_length=17, blank=True, null=True)
    empty_fields = models.CharField(max_length=100, blank=True, null=True)
    price_table = models.CharField(max_length=199, blank=True, null=True)
    enabled = models.SmallIntegerField()
    enabled_search = models.CharField(max_length=1)
    weight = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'ang_suppliers'


class BrandsDict(models.Model):
    brand = models.CharField(max_length=255)
    brand_name_2 = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'brands_dict'
