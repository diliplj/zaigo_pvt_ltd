from django.forms import ValidationError
from .models import *
from rest_framework import serializers
from django.db.models import Q

from django.contrib.auth.hashers import make_password

class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True,label='User name')
    password = serializers.CharField(style={'input_type': 'password', 'required': False, 'custom_type': 'PasswordField'}, required=False, label='Your Secret Key')

    def validate(self, data):
        if data['user_name'] and data['password'] and Members.objects.filter(member_name=data['user_name'],user_secret_key=data['password']).exists():
            return data
        else:
            raise serializers.ValidationError('User / secret key Wrong')



class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['member_name','role','user_secret_key']




class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Roles
        fields = ['role_name']

class RightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rights
        fields = ['role','rights'] 

