from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token-requests/', obtain_auth_token, name='token-requests'),
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
