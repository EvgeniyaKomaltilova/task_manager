from datetime import date, timedelta, datetime
from django.contrib.auth.models import User
from django.test import TestCase
from tasks.models import Task


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
        self.assertEqual(history1.status, 'planned')
        self.assertEqual(history1.planned_completion_date, date.today() + timedelta(days=20))
