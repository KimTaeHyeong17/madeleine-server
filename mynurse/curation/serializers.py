from rest_framework import serializers
from rest_framework.response import Response
from .models import Curation, CurationPage

class CurationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Curation
        fields = ['url', 'id', 'title', 'explain', 'newsletter', 'curation_page']

class CurationPageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurationPage
        fields = ['url', 'id', 'title', 'content', 'intro_title', 'intro_content', 'image']
        