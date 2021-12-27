#Altered Schema
import graphene
from graphene_django import DjangoObjectType
from transaction.models import submodels


class SubmodelType(DjangoObjectType):
    class Meta:
        model = submodels
        fields = '__all__'


class create_submodels(graphene.Mutation):
    class Arguments:
        description = graphene.String()
        api_route = graphene.String()

    submodel = graphene.Field(SubmodelType)

    def mutate(root, self, description, api_route):
        _submodel = submodels.objects.create(
            description=description, api_route=api_route)
        return create_submodels(submodel=_submodel)


class update_submodel(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        description = graphene.String()
        api_route = graphene.String()

    submodel = graphene.Field(SubmodelType)

    def mutate(self, root, id, description, api_route):
        _submodel = submodels.objects.get(id=id)
        _submodel.description = description
        _submodel.api_route = api_route
        _submodel.save()
        return update_submodel(submodel=_submodel)


class delete_submodel(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    submodel = graphene.Field(SubmodelType)

    def mutate(self, root, id):
        _submodel = submodels.objects.get(id=id)
        _submodel.delete()
        return delete_submodel(submodel=_submodel)
