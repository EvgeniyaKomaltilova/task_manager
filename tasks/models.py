from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Model for users tasks"""

    status_choices = [
        ('new', 'new'),
        ('planned', 'planned'),
        ('in progress', 'in progress'),
        ('completed', 'completed')
    ]

    title = models.CharField(verbose_name='task title', max_length=32)
    description = models.TextField(verbose_name='task description')
    date_of_creation = models.DateField(verbose_name='date of task creation', auto_now_add=True)
    status = models.CharField(verbose_name='task status', max_length=11, choices=status_choices)
    planned_completion_date = models.DateField(verbose_name='planned task completion date', null=True, blank=True)
    user = models.ForeignKey(verbose_name='task owner', to=User, related_name='tasks', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """history object created when the task object is saved"""
        super(Task, self).save(*args, **kwargs)
        History.objects.create(
            task=self,
            title=self.title,
            description=self.description,
            status=self.status,
            planned_completion_date=self.planned_completion_date,
        )


class History(models.Model):
    """Model for saved changes in user tasks"""

    date_of_change = models.DateTimeField(verbose_name='date when the task was changed', auto_now_add=True)
    task = models.ForeignKey(verbose_name='task whose history is stored', to=Task, related_name='history',
                             on_delete=models.CASCADE)
    title = models.CharField(verbose_name='changed task title', max_length=32, null=True)
    description = models.TextField(verbose_name='changed task description', null=True)
    status = models.CharField(verbose_name='changed task status', max_length=11, null=True)
    planned_completion_date = models.DateField(verbose_name='changed planned task completion date',
                                               null=True, blank=True)

    def __str__(self):
        return f'{self.task.user}-{self.title}-{self.date_of_change}'
