from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('pre_register/', views.PreRegisterView.as_view(), name='pre_register'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
