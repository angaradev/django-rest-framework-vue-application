from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('languages', views.LanguageView)
router.register('paradigms', views.ParadigmView)
router.register('programmers', views.ProgrammerView)
router.register('nested', views.NestedView)


urlpatterns = [
        path('', include(router.urls)),
        ]
