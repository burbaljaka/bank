from django.urls import path
from .views import addition, substraction, get_status, test


urlpatterns = [
    path('test/', test, name='test'),
    path('add/', addition, name='addition'),
    path('substract/', substraction, name='substraction'),
    path('get_status/', get_status, name='get_status')
]