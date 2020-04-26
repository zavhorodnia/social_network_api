from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username or not password:
            raise ValueError('Username and password are required fields')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if not username or not password:
            raise TypeError('Username and password are required fields')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class NetworkUser(AbstractUser):
    last_request = models.DateTimeField(auto_now_add=True)

    objects = UserManager()


class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        NetworkUser,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts')
    published = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(NetworkUser, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date = models.DateField(auto_now_add=True)
