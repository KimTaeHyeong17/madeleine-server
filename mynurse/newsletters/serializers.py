from rest_framework import serializers
from rest_framework.response import Response
from .models import NewsLetter, Tag, Episode

class NewsLetterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsLetter
        fields = ['url', 'newsletter_name', 'id', 'explain', 'tags', 'register_url', 'image', 'followers']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name', 'image']

class EpisodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Episode
        fields = ['url', 'id', 'newsletter', 'title', 'date', 'episode_url']
