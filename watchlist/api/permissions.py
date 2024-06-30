""" Custom permission class to allow only admin to edit the data """
from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    """ Custom permission class to allow only admin to edit the data"""

    def has_permission(self, request, view):
        """ Check if the user is admin or not"""
        # return request.method in permissions.SAFE_METHODS or request.user.is_staff
        # or
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method in permissions.SAFE_METHODS or admin_permission


class ReviewUserOrReadOnly(permissions.BasePermission):
    """ Custom permission class to allow only admin to edit the data"""

    def has_object_permission(self, request, view, obj):
        """ Check if the user is admin or not,
        for review check the user is the owner of the review, and he is only allowed to edit the review """
        if request.method in permissions.SAFE_METHODS:
            # get, head, options
            return True
        else:
            # post, put, patch, delete
            return obj.user == request.user
