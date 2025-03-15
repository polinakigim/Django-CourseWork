from django.db import models

class Recipient(models.Model):
    email = models.CharField(max_length=50, unique=True, help_text='Email получателя рассылки')
    full_name = models.CharField(max_length=100, verbose_name='ФИО', help_text='Полное имя получателя рассылки')
    comment = models.TextField('Введите комментарий о получателе')

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['email', ]

    def __str__(self):
        return f"{self.full_name}"