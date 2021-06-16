from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.datasets),
    path('datasets/<str:dataset_id>', views.dataset),
    path('downloads/<str:dataset_id>', views.downloads),
    path('accounts/', include('django.contrib.auth.urls')),
]
