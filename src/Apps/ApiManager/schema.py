import graphene
from graphene_django import DjangoObjectType

from Apps.MealManager.models import Recipe


class MyModelType(DjangoObjectType):
    class Meta:
        model = Recipe
        filter_fields = {
            'helloFreshId': ('exact', 'startswith', 'contains'),
            'name': ('exact', 'contains', 'full_text_search'),
            'description': ('exact', 'contains', 'full_text_search'),
        }

class Query(graphene.ObjectType):
    mymodels = graphene.List(MyModelType)

    def resolve_mymodels(self, info, **kwargs):
        return Recipe.objects.all()

schema = graphene.Schema(query=Query)