# permissions.py

from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow administrators to edit all projects,
    but regular users can only edit their own projects.
    """

    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user and request.user.is_staff:
            return True
        
        # Regular users can only access their own projects
        return obj.owner == request.user

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own tasks.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'project'):
            # obj is a Task, check if the task belongs to a project owned by the user
            return obj.project.owner == request.user
        else:
            # obj is a Project, check if the project is owned by the user
            return obj.owner == request.user
