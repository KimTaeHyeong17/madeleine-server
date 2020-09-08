from django.urls import path

from .views import get_curation, all_curation

urlpatterns = [
    path('get/', get_curation),
    path('all/', all_curation)
]