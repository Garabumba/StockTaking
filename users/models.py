from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from django_group_model.models import AbstractGroup

class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    patronymic = models.CharField(blank=True, null=True, verbose_name="Отчество")
    computers = models.ManyToManyField('home.Computer', blank=True, related_name='UsersComputers')
    projectors = models.ManyToManyField('home.Projector', blank=True, related_name='UsersProjectors')
    printers = models.ManyToManyField('home.Printer', blank=True, related_name='UsersPrinters')
    tvs = models.ManyToManyField('home.TV', blank=True, related_name='UsersTVs')
    monitors = models.ManyToManyField('home.Monitor', blank=True, related_name='UsersMonitors')
    group = models.ForeignKey('Group', on_delete=models.PROTECT, null=True)

class Group(AbstractGroup):
    is_responsible = models.BooleanField(default=False)

class Task(models.Model):
    title = models.CharField(max_length=50, default='', null=False)
    message = models.CharField(max_length=500, default='', null=True)
    computer = models.ForeignKey('home.Computer', on_delete=models.CASCADE, null=True)
    printer = models.ForeignKey('home.Printer', on_delete=models.CASCADE, null=True)
    projector = models.ForeignKey('home.Projector', on_delete=models.CASCADE, null=True)
    tv = models.ForeignKey('home.TV', on_delete=models.CASCADE, null=True)
    monitor = models.ForeignKey('home.Monitor', on_delete=models.CASCADE, null=True)
    status = models.ForeignKey('TaskStatus', on_delete=models.PROTECT, null=True)
    users = models.ManyToManyField('User', through="User_Task")

    def get_absolute_url(self):
        return reverse_lazy('tasks')

class User_Task(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    owner = models.BooleanField()

    def get_absolute_url(self):
        return reverse_lazy('')

class TaskStatus(models.Model):
    class Status(models.IntegerChoices):
        IN_PROGRESS = 1, 'В работе'
        FINISHED = 2, 'Завершена'

    status_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.status_name
    
    def get_absolute_url(self):
        return reverse_lazy('')