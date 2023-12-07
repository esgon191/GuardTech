from django.contrib import admin
from django.urls import path
from .views import index_page
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('process/', views.process, name='process'),
    path('process_file_path/', views.process_file_path, name='process_file_path'),
    path('save_to_excel/', views.save_to_excel, name='save_to_excel'),
]