from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse_lazy


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class SuppliersBrands(models.Model):
    brand = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.ForeignKey(
        AngSuppliers, on_delete=models.CASCADE, blank=True, null=True, related_name='supplier_related')
    count = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = True
        #db_table = 'ang_prices_all'

    def __str__(self):
        return self.name


class BrandsDict(models.Model):
    brand = models.CharField(max_length=255, unique=True)

    class Meta:
        managed = True
        db_table = 'brands_dict'

    def get_absolute_url(self):
        return reverse_lazy('detailfunc-view', args=[self.pk])

    def __str__(self):
        return self.brand


class BrandDictSup(models.Model):
    ang_brand = models.CharField(max_length=255, null=True)
    brand_name = models.ForeignKey(
        to='brands.BrandsDict', related_name='brand_supplier', on_delete=models.CASCADE)

    class Meta:
        managed = True

    def __str__(self):
        return self.ang_brand


class BrandsDictSup(models.Model):
    suplier_brand_name = models.CharField(max_length=255)
    brand_dict = models.ForeignKey(
        BrandsDict, related_name='ang_brand_name', on_delete=models.CASCADE)

    def __str__(self):
        return self.ang_brand
