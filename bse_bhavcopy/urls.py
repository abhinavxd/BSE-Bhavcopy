from django.contrib import admin
from django.urls import path, include
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-data-by-name', api_views.search_name),
    path('', include('frontend.urls'))
]
