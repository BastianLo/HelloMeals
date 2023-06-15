import django_filters
from Apps.MealManager.models import Ingredient, RecipeIngredient
from Apps.MealManager.serializers import IngredientSerializer
from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from util.pagination import RqlPagination


class IngredientFilterSet(filters.FilterSet):
    srch = django_filters.CharFilter(method='filter_search')
    ordering = django_filters.OrderingFilter(fields=['name'])

    def filter_search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Ingredient
        fields = ['srch']


@permission_classes([IsAuthenticated])
class IngredientList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination
    filterset_class = IngredientFilterSet

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
        queryset = Ingredient.objects.filter(parent=None)

        usage_count_param = self.request.query_params.get('usage_count')
        if usage_count_param:
            try:
                usage_count = int(usage_count_param)
                ingredient_ids = RecipeIngredient.objects.values('ingredient').annotate(
                    count=Count('ingredient')).filter(count__gte=usage_count).values_list('ingredient', flat=True)
                queryset = queryset.filter(helloFreshId__in=ingredient_ids)
            except ValueError:
                pass

        return queryset


@permission_classes([IsAuthenticated])
class stockList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination
    filterset_class = IngredientFilterSet

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
        user = self.request.user
        if user.profile.stock:
            return user.profile.stock.ingredients
        else:
            return Ingredient.objects.none()


@permission_classes([IsAuthenticated])
class shoppingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination
    filterset_class = IngredientFilterSet

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
        user = self.request.user
        if user.profile.stock and user.profile.stock.shoppinglist:
            return user.profile.stock.shoppinglist.ingredients
        else:
            return Ingredient.objects.none()


@api_view(['POST'])
def assign_ingredient_parent(request, helloFreshId, parentId=None):
    try:
        source = Ingredient.objects.get(helloFreshId=helloFreshId)
    except Ingredient.DoesNotExist:
        return Response({'error': 'Recipe not found'}, status=404)
    try:
        parent = Ingredient.objects.get(helloFreshId=parentId)
    except:
        parent = None
    if parent is not None and parent.parent is not None:
        return Response({'error': 'Can not assign a parent which is already a child'}, status=400)

    source.parent = parent
    source.save()
    response = {
        'message': 'Ingredient assigned successfully',
        'helloFreshId': helloFreshId,
    }

    return Response(response)
