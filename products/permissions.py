from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Oddiy foydalanuvchi faqat GET/HEAD/OPTIONS qila oladi.
    Admin esa barcha amallarni qila oladi.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.is_staff
        )
