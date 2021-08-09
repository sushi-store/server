from django.urls import path
from . import views


app_name = 'order_api'

urlpatterns = [
    path('', views.OrdersList.as_view()),
    path('create', views.CreateOrder.as_view()),
    path('<int:pk>', views.OrderDetailId.as_view()),
]
