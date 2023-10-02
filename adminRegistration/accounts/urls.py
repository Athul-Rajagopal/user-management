from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('admin_panel', views.admin_panel, name='admin_panel'),

    path('update_user/<int:user_id>/', views.update_user , name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user , name='delete_user'),
    path('create_user', views.create_user, name='create_user')
]