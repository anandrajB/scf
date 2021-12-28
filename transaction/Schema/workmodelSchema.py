import graphene
from graphene_django import DjangoObjectType, DjangoListField
from transaction.models import workmodel


class workmodelType(DjangoObjectType):
    class Meta:
        model = workmodel
        fields = '__all__'


class workmodelInput(graphene.InputObjectType):
    id = graphene.ID()
    description = graphene.String(required=True)
    workflow = graphene.Boolean(required=True)


class workmodelType_create(graphene.Mutation):
    class Arguments:
        _model = workmodelInput(required=True)

    workmodel1 = graphene.Field(workmodelType)

    def mutate(self, root, _model=None):
        _workmodel1 = workmodel.objects.create(**_model)
        return workmodelType_create(workmodel1=_workmodel1)


class workmodelType_update(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        description = graphene.String()
        workflow = graphene.Boolean()

    workmodel1 = graphene.Field(workmodelType)

    def mutate(self, root, description, workflow, id):
        workmodel1 = workmodel.objects.get(id=id)
        workmodel1.description = description
        workmodel1.workflow = workflow
        workmodel1.save()
        return workmodelType_update(workmodel1=workmodel1)


class workmodelType_delete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    workmodel1 = graphene.Field(workmodelType)

    def mutate(self, root, id):
        workmodel1 = workmodel.objects.get(id=id)
        workmodel1.delete()
        return workmodelType_delete(workmodel1=workmodel1)
