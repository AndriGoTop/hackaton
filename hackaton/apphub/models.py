from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    login = models.CharField("Логин", max_length=50)
    email = models.EmailField("Почта", unique=True)
    picture = models.ImageField(upload_to='user_images/', null=True, blank=True)
    favorite = models.ManyToManyField("Tags", blank=True)
    telegram_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username


class Tags(models.Model):
    title = models.CharField("Тэги", max_length=50)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField("Название", max_length=60)
    article = models.TextField()
    picture = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tags", blank=True)

    def __str__(self):
        return self.title
