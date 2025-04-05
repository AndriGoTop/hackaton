from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    login = models.CharField("Логин", max_length=50)
    email = models.EmailField("Почта", unique=True)
    picture = models.ImageField(upload_to='media/user_images/', null=True, blank=True)
    subs = models.ManyToManyField("Subs", related_name="subs",blank=True)
    telegram_id = models.ForeignKey("Subs",on_delete=models.CASCADE,blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Tags(models.Model):
    title = models.CharField("Тэги", max_length=50)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField("Название", max_length=60)
    article = models.TextField()
    picture = models.ImageField(upload_to='media/product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    tags = models.ManyToManyField("Tags", blank=True)

    def __str__(self):
        return self.title


class Subs(models.Model):
    sub = models.CharField("tg", max_length=100)
