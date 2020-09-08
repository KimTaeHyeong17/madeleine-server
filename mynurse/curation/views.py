from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from newsletters.models import NewsLetter, Tag

from .serializers import CurationSerializer, CurationPageSerializer
from .models import Curation, CurationPage
# Create your views here.
class CurationViewSet(viewsets.ModelViewSet):
    queryset = Curation.objects.all()
    serializer_class = CurationSerializer

class CurationPageViewSet(viewsets.ModelViewSet):
    queryset = CurationPage.objects.all()
    serializer_class = CurationPageSerializer

@api_view(['POST'])
def get_curation(request):
    curation_page = request.data['curation_pk']
    try:
        page = CurationPage.objects.get(id=curation_page)

        curation_queryset= Curation.objects.filter(curation_page=page)
        curations = []
        tags = set()
        for curation in curation_queryset:
            curations.append({
                'curation_pk'           : curation.id,
                'curation_title'        : curation.title,
                'curation_explain'      : curation.explain,
                'curation_newsletter_pk'   : curation.newsletter.id
            })
            newsletter = NewsLetter.objects.get(id=curation.newsletter.id)
            for tag in newsletter.tags.all():
                tags.add(tag.name)
                
        
        image = str(page.image)
        if image[0] != '/':
            image = '/' + image
        status = 'S00'
        message = 'Curation Page'
        value = {
            'page_pk'               : page.id,
            'page_title'            : page.title,
            'page_content'          : page.content,
            'page_intro_title'      : page.intro_title,
            'page_intro_content'    : page.intro_content,
            'page_image'            : request.build_absolute_uri('/media' + image),
            'curations'             : curations,
            'page_tags'             : tags
        }
    
    except:
        status = 'E00'
        message = 'Wrong Curation Number'
        value = curation_page

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }

    return Response(response)

@api_view(['POST'])
def all_curation(request):
    page_queryset = CurationPage.objects.all()

    pages = []

    for page in page_queryset:
        tags = set()
        curations = Curation.objects.filter(curation_page=page)
        for curation in curations:
            for tag in curation.newsletter.tags.all():
                tags.add(tag.name)

        image = str(page.image)
        if image[0] != '/':
            image = '/' + image
        pages.append({
            'page_pk'               : page.id,
            'page_title'            : page.title,
            'page_content'          : page.content,
            'page_intro_title'      : page.intro_title,
            'page_intro_content'    : page.intro_content,
            'page_image'            : request.build_absolute_uri('/media' + image),
            'page_tags'             : tags
        })

    response = {
        'status'    : 'S00',
        'message'   : 'GET All Curation Pages',
        'value'     : pages
    }

    return Response(response)
