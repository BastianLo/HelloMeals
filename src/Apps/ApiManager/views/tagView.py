from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from Apps.MealManager.serializers import TagMergeSerializer, TagSerializer, TagGroupSerializer
from Apps.MealManager.models import TagMerge, Tag, TagGroup

from util.pagination import RqlPagination

from Apps.MealManager.filters import TagFilters


### Views ###

@permission_classes([IsAuthenticated])
class TagMergeListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagMergeSerializer
        return TagMergeSerializer

    def get_queryset(self):
        tag_merges = TagMerge.objects.all()
        return tag_merges


@permission_classes([IsAuthenticated])
class TagListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination
    rql_filter_class = TagFilters

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagSerializer
        return TagSerializer

    def get_queryset(self):
        tags = Tag.objects.all()
        return tags

@permission_classes([IsAuthenticated])
class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    lookup_field = 'helloFreshId'

    def get_queryset(self):
        return Tag.objects.all()

@permission_classes([IsAuthenticated])
class TagGroupList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagGroupSerializer
        return TagGroupSerializer

    def get_queryset(self):
        tag_groups = TagGroup.objects.all()
        return tag_groups

