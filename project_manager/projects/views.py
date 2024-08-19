from rest_framework import viewsets
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import filters
from django.db.models import Count
from .utils.notifications import send_telegram_message
from .permissions import IsAdminOrOwner, IsOwner
from rest_framework.permissions import IsAuthenticated

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    
    def perform_create(self, serializer):
        # Automatically assign the current user as the owner
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        """
        Optionally restricts the returned projects to the ones owned by the user
        if they are not an admin.
        """
        user = self.request.user
        if user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(owner=user)
    
    @action(detail=True, methods=['get'])
    def task_status_report(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.values('status').annotate(count=Count('id'))
        return Response(tasks)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        queryset = project.tasks.all()
        
        # Filtering by status and priority
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        serializer.save(project=project)

class TaskOverdueReportView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        overdue_tasks = Task.objects.filter(deadline__lt=timezone.now().date(), status__in=['new', 'in_progress'])
        serializer = TaskSerializer(overdue_tasks, many=True)
        # Send notification if there are overdue tasks
        if overdue_tasks.exists():
            message = "Overdue tasks detected:\n"
            for task in overdue_tasks:
                message += f"- {task.name} (Deadline: {task.deadline})\n"
            send_telegram_message(message)
        return Response(serializer.data)
