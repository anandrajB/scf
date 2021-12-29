from django.urls import path
from .views import Proslistapiview, Proscreateapiview
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('pros/', Proscreateapiview.as_view(), name='pros'),
    path('pro/', Proslistapiview.as_view(), name='pro-list'),
    # path('program/',ProgramListApiview.as_view(),name='programs-add'),
    # path('program/<int:pk>/', ProgramupdateDeleteapiview.as_view(), name="program-update"),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]
