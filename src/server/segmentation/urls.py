from django.urls import path, include
from . import views


urlpatterns = [
    # HTML
    path('', views.index),
    path('datasets/', views.datasets),
    path('datasets/<str:dataset_id>', views.dataset),
    path('accounts/', include('django.contrib.auth.urls')),
    # REST API
]
