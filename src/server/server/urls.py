from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),
    path('segmentation/', include('segmentation.urls')),
    path('scoring/', include('scoring.urls')),
    path('admin/', admin.site.urls),
]
