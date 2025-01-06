from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('workers', views.workers, name='workers'),
    path('delete_worker/<int:w_id>', views.delete_worker, name='workers'),
]