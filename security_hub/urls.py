from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('workers', views.workers, name='workers'),
    path('delete_worker/<int:w_id>', views.delete_worker, name='delete_worker'),
    path('add_worker', views.AddWorker.as_view(), name='add_worker'),
    path('worker/<int:w_id>/card/', views.worker_card, name='worker_card'),
    path('worker/<int:w_id>/card/add', views.add_worker_card, name='add_worker_card'),
    path('api/register-card/<str:card>/', views.register_card, name='register_card'),
    path('api/check_card_status/<int:card_change_id>/', views.check_card_status, name='check_card_status'),
    path('api/validate-card-scan/', views.validate_card_scan, name='validate_card_scan'),
]