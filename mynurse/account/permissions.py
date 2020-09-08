from rest_framework import permissions

class IsMeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj.username , ' ', request.user)
        return obj.username == str(request.user)