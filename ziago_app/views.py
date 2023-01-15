from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets, status,permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth import authenticate, login

from .models import *
from .serializers import *
from .decorators import *


class Login(viewsets.ModelViewSet):

    serializer_class = LoginSerializer

    def login(self,request):
        user_name = request.data['user_name']
        password = request.data['password']
        if user_name and password:
            user = authenticate(username=user_name,password=password)
            if user is not None:
                login(request,user)
                return Response({"msg": "User has been logged in"}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "cannot logged in"},status= status.HTTP_400_BAD_REQUEST)


class CRUD_MembersView(viewsets.ModelViewSet):
    serializer_class = MembersSerializer
    

    def get_role(self, *args, **kwargs):
        if kwargs.get('role'):
            role = Roles.objects.get(id=int(kwargs.get('role')))
            return role

    def get_queryset(self, *args, **kwargs):
        queryset = None
        if kwargs.get('pk'):
            pk =int(kwargs.get('pk'))
            if Members.objects.filter(id=pk).exists():
                queryset  =  Members.objects.get(id=pk)
                return queryset
        else:
            queryset  =  Members.objects.all()
        return queryset

    @all_admin
    @logged_in
    def list(self,request,*args, **kwargs):
        data = self.get_queryset()
        role =""
        for r in data:
            role = r.role.id
        role = self.get_role(role=role)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    @admin_only
    @operator_and_technician
    @logged_in
    def create(self, request, *args, **kwargs):
        data = request.data
        if  Members.objects.filter(member_name=data['member_name'],datamode="A").exists():
            return Response({'msg':' User already created'}, status=status.HTTP_208_ALREADY_REPORTED)
        else:
            user = User()
            user.username = data['member_name']
            user.password = make_password(data['user_secret_key'])
            role = self.get_role(role=data['role'])
            if role.role_name =="super admin":
                user.is_superuser =True
            serializer_data = self.serializer_class(data=data)
            if serializer_data.is_valid():
                serializer_data.save()
                user.save()
                return Response(serializer_data.data)
    
    @admin_only
    @all_admin
    @logged_in
    def delete(self,request,pk=None):
        if pk and Members.objects.filter(id=pk).exists():
            data_deleted = self.get_queryset(pk=pk)
            data_deleted.delete()
            return Response({'msg':'Data deleted'},status=status.HTTP_204_NO_CONTENT)


    @admin_only
    @operator_and_technician   
    @logged_in
    def update(self,request,pk):
        model_data = self.get_queryset(pk=pk)
        serializer = self.serializer_class(model_data, data=request.data,partial=True)
        if serializer.is_valid():
            current_user_id = Members.objects.get(member_name=self.request.user, datamode="A")
            if int(current_user_id.id) == int(pk):
                Members.objects.filter(id=pk).update(member_name=request.data.get('member_name'),
                # here i update the old role beacuse a user cannot change his own role as per requirement
                role = model_data.role.id,user_secret_key = request.data.get('user_secret_key')
                )
                password_update = make_password(request.data.get('user_secret_key'))
                User.objects.filter(username = model_data.member_name).update(password =password_update)
                
                return Response({'msg':'updated the old role because a user cannot change his own role'}, status=status.HTTP_200_OK)
            else:
                post__data_role_id = request.data.get('role')
                member_data = Members.objects.get(role__id=post__data_role_id)
                if member_data or str(member_data.role.role_name) not in ['super admin']:
                    serializer.save()
                    return Response({'msg':'updated the user'}, status=status.HTTP_200_OK)
                elif member_data or member_data.role.role_name in ["super admin"]:
                    return Response({'msg':'you cant updated super admin user'}, status=status.HTTP_200_OK)


    @admin_only
    @all_admin    
    @logged_in
    def read(self,request,pk):
        data = self.get_queryset(pk=pk)
        serializer = self.serializer_class(data)
        return Response(serializer.data)


# Role

class CRUD_RolesView(viewsets.ModelViewSet):
    serializer_class = RolesSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = None
        if kwargs.get('pk'):
            pk =kwargs.get('pk')
            if Roles.objects.filter(id=pk).exists():
                queryset  =  Roles.objects.get(id=pk)
                return queryset
        else:
            queryset  =  Roles.objects.all()
        return queryset

    @all_admin
    @logged_in
    def list(self,*args, **kwargs):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    @all_admin
    @logged_in
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer_data = self.serializer_class(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
    
    @all_admin
    @logged_in
    def delete(self,request,pk=None):
        if pk and Roles.objects.filter(id=pk).exists():
            data_deleted = self.get_queryset(pk=pk)
            data_deleted.delete()
        return Response({'msg':'Data deleted'},status=status.HTTP_204_NO_CONTENT)

    
    @all_admin
    @logged_in
    def update(self,request,pk):
        model_data = self.get_queryset(pk=pk)
        serializer = self.serializer_class(model_data, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    @all_admin
    @logged_in
    def read(self,request,pk):
        data = self.get_queryset(pk=pk)
        serializer = self.serializer_class(data)
        return Response(serializer.data)



# Rights

class CRUD_RightsView(viewsets.ModelViewSet):
    serializer_class = RightsSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = None
        if kwargs.get('pk'):
            pk =kwargs.get('pk')
            if Rights.objects.filter(id=pk).exists():
                queryset  =  Rights.objects.get(id=pk)
                return queryset
        else:
            queryset  =  Rights.objects.all()
        return queryset

    
    @all_admin
    @logged_in
    def list(self,*args, **kwargs):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    
    @all_admin
    @logged_in
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer_data = self.serializer_class(data=data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
    
    
    @all_admin
    @logged_in
    def delete(self,request,pk=None):
        if pk and Rights.objects.filter(id=pk).exists():
            data_deleted = self.get_queryset(pk=pk)
            data_deleted.delete()
        return Response({'msg':'Data deleted'},status=status.HTTP_204_NO_CONTENT)

    
    @all_admin
    @logged_in
    def update(self,request,pk):
        model_data = self.get_queryset(pk=pk)
        serializer = self.serializer_class(model_data, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    
    @all_admin
    @logged_in
    def read(self,request,pk):
        data = self.get_queryset(pk=pk)
        serializer = self.serializer_class(data)
        return Response(serializer.data)
