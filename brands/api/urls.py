from django.urls import include, path
from rest_framework.routers import DefaultRouter
from brands.api.router import router
from brands.api import views as bv
from brands.views import MakeTmpTable

#router = DefaultRouter()
#router.register(r'questions', qv.QuestionViewSet)
urlpatterns = [
        path('brand_update/', include(router.urls)),
        path('brand_dup_detail/<int:pk>/', bv.CheckDuplicatesDetail.as_view(), name='dup-check-detail'),
        path('brand_sup_not_exists/<int:pk>/', bv.AngPriceAllViewNotExists.as_view(), name='brand-sup-not-exists'),
        path('check_duplicates/<str:brand>/', bv.CheckDuplicates.as_view(), name='brand-check'),
        path('new_brands/', bv.AlbumAPIView.as_view(), name='brnd-list'),
        path('maketable/', MakeTmpTable.as_view(), name='meke-table'),
        path('supplires/', bv.SupplersListView.as_view(), name='suppliers-list'),
        ]

