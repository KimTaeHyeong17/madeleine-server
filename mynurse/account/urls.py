from django.urls import path

from .views import mail, get_user, profile, login_view, create_user, update_user
from .views import register_like_tags, delete_like_tags, confirm_mail, get_subscribes, get_tag_recommend, subscribe_register, subscribe_remove
from .views import find_username, change_password

urlpatterns = [
    path('mail/send/', mail),
    path('mail/confirm/', confirm_mail),
    
    path('create/', create_user),
    path('update/', update_user),
    path('user/', get_user),
    path('login/', login_view),
    path('subscribes/get/', get_subscribes),
    path('subscribes/post/', subscribe_register),
    path('subscribes/delete/', subscribe_remove),
    path('tag_recommend/', get_tag_recommend),
    path('find_username/', find_username),
    path('change_password/', change_password),

    #path('health/create/', create_health),
    #path('health/pregnant_update/', update_health),
    #path('health/surgery_update/', update_surgery),
    #path('health/allgery_update/', update_allgery),

    path('register_tags/', register_like_tags),
    path('delete_tags/', delete_like_tags),   
]