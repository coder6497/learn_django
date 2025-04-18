from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
]
