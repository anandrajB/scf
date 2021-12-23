from django.urls import path
from .views import ProgramtypeupdateDeleteapiview , programtypelistapiview , ProgramListApiview , ProgramupdateDeleteapiview
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('programtype/', programtypelistapiview.as_view(), name="program list view"),
    path('programtype/<int:pk>/', ProgramtypeupdateDeleteapiview.as_view(), name="program list view update"),
    path('program/', ProgramListApiview.as_view(), name="program list "),
    path('program/<int:pk>/', ProgramupdateDeleteapiview.as_view(), name="program-update"),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]