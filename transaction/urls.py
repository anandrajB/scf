from django.urls import path
from .views import ProgramListApiview, ProgramupdateDeleteapiview
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('program/', ProgramListApiview.as_view(), name="program list "),
    path('program/<int:pk>/', ProgramupdateDeleteapiview.as_view(),
         name="program-update"),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]
