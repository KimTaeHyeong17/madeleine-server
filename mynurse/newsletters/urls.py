from django.urls import path

from .views import get_tags, search, get_newsletter_from_tag, get_newsletter, post_newsletter, famous_newsletter, register_newsletter_page, register_newsletter
from .views import get_episode
from .views import update_newsletter_image, upload_episode

urlpatterns = [
    path('tags/', get_tags),
    path('search/', search),
    path('have_tag/', get_newsletter_from_tag),
    path('get/', get_newsletter),
    path('post/', post_newsletter),
    path('famous/', famous_newsletter),
    path('test/', update_newsletter_image),
    path('episode/get/', get_episode),
    path('register/', register_newsletter_page, name='register_page'),
    path('register/post/', register_newsletter, name='register_newsletter'),
]