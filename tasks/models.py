from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    
    class Status(models.TextChoices):
        TODO = 'TODO', _('До виконання')
        IN_PROGRESS = 'IN_PROG', _('В процесі')
        DONE = 'DONE', _('Виконано')

    class Priority(models.TextChoices):
        LOW = 'LOW', _('Низький')
        MEDIUM = 'MED', _('Середній')
        HIGH = 'HIGH', _('Високий')

    title = models.CharField(max_length=255, verbose_name=_("Назва"))
    description = models.TextField(blank=True, verbose_name=_("Опис"))
    
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.TODO,
        verbose_name=_("Статус")
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name=_("Пріоритет")
    )
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Термін виконання"))

    image = models.ImageField(
        upload_to='task_images/',
        null=True,
        blank=True,
        verbose_name="Зображення"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks', 
        verbose_name=_("Користувач")
    )

    class Meta:
        ordering = ['due_date', '-priority']
        verbose_name = _("Завдання")
        verbose_name_plural = _("Завдання")

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name=_("Завдання")
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name=_("Автор")
    )
    text = models.TextField(verbose_name=_("Текст коментаря"), blank=True)
    
    image = models.ImageField(
        upload_to='comment_images/',
        null=True,
        blank=True,
        verbose_name="Зображення"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Коментар")
        verbose_name_plural = _("Коментарі")

    def __str__(self):
        return f"Коментар від {self.author} до {self.task.title}"