from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Role


class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsDirector(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.objects.get(name='director')
