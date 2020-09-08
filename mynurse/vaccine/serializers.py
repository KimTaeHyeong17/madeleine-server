from rest_framework import serializers

from account.models import User

from .models import Vaccine

class VaccinSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='User.username')
    class Meta:
        model = Vaccine
        fields = ['url', 'id', 'owner', 'vaccine', 'date', 'hospital']