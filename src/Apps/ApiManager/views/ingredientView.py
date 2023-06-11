from Apps.MealManager.models import Ingredient
from Apps.MealManager.serializers import IngredientSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from util.pagination import RqlPagination


@permission_classes([IsAuthenticated])
class IngredientList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            fields = self.request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                meta = IngredientSerializer.Meta
                meta.exclude = None
                meta.fields = fields
                return type('DynamicRecipeBaseSerializer', (IngredientSerializer,), {'Meta': meta})
            else:
                return IngredientSerializer
        return IngredientSerializer

    def get_queryset(self):
        recipes = Ingredient.objects.all()
        return recipes
