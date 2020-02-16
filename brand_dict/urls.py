from django.urls import path, include, re_path
from brand_dict import views as v
from django.views.generic import TemplateView


urlpatterns = [
    path('', v.DictionaryList.as_view(), name='main-view'),
    path('search/', v.DictionarySearchList.as_view(), name='search-view'),
    path('detail/<int:pk>/', v.DictionaryDetailedView.as_view(), name='detail-view'),
    path('detail_func/<int:pk>/<int:page>/', v.manage_brands, name='detailfunc-view'),
    path('suppliers/', v.SuppliersList.as_view(), name='suppliers-view'),
    path('supplier/<int:pk>/', v.SupplierDetail.as_view(), name='supplier-detail'),
    path('create/<int:pk>/', v.ParentCreateView.as_view(), name='create-brand'),
    path('class/upload/', v.UploadBrandList.as_view(), name='class-upload-file'),
    ]