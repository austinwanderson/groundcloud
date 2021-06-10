from django.contrib import admin
from django.urls import path
from gcinterview import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drivers/', views.list_drivers),
    path('companies/', views.list_companies),
    path('trucks/', views.list_trucks),
    path('driver/create', views.create_driver),
    path('company/create', views.create_company),
    path('truck/create', views.create_truck),
    path('driver/<int:pk>/', views.driver_detail),
    path('company/<int:pk>/', views.company_detail),
    path('truck/<int:pk>/', views.truck_detail),
    path('truck/closest', views.get_closest_truck),
]

urlpatterns = format_suffix_patterns(urlpatterns)