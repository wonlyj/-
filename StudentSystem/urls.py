from django.contrib import admin
from studentManagement import views
from django.urls import path, include
from django.urls import re_path as url
urlpatterns = [
    path('', include('studentManagement.urls', namespace='student')),
    path('student/', include('studentManagement.urls')),
    path('admin/', admin.site.urls),
    # url(r'^admin/', admin.site.urls),
    # url(r'^', include('studentManagement.urls', namespace='student'))
    path('studentinformation/', views.new_studentinformation, name='new_studentinformation'),
]
