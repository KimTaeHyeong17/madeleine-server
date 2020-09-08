from rest_framework import serializers
from rest_framework.response import Response
from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'birth', 'gender', 'first_name', 'last_name', 'like_tags', 'subscribes']
        
    def  create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            birth=validated_data['birth'],
            gender=validated_data['gender']
        )
        user.set_password(validated_data['password'])
        user.save()
        print('serializer')
        return user