from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
# from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from rest_framework.response import *
from rest_framework import status

import sys

def get_rights(self,logged_user_role):
    role_rights = []
    all_rights = Rights.objects.all().filter(role__role_name=logged_user_role)
    for right in all_rights:
        role_rights.append(str(right.rights))
    return role_rights


def logged_in(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                return func(self,request,*args, **kwargs)
            else:
                return redirect('login')
                
        except Exception as e:
            print("e  ",e)
            return JsonResponse({'msg':"check the Error "})
    
    return wrapper


def admin_only(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            url = str(request.get_full_path()).split('/')[1]
            if url != 'create':

                url_id = int(kwargs.get('pk',None))
                post_data_role =int(self.request.data.get('role')) if self.request.data else None
                if request.user.is_authenticated:
                    current_logged_user_role = Members.objects.get(member_name= request.user,datamode="A")
                    logged_user_role = current_logged_user_role.role.role_name
                    logged_user_rights = get_rights(self,logged_user_role)
                    
                    # if url_id and url in ['update']:
                    #     if int(url_id) == int(current_logged_user_role.id):
                    #         return Response({
                    #         'msg' : 'Hi you dont have access to edit your own id'
                    #         },status=status.HTTP_401_UNAUTHORIZED)
                
                    if url_id and url in logged_user_rights:
                        url_id_data = Members.objects.get(id= url_id,datamode="A")
                        post_data_role = url_id_data.role.id
                        if str(logged_user_role) == str(url_id_data.role.role_name) and url in ['destory']:
                            return Response({
                            'msg' : 'Hi  you dont have access to Delete same role user'
                            },status=status.HTTP_401_UNAUTHORIZED)
    
                    post_data_role = Roles.objects.get(id=post_data_role)
                                
                    if logged_user_role == 'admin' and post_data_role.role_name == 'super admin' and url in logged_user_rights:
                        return Response({
                            'msg' : 'Hi Admin you dont have access to Update or Delete or View Super admin user'
                        },status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return func(self,request, *args, **kwargs) 
                else:
                    return redirect('login')
            elif url == "create":
                return func(self,request, *args, **kwargs)
        
        except Exception as e:
            print("e ",e)
            return Response({'msg':'error in line 66 decorator or No data found'},status=status.HTTP_303_SEE_OTHER)
    return wrapper

def all_admin(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            url = str(request.get_full_path()).split('/')[1]
            check_role = Members.objects.get(member_name= self.request.user,datamode="A")
            role = str(check_role.role.role_name)
            technicians_rights = get_rights(self,role)
            if role in ['admin','super admin']:
                return func(self,request, *args, **kwargs)
            elif role in ['technicians'] and url =="read" and url in technicians_rights:
                read_url_id_role = int(kwargs.get('pk',0))
                check_post_id_role = Members.objects.get(id= read_url_id_role,datamode="A")
                if str(check_post_id_role.role.role_name) == str(role):
                    return func(self,request, *args, **kwargs)
                else:
                    return Response({'msg':'You dont have access to view admins detail'}, status=status.HTTP_401_UNAUTHORIZED)


            else:
                return Response({'msg':'Only admin and super admin only have access . others dont have access'}, status=status.HTTP_401_UNAUTHORIZED)
            

        except Exception as e:
            print("error  all admin decorator",e)
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            return HttpResponse(exc_traceback.tb_lineno,e)
    return wrapper



def operator_and_technician(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            url = str(request.get_full_path()).split('/')[1]
            if self.request.user.is_authenticated:
                check_role = Members.objects.get(member_name= self.request.user,datamode="A")
                role = str(check_role.role.role_name)
                right = get_rights(self,role)
                if role in ['operators','operator'] and url in right:
                    if url == "create":
                        #create page
                        post_data_role_id =int(self.request.data.get('role')) if self.request.data else None
                        post_data_role = Roles.objects.get(id=post_data_role_id)
                        if str(post_data_role.role_name) not in ["technicians","technician"]:
                            return Response({'msg':'Hi Operator you have access to create technicians only not admins'},
                            status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            return func(self,request, *args, **kwargs)
                    else:
                        # edit page
                        url_id = int(kwargs.get('pk',None))
                        url_id_data = Members.objects.get(id= url_id,datamode="A")
                        post_data_role = str(url_id_data.role.role_name)
                        if post_data_role not in ["technicians","technician"]:
                            return Response({'msg':'Hi Operator you have access to EDIT technicians only not admins'},
                            status=status.HTTP_401_UNAUTHORIZED)

                elif role not in ['operator','technicians']:
                    return func(self,request, *args, **kwargs)
                    
            else:
                return Response({'msg':'you got error in operator_and_technician decorator '}, status=status.HTTP_306_RESERVED)

        except Exception as e:
            print("error in ",e)
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            return Response({'msg':'Error got in operator_and_technician decorator '},status=status.HTTP_404_NOT_FOUND)
    return wrapper