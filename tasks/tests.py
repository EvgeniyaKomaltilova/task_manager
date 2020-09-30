import json
from datetime import date, timedelta
import requests
from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase

from tasks.models import Task, History


class TaskModelTest(TestCase):
    """Task model testing"""

    def test_task_object_was_created(self):
        """test: task object was created"""
        user = User.objects.create()
        task1 = Task.objects.create(
            title='title',
            description='description',
            status='new',
            planned_completion_date=date.today() + timedelta(days=10),
            user=user
        )
        task2 = Task.objects.create(title='test', user=user)
        self.assertEqual(Task.objects.all().count(), 2)
        self.assertEqual(task2.title, 'test')
        self.assertEqual(task1.title, 'title')
        self.assertEqual(task1.description, 'description')
        self.assertEqual(task1.date_of_creation, date.today())
        self.assertEqual(task1.status, 'new')
        self.assertEqual(task1.planned_completion_date, date.today() + timedelta(days=10))


class HistoryModelTest(TestCase):
    """History model testing"""

    def test_task_object_was_created(self):
        """test: history object created when the task object is saved"""
        user = User.objects.create()
        task = Task.objects.create(
            title='title',
            description='description',
            status='new',
            planned_completion_date=date.today() + timedelta(days=10),
            user=user
        )
        task.title = 'another title'
        task.description = 'another description'
        task.status = 'planned'
        task.planned_completion_date = date.today() + timedelta(days=20)
        task.save()
        history1 = History.objects.last()
        self.assertEqual(history1.title, 'another title')
        self.assertEqual(history1.description, 'another description')
        self.assertEqual(history1.date_of_creation, task.date_of_creation)
        self.assertEqual(history1.status, 'planned')
        self.assertEqual(history1.planned_completion_date, task.planned_completion_date)


class TaskApiTest(LiveServerTestCase):
    """Testing task api"""

    def test_task_created_by_post_request(self):
        """test: task object was created after post request"""

        user = User.objects.create(username='user', password='password')
        user.set_password('password')
        user.save()
        print(f'user: user')
        print(f'password: password')
        token_url = self.live_server_url + '/api-token-auth/'
        token_headers = {'Content-Type': 'application/json'}
        token_data = {'username': 'user', 'password': 'password'}
        token_request = requests.post(url=token_url, headers=token_headers, data=json.dumps(token_data))
        print(token_request.text)
        token = json.loads(token_request.text)['token']
        print(token)

        url = self.live_server_url + '/api/tasks/'
        task_headers = {
            'Authorization': f'JWT {token}',
            'Content-Type': 'application/json'
        }
        dict = {
            'title': 'title',
            'description': 'description',
            'status': 'new',
            # 'planned_completion_date': date.today() + timedelta(days=10),
            'user': user.id,
            'history': None
        }
        new_task_request = requests.post(url, data=json.dumps(dict), headers=task_headers)
        print(new_task_request.text)
        new_task = json.loads(new_task_request.text)
        self.assertEqual(new_task['title'], 'title')
        self.assertEqual(new_task['description'], 'description')
        self.assertEqual(new_task['status'], 'new')


class UserApiTest(LiveServerTestCase):
    """Testing user api"""

    def test_user_created_by_api_request(self):
        """test: user was created after api post request"""

        url = self.live_server_url + '/api/users/'
        headers = {'Content-Type': 'application/json'}
        dict = {
            'username': 'test_username',
            'password': 'test_password',
        }
        new_user_request = requests.post(url, data=json.dumps(dict), headers=headers)
        # print(new_user_request.text)
        user = json.loads(new_user_request.text)
        self.assertEqual(user['username'], 'test_username')
        self.assertEqual(user['password'], 'test_password')
