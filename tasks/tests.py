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

    def test_history_object_was_created(self):
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

    def test_user_can_get_only_his_own_tasks(self):
        """test: user can get his own task, not all"""

        user1 = _create_test_user('user', 'password')
        user2 = _create_test_user('user2', 'password2')
        token = _get_token(self, user1)

        Task.objects.create(user=user1)
        Task.objects.create(user=user2)

        url = self.live_server_url + '/api/tasks/'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        task_request = requests.get(url, headers=headers)
        task = json.loads(task_request.text)
        self.assertEqual(len(task), 1)

    def test_user_can_get_certain_task(self):
        """test: user can get one task use its id"""

        user = _create_test_user('user', 'password')
        token = _get_token(self, user)

        task = Task.objects.create(user=user, title='test')

        url = self.live_server_url + f'/api/tasks/{task.id}/'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        new_task_request = requests.get(url, headers=headers)
        new_task = json.loads(new_task_request.text)
        self.assertEqual(new_task['user'], user.id)
        self.assertEqual(new_task['title'], 'test')

    def test_user_can_not_get_foreign_task(self):
        """test: user can't get task owned by someone else"""

        user1 = _create_test_user('user', 'password')
        user2 = _create_test_user('user2', 'password2')
        token1 = _get_token(self, user1)

        task2 = Task.objects.create(user=user2)

        url2 = self.live_server_url + f'/api/tasks/{task2.id}/'
        headers = {
            'Authorization': f'Bearer {token1}',
            'Content-Type': 'application/json'
        }
        task_request2 = requests.get(url2, headers=headers)
        task2 = json.loads(task_request2.text)
        self.assertNotIn('user', task2)
        self.assertNotIn('title', task2)

    def test_task_created_by_post_request(self):
        """test: task object was created after post request"""

        user = _create_test_user('user', 'password')
        token = _get_token(self, user)

        url = self.live_server_url + '/api/tasks/'

        task_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        dict = {
            'title': 'title',
            'description': 'description',
            'status': 'new',
            'planned_completion_date': date.today().isoformat(),
            'user': user.id,
            'history': None
        }

        new_task_request = requests.post(url, data=json.dumps(dict), headers=task_headers)
        new_task = json.loads(new_task_request.text)
        self.assertEqual(new_task['title'], 'title')
        self.assertEqual(new_task['description'], 'description')
        self.assertEqual(new_task['status'], 'new')
        self.assertEqual(new_task['planned_completion_date'], date.today().isoformat())

    def test_user_can_update_his_task(self):
        """test: user can put new data"""

        user = _create_test_user('user', 'password')
        token = _get_token(self, user)
        task = Task.objects.create(user=user)

        url = self.live_server_url + f'/api/tasks/{task.id}/'

        task_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        dict = {
            'title': 'title',
            'description': 'description',
            'status': 'new',
            'planned_completion_date': date.today().isoformat(),
            'user': user.id
        }

        new_task_request = requests.put(url, data=json.dumps(dict), headers=task_headers)
        new_task = json.loads(new_task_request.text)
        self.assertEqual(new_task['title'], 'title')
        self.assertEqual(new_task['description'], 'description')
        self.assertEqual(new_task['status'], 'new')
        self.assertEqual(new_task['planned_completion_date'], date.today().isoformat())

    def test_user_can_patch_his_task(self):
        """test: user can patch task object"""

        user = _create_test_user('user', 'password')
        token = _get_token(self, user)
        task = Task.objects.create(user=user)

        url = self.live_server_url + f'/api/tasks/{task.id}/'

        task_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        dict = {
            'title': 'title',
            'description': 'description',
            'status': 'new',
        }

        new_task_request = requests.patch(url, data=json.dumps(dict), headers=task_headers)
        new_task = json.loads(new_task_request.text)
        self.assertEqual(new_task['title'], 'title')
        self.assertEqual(new_task['description'], 'description')
        self.assertEqual(new_task['status'], 'new')
        self.assertEqual(new_task['planned_completion_date'], None)

    def test_user_can_delete_his_task(self):
        """test: user can delete his task"""

        user = _create_test_user('user', 'password')
        token = _get_token(self, user)
        task = Task.objects.create(user=user)
        number_of_tasks_before_delete = Task.objects.count()

        url = self.live_server_url + f'/api/tasks/{task.id}/'

        task_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        requests.delete(url, headers=task_headers)

        number_of_tasks_after_delete = Task.objects.count()
        self.assertEqual(number_of_tasks_before_delete, number_of_tasks_after_delete + 1)


class HistoryApiTest(LiveServerTestCase):
    """Testing history api"""

    def test_user_can_get_task_history_objects(self):
        """test: user can get history objects to certain task"""

        user = _create_test_user('user', 'password')
        task = Task.objects.create(user=user)
        task.save()
        token = _get_token(self, user)

        url = self.live_server_url + f'/api/history?task={task.id}'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        history_request = requests.get(url, headers=headers)
        history = json.loads(history_request.text)
        self.assertEqual(len(history), 2)


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
        user = json.loads(new_user_request.text)
        self.assertEqual(user['username'], 'test_username')
        self.assertEqual(user['password'], 'test_password')


def _get_token(obj, user):
    token_url = obj.live_server_url + '/api-token-auth/'
    token_headers = {'Content-Type': 'application/json'}
    token_data = {'username': user.username, 'password': 'password'}
    token_request = requests.post(url=token_url, headers=token_headers, data=json.dumps(token_data))
    token = json.loads(token_request.text)['token']
    return token


def _create_test_user(username, password):
    user = User.objects.create(username=username, password=password)
    user.set_password(password)
    user.save()
    return user
