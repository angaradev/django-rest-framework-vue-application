
from django.urls import path, include
from . import views
from rest_framework import routers
from .views import AlbumAPIView


#router = routers.DefaultRouter()

urlpatterns = [
    #       path('', include(router.urls)),
            path('albums/', AlbumAPIView.as_view(), name='album-list'),
        ]
