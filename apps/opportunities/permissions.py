from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOpportunityOwnerOrAdmin(BasePermission):
    message = "Only the opportunity owner or an administrator can modify it."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (
            obj.owner_id == request.user.pk
            or request.user.is_staff
        )
