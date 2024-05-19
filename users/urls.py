"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin-panel'),
    path('add-panel/', views.add_panel, name='add-panel'),
    path('user/edit_panel/<int:order_id>/<int:user_id>/', views.edit_panel, name='edit_panel'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<str:category_name>/', views.delete_category, name='delete_category'),
    path('user/edit_category/<str:category_name>/', views.edit_category, name='edit_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('user/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/edit_sold/<int:order_item_id>/', views.edit_sold, name='edit_sold'),
    path('delete_sold/<int:order_item_id>/', views.delete_sold, name='delete_sold'),
]
