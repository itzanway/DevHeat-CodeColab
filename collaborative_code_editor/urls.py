from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from code_editor.views import health_check



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('code_editor.urls')), # url for code editor app
    path('', health_check),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)