from django.shortcuts import render
from django.contrib.auth import authenticate

from .serializers import VaccinSerializer
from .models import Vaccine
from .permissions import IsOwnerOrReadOnly

from account.models import User
from .models import Vaccine

from rest_framework import viewsets, generics, renderers, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

# Create your views here.
'''
해당 유저 백신 다가져오는 걸로
input   : username
'''
@api_view(['POST'])
def get_vaccine(request):
    username = request.data['username']
    user = User.objects.get(username=username)
    
    try:
        vaccine = Vaccine.objects.filter(owner=user)
    except:
        response = {
            'status'    : 'S00',
            'message'   : 'No Vaccine',
            'value'     : ''
        }
        return Response(response)
    vaccines = []

    for v in vaccine:
        vaccines.append({
            'id'        : v.id,
            'vaccine'   : v.vaccine,
            'date'      : v.date,
            'hospital'  : v.hospital
        })

    response = {
        'status'    : 'S00',
        'message'   : 'Success GET Vaccine',
        'value'     : vaccines
    }
    return Response(response)

@api_view(['POST'])
def delete_vaccine(request):
    #user = authenticate(username=request.data['username'], password=request.data['password'])
    username = request.data['username']
    user = User.objects.get(username=username)
    pk = request.data['vaccine_id']

    try:
        pk = request.data['vaccine_id']
    except:
        response = {
            'status'    : 'E00',
            'message'   : 'No Vaccine_ID',
            'value'     : ''
        }
        return Response(response)
    try:
        vaccine = Vaccine.objects.get(pk=pk)
    except:
        response = {
            'status'    : 'E00',
            'message'   : 'Not Valid vaccine_id',
            'value'     : ''
        }
        return Response(response)

    if user != vaccine.owner:
        response = {
            'status'    : 'E00',
            'message'   : 'Only Access Your Vaccine',
            'value'     : ''
        }
        return Response(response)

    vaccine.delete()
    response = {
        'status'    : 'S00',
        'message'   : 'Success DELETE Vaccine',
        'value'     : ''
    }
    return Response(response)

class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            status = 'S00'
            message = 'Object Create Success'
            value = ''
        except:
            status = 'E00'
            message = 'Wrong Object Attribute'
            value = ''
        response = {
            'status'    : status,
            'message'   : message,
            'value'     : value
        }
        return Response(response)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
'''
    @api_view(['POST'])
    def retrieve(request):
        vaccine_id = request.data['vaccine_id']
        try:
            vaccine = Vaccine.objects.get(id=vaccine_id)
            status = 'S00'
            message = 'GET Vaccine Success'
            value = {
                'id'    : vaccine.id,
                'name'  : vaccine.vaccine,
                'date'  : vaccine.date,
                'hospital'  : vaccine.hospital
            }
        except:
            status = 'E00'
            message = 'Wrong Vaccine ID'
            value = ''
        response = {
            'status'    : status,
            'message'   : message,
            'value'     : value
        }
        return Response(response)

    @api_view(['POST'])
    def destroy(request):
        vaccine_id = request.data['vaccine_id']
        try:
            vaccine = Vaccine.objects.get(id=vaccine_id)
            vaccine.delete()
            status = 'S00'
            message = 'DELETE Success'
            value = ''
        except:
            status = 'E00'
            message = 'Wrong Vaccine ID'
            value = ''
        response = {
            'status'    : status,
            'message'   : message,
            'value'     : value
        }
        return Response(response)
'''    

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'vaccines' : reverse('vaccine-list', request=request, format=format),
        'users' : reverse('user-list', request=request, format=format)
    })