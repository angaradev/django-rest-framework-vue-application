from django.urls import path
from users.api.views import CurrentUserAPIVeiw


urlpatterns = [
        path('user/', CurrentUserAPIVeiw.as_view(), name='current-user'),
        ]
