from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login_history/', views.login_history, name='login_history'),
    path('get_last_order/', views.get_last_order_id, name='get_last_order_id'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_customer/', views.create_customer, name='create_customer'),
]