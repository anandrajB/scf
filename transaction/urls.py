from django.urls import path
from .views import AB, BC, Proslistapiview, Proscreateapiview, start_draft
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('pros/', Proscreateapiview.as_view(), name='pros'),
    path('pro/', Proslistapiview.as_view(), name='pro-list'),
    # path('program/',ProgramListApiview.as_view(),name='programs-add'),
    # path('program/<int:pk>/', ProgramupdateDeleteapiview.as_view(), name="program-update"),
    path('change/<int:pk>/', start_draft, name="start"),
    path('change_AB/<int:pk>/', AB, name="AB"),
    path('change_BC/<int:pk>/', BC, name="BC"),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
]
