from django.db import models


class Task(models.Model):

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
    # user = models.ForeignKey(verbose_name='task owner', to='User', related_name='tasks', on_delete=models.CASCADE)
