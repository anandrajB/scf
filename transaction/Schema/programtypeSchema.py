import graphene
from graphene_django import DjangoObjectType
from transaction.models import ProgramType


class Program_Type(DjangoObjectType):
    class Meta:
        model = ProgramType
        fields = '__all__'


class createProgramType(graphene.Mutation):
    class Arguments:
        description = graphene.String(required=True)

    _program_type = graphene.Field(Program_Type)

    def mutate(self, root, description):
        _programtype = ProgramType.objects.create(description=description)
        return createProgramType(_program_type=_programtype)


class updateProgramType(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        description = graphene.String(required=True)

    _program_type = graphene.Field(Program_Type)

    def mutate(self, root, id, description):
        _programtype = ProgramType.objects.get(id=id)
        _programtype.description = description
        _programtype.save()
        return updateProgramType(_program_type=_programtype)


class deleteProgramType(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    _program_type = graphene.Field(Program_Type)

    def mutate(self, root, id):
        _programtype = ProgramType.objects.get(id=id)
        _programtype.delete()
        return deleteProgramType(_program_type=_programtype)
