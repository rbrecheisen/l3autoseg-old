from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('accounts/', include('django.contrib.auth.urls')),
]
