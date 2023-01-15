from django.urls import path
from .views import *

urlpatterns = [
    path('login/',Login.as_view({'post':'login'}),name="login"),

    #member viewset
    path('list/',CRUD_MembersView.as_view({'get':'list'}),name="list"),
    path('create/',CRUD_MembersView.as_view({'post':'create'}),name="create"),
    path('update/<str:pk>/',CRUD_MembersView.as_view({'post':'update'}),name="update"),
    path('destory/<str:pk>/',CRUD_MembersView.as_view({'DELETE':'delete'}),name="delete"),
    path('read/<str:pk>/',CRUD_MembersView.as_view({'get':'read'}),name="read"),


    #Role viewset
    path('role/list/',CRUD_RolesView.as_view({'get':'list'}),name="role_list"),
    path('role/create/',CRUD_RolesView.as_view({'post':'create'}),name="role_create"),
    path('role/update/<str:pk>/',CRUD_RolesView.as_view({'post':'update'}),name="role_update"),
    path('role/destory/<str:pk>/',CRUD_RolesView.as_view({'DELETE':'delete'}),name="role_delete"),
    path('role/read/<str:pk>/',CRUD_RolesView.as_view({'get':'read'}),name="role_read"),

    #Rights viewset
    path('rights/list/',CRUD_RightsView.as_view({'get':'list'}),name="rights_list"),
    path('rights/create/',CRUD_RightsView.as_view({'post':'create'}),name="rights_create"),
    path('rights/update/<str:pk>/',CRUD_RightsView.as_view({'post':'update'}),name="rights_update"),
    path('rights/destory/<str:pk>/',CRUD_RightsView.as_view({'delete':'delete'}),name="rights_delete"),
    path('rights/read/<str:pk>/',CRUD_RightsView.as_view({'get':'read'}),name="rights_read")
]
