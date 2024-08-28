from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('trovaMatricole/', include("ManagerRilievoMatricole.urls")),
    path('admin/', admin.site.urls),

]
