from django.contrib import admin
from django.urls import path, include
from monitor.views import root_view

urlpatterns = [
    path('', root_view, name='root'),  # Add this line for root URL
    path('admin/', admin.site.urls),
    path('api/', include('monitor.urls')),
]

