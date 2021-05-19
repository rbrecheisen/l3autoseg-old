from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('models/', views.models),
    path('models/<str:model_id>', views.model),
    path('datasets/', views.datasets),
    path('datasets/<str:dataset_id>', views.dataset),
    path('jobs/', views.jobs),
    path('jobs/<str:job_id>', views.job),
    path('results/', views.results),
    path('results/<str:result_id>', views.result),
    path('accounts/', include('django.contrib.auth.urls')),
]
