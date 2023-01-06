from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('AdminPanel/', include('AdminPanel.urls')),
    path('', include('AdminPanel.urls')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
