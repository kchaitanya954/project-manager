from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Project, Task
from django.contrib.auth.models import User

class ProjectTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # JWT token authentication
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.token = response.data['access']

        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create a project
        self.project = Project.objects.create(
            name="Test Project",
            description="Description for Test Project",
            owner=self.user
        )

    def test_create_project(self):
        url = reverse('project-list')
        data = {'name': 'New Project', 'description': 'New project description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_project_list(self):
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_project(self):
        url = reverse('project-detail', args=[self.project.id])
        data = {'name': 'Updated Project', 'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Project')

    def test_delete_project(self):
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.project = Project.objects.create(
            name="Test Project",
            description="Description for Test Project",
            owner=self.user
        )

    def test_create_task(self):
        url = reverse('task-list', args=[self.project.id])
        data = {
            'name': 'Task 1',
            'description': 'Task 1 description',
            'status': 'new',
            'priority': 'high',
            'deadline': '2024-08-20'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks(self):
        Task.objects.create(
            project=self.project,
            name="Task 1",
            description="Task 1 description",
            status="new",
            priority="medium",
            deadline="2024-08-20"
        )

        url = f'{reverse("task-list", args=[self.project.id])}?status=new'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_tasks_by_status(self):
        Task.objects.create(
            project=self.project,
            name="Task 1",
            description="Task 1 description",
            status="new",
            priority="medium",
            deadline="2024-08-20"
        )
        url = f'{reverse("task-list", args=[self.project.id])}?status=new'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_task(self):
        task = Task.objects.create(
            project=self.project,
            name="Task 1",
            description="Task 1 description",
            status="new",
            priority="high",
            deadline="2024-08-20"
        )
        url = reverse('task-detail', args=[self.project.id, task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


from unittest.mock import patch
from django.utils import timezone
from rest_framework.test import APIClient


class OverdueTaskReportTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/reports/overdue_tasks/'
        self.user = User.objects.create_user(username='testuser', password='testpass')

        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.project = Project.objects.create(
            name="Test Project",
            description="Description for Test Project",
            owner=self.user
        )

    @patch('projects.utils.notifications.send_telegram_message')
    def test_overdue_task_notification(self, mock_send_telegram_message):
        Task.objects.create(
            project=self.project,
            name="Overdue Task",
            description="Task that is overdue",
            status="new",
            priority="high",
            deadline=timezone.now().date() - timezone.timedelta(days=1)  # Overdue
        )
        
        url = reverse('overdue_tasks_report')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
