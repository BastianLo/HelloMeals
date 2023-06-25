from Apps.MealManager.filters import TagFilters
from Apps.MealManager.models import TagMerge, Tag, TagGroup
from Apps.MealManager.serializers import TagMergeSerializer, TagSerializer, TagGroupSerializer, TagGroupFullSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from util.pagination import RqlPagination


### Views ###

@permission_classes([IsAuthenticated, IsAdminUser])
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


@permission_classes([IsAuthenticated])
class TagGroupFullList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = RqlPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagGroupFullSerializer
        return TagGroupFullSerializer

    def get_queryset(self):
        tags = TagGroup.objects.all()
        return tags
