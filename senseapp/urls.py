from django.urls import path
from .views import sense_func

urlpatterns = [
    path('', sense_func, name='sense_func')
    ]