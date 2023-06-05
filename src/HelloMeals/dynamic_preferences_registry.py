from dynamic_preferences.api.viewsets import GlobalPreferencesViewSet
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import BooleanPreference
from dynamic_preferences.users.registries import user_preferences_registry
from dynamic_preferences.users.viewsets import UserPreferencesViewSet
from rest_framework.response import Response


class CustomUserPreferencesViewSet(UserPreferencesViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response([dict(serializer.data[i], id=queryset[i].id) for i in range(len(queryset))])

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.filter(user=request.user).first()
        if instance is not None:
            serializer = self.get_serializer(instance)
            response_data = serializer.data
            response_data['id'] = instance.pk
            return Response(response_data)
        else:
            return Response({'detail': 'Nicht gefunden.'}, status=404)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.filter(user=request.user).first()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'detail': 'Nicht gefunden.'}, status=404)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CustomGlobalPreferencesViewSet(GlobalPreferencesViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response([dict(serializer.data[i], id=queryset[i].id) for i in range(len(queryset))])

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.filter(id=kwargs['pk']).first()
        if instance is not None:
            serializer = self.get_serializer(instance)
            response_data = serializer.data
            response_data['id'] = instance.pk
            return Response(response_data)
        else:
            return Response({'detail': 'Nicht gefunden.'}, status=404)

    def update(self, request, *args, **kwargs):
        instance = self.queryset.filter(id=kwargs['pk']).first()
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'detail': 'Nicht gefunden.'}, status=404)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# we create some section objects to link related preferences together

general = Section('general')
scraper = Section('scraper')


# We start with a global preference
@global_preferences_registry.register
class ScraperDownloadRecipeImages(BooleanPreference):
    help_text = 'Download images for recipes'
    section = scraper
    name = 'Download_Recipe_Images'
    default = True


@global_preferences_registry.register
class ScraperDownloadIngredientImages(BooleanPreference):
    help_text = 'Download images for ingredients'
    section = scraper
    name = 'Download_Ingredient_Images'
    default = False


@global_preferences_registry.register
class ScraperDownloadProcessStepImages(BooleanPreference):
    help_text = 'Download images for process steps'
    section = scraper
    name = 'Download_Process_Step_Images'
    default = False


# now we declare a per-user preference
@user_preferences_registry.register
class CommentNotificationsEnabled(BooleanPreference):
    name = 'comment_notifications_enabled'
    default = True
