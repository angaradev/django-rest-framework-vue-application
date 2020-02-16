
from brands.api.views import BrandsDictViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('list', BrandsDictViewSet)
