from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('workers', views.workers, name='workers'),
    path('delete_worker/<int:w_id>', views.delete_worker, name='delete_worker'),
    path('add_worker', views.AddWorker.as_view(), name='add_worker'),
]