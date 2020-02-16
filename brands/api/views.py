from .serializers import AlbumSerializer  # , AlbumPKSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from brands.models import BrandsDict, SuppliersBrands, BrandDictSup, AngSuppliers, BrandsDictSup
from brands.api.serializers import AngPriceAllSerializerNotExists, BrandsDictSerializer
from brands.api.serializers import CheckDuplicatesSerializer, BrandDictSupSerializer, SuppliersSerializer

from django.db import connection


# class BrandsListAPIView(APIView):

#     def get(self, request):
#         brands = BrandsDict.objects.filter(brand='MOBIS')
#         serializer = BrandsDictSerializer(brands, many=True)
#         return Response(serializer.data)


# Trying to save my data from vue to database


class BrandsDictViewSet(viewsets.ModelViewSet):
    queryset = BrandsDict.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['brand']


# Using for return list of not exists brands in our dictionry related to supplier

def get_non_exists(pk):
        lst = SuppliersBrands.objects.filter(
            supplier=pk).values_list('brand', flat=True).distinct()
        qs = BrandDictSup.objects.select_related(
            'brand_name').filter(ang_brand__in=lst)
        exist_list = qs.values_list('ang_brand', flat=True)
        not_exist_list = lst.exclude(brand__in=exist_list).order_by('brand')
        nel = []
        for n in not_exist_list:
            cnt = SuppliersBrands.objects.filter(brand__iexact=n).count()
            p = {'ang_brand': n, 'count': cnt}

            nel.append(p)
        return nel

class AngPriceAllViewNotExists(generics.ListAPIView):

    serializer_class = AngPriceAllSerializerNotExists
    permission_classes = [IsAuthenticated]
    #pagination_class = None

    def get_queryset(self):

        pk = self.kwargs.get('pk')
        return get_non_exists(pk)

    def list(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        response = super().list(request, args, kwargs)
        response.data['supplier'] = AngSuppliers.objects.get(id=pk).name
        return response

# Using for checking if brand have already exists in the dictionry


class CheckDuplicates(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, brand='some_bulshit'):

        # try:

        res = BrandsDict.objects.filter(Q(brand__startswith=brand) | Q(
            brand_supplier__ang_brand__startswith=brand)).distinct()
        serializer = CheckDuplicatesSerializer(res, many=True)
        return Response(serializer.data)
        # except:
        #    return Response({"brand": ""})


class CheckDuplicatesDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        # try:

        res = BrandsDict.objects.get(id=pk)
        print(res)
        serializer = CheckDuplicatesSerializer(res)
        return Response(serializer.data)
        # except:
        #    return Response({"brand": ""})


###############################################################################


class AlbumAPIView(APIView):

    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):

        #albums = BrandsDict.objects.all()
        #pk = self.kwargs.get('pk')
        pk = 1
        lst = SuppliersBrands.objects.filter(
            supplier=pk).values_list('brand', flat=True).distinct()
        qs = BrandDictSup.objects.select_related(
            'brand_name').filter(ang_brand__in=lst)
        exist_list = qs.values_list('ang_brand', flat=True)
        not_exist_list = lst.exclude(brand__in=exist_list)
        # print(not_exist_list)
        nel = []
        for n in not_exist_list:
            p = {'ang_brand': n}
            nel.append(p)

        brands_dict = BrandsDict.objects.all()

        serializer = AlbumSerializer(instance=brands_dict, many=True)
        #serializer = AlbumPKSerializer(instance=albums, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Listing all suppliers





class SupplersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    qset = list(SuppliersBrands.objects.values_list(
        'supplier', flat=True).annotate(cnt=Count('supplier')))
    queryset = AngSuppliers.objects.filter(enabled=1, weight__gt=0).annotate(
        b_c=Count('supplier_related')).order_by('-weight')

    queryset = queryset.filter(id__in=qset)

    serializer_class = SuppliersSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name']
    pagination_class = None
