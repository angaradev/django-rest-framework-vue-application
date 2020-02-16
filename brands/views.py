from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from django.shortcuts import redirect, render
from django.db.models import Count, Q

from brands.api.serializers import BrandsDictSerializer
from brands.models import BrandsDict, SuppliersBrands, AngPricesAll, AngSuppliers
#from questions.api.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


class BrandsDictViewSet(viewsets.ModelViewSet):
    queryset = BrandsDict.objects.all()
    lookup_field = 'brand_name_2'
    serializer_class = BrandsDictSerializer
    permission_classes = [IsAuthenticated]

# Inserting data from ang_prices_all to tmp table


class MakeTmpTable(View):
    template_name = 'tmp.html'

    def get(self, request):
        above_1 = Count('book', filter=Q(__gt=5))
        qs = AngPricesAll.objects.values('brand', 'supplier').annotate(
            brand_count=Count('supplier')).exclude(brand_count=0)
        
       

        SuppliersBrands.objects.all().delete()

        brand_list = [SuppliersBrands(** {'supplier': AngSuppliers.objects.get(id=q['supplier']),
         "brand": q['brand'], "count": q['brand_count']}) for q in qs]

        brand_list = []
        for q in qs:

            try:
                sup = AngSuppliers.objects.get(id=q['supplier'])
                brand_list.append(SuppliersBrands(
                    **{"supplier": sup, "brand": q['brand'], "count": q['brand_count']}))
            except Exception as e:
                print(e)

        SuppliersBrands.objects.bulk_create(brand_list)

        #return render(request, self.template_name)
        return redirect('/suppliers')
