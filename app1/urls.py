from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('display_register',views.display_register),
    path('register',views.register),
    path('register_success',views.register_success),
    path('login',views.login),
    path('login_success',views.login_success),
    path('logout',views.logout),
    path('create_item',views.create_item),
    path('show_create_item',views.show_create_item),
    path('remove_item/<int:id>',views.remove_item),
    path('delete_item/<int:id>',views.delete_item),
    path('display_item/<int:id>',views.display_item),
    path('add_to_wishlist/<int:id>',views.add_to_wishlist)



   
]
