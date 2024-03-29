from rest_framework.permissions import BasePermission, SAFE_METHODS
from shopAuth.models import Role


class IsAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsStorekeeper(BasePermission):

    def has_object_permission(self, request, view, obj):
        # if request.method in SAFE_METHODS:
        #     return True

        return request.user.role == Role.objects.get(name='storekeeper')


class IsSeller(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.objects.get(name='seller')


class IsMerchandiserOrAuthenticatedReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True

        return request.user.role == Role.objects.get(name='merchandiser')


class IsMerchandiser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.objects.get(name='merchandiser')


class IsDirector(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.objects.get(name='director')


class IsGK(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.objects.get(name='GK')
