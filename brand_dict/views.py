from brands.models import SuppliersBrands
import csv
from django.conf import settings
from brand_dict.forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
import os  # Need to be move to top later on
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.views import View


from django.db.models import Q
from django.db import connection

from brands.models import BrandsDict, BrandDictSup, AngSuppliers, AngPricesAll
from brand_dict.forms import BrandForm, BrandFormSetFactory


@method_decorator(login_required, name='dispatch')
class DictionaryList(ListView):
    template_name = 'brand/brands_main.html'
    model = BrandsDict
    paginate_by = 20


# Implementing serach logic
@method_decorator(login_required, name='dispatch')
class DictionarySearchList(ListView):
    template_name = 'brand/brands_main.html'
    model = BrandsDict
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET['q']
        brand_sup = BrandDictSup.objects.filter(ang_brand=q)
        return BrandsDict.objects.filter(Q(brand__startswith=q)).order_by('brand')


@method_decorator(login_required, name='dispatch')
class DictionaryDetailedView(SuccessMessageMixin, ModelFormMixin, DetailView):
    template_name = 'brand/brand_detail.html'
    model = BrandsDict
    form_class = BrandForm
    success_message = 'Бренд сохранен!!'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def post(self, request, *args, **kwags):
        if request.user.is_authenticated:
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                # form.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse('detail-view', args=[self.object.pk])


# Here is the inline formset factory for single brand working with
@login_required
def manage_brands(request, pk, page):
    if not page:
        page = 1
    brand = BrandsDict.objects.get(pk=pk)
    BrandInlineFormSet = inlineformset_factory(BrandsDict, BrandDictSup, fields=(
        'ang_brand',), labels={'ang_brand': ''}, extra=1)
    if request.method == "POST":
        formset = BrandInlineFormSet(request.POST, instance=brand)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            if request.POST.get('submit') == 'stay':
                return HttpResponseRedirect(reverse('detailfunc-view', kwargs={'pk': pk, 'page': page}))
            else:
                return redirect(reverse('main-view') + f'?page={page}')

    else:
        formset = BrandInlineFormSet(instance=brand)
    return render(request, 'brand/brand_detail.html', {'formset': formset})


# Listing suppliers
@method_decorator(login_required, name='dispatch')
class SuppliersList(ListView):
    template_name = 'brand/suppliers_main.html'
    model = AngSuppliers
    paginate_by = 20

    def get_queryset(self):
        sups = AngSuppliers.objects.filter(enabled=1).order_by('-weight')
        return sups

# Supplier detail View
@method_decorator(login_required, name='dispatch')
class SupplierDetail(ListView):
    model = AngPricesAll
    template_name = 'brand/supplier_detail.html'
    paginate_by = 50

    def my_custom_sql(self, pk):
        raw_q = f'''
        SELECT DISTINCT(a.brand) as sup_brand, c.id as id, c.brand FROM ang_prices_all as a LEFT OUTER JOIN brands_branddictsup as b ON a.brand = b.ang_brand LEFT JOIN brands_dict as c ON b.brand_name_id = c.id WHERE supplier = {pk}'''
        with connection.cursor() as cursor:
            cursor.execute(raw_q)
            return cursor.fetchall()

    # def get_queryset(self):
    #     sup = int(self.kwargs.get('pk'))
    #     q = self.model.objects.values('brand').filter(supplier=sup).distinct()

    #     query = self.my_custom_sql(sup)
    #     print(query)
    #     return query

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        lst = self.model.objects.filter(supplier=pk).values_list(
            'brand', flat=True).distinct()

        qs = BrandDictSup.objects.select_related(
            'brand_name').filter(ang_brand__in=lst)

        exist_list = qs.values_list('ang_brand', flat=True)
        not_exist_list = lst.exclude(brand__in=exist_list)

        return not_exist_list


ChildFormset = inlineformset_factory(
    BrandsDict, BrandDictSup, fields=('ang_brand',)
)

# Trying set formset for parent and child together
# Seems to working variant


class ParentCreateView(CreateView):
    model = BrandsDict
    fields = ["brand"]
    #template_name = 'brand/create_alltogether.html'
    template_name = 'brand/supplier_detail.html'
    paginate_by = 50

    def get_data(self):
        pk = self.kwargs.get('pk')
        lst = AngPricesAll.objects.filter(supplier=pk).values_list(
            'brand', flat=True).distinct()

        qs = BrandDictSup.objects.select_related(
            'brand_name').filter(ang_brand__in=lst)

        exist_list = qs.values_list('ang_brand', flat=True)
        not_exist_list = lst.exclude(
            brand__in=exist_list).distinct().order_by('name')

        return not_exist_list

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        data['object_list'] = self.get_data()
        if self.request.POST:
            data["children"] = ChildFormset(self.request.POST)
        else:
            data["children"] = ChildFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return redirect(reverse_lazy("supplier-detail", kwargs={'pk': 1}))


################################################################
# Adding upload brand list feature #
###############################################################


class UploadBrandList(View):
    template_name = 'brand/add_brand_list.html'
    form_class = UploadFileForm
    initial = {'title': 'angara.csv'}
    table_name = 'brands_suppliersbrands'


# Function for inserting csv file to Brnads for checking angara
    def insert_data(self, request):
        path = os.path.join(settings.MEDIA_ROOT, 'brands')
        f = os.path.join(path, os.listdir(path)[0])

        with open(f, encoding='utf-8') as csvfile:
            angara = csv.reader(csvfile, delimiter=';')
            bulk = [SuppliersBrands(
                **{'brand': i[0], 'supplier': AngSuppliers.objects.get(id=1000)}) for i in angara if i]
            if SuppliersBrands.objects.bulk_create(bulk):
                os.remove(f)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        # self.insert_data(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,  request.FILES)
        if form.is_valid():
            # <process form cleaned data>
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage(location='media/brands/')
            name = fs.save(uploaded_file.name, uploaded_file)
            self.insert_data(request)
            return HttpResponseRedirect(reverse('class-upload-file'))

        return render(request, self.template_name, {'form': form})
