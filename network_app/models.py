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
        if username is None or password is None:
            raise TypeError('Username and password are required fields')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class NetworkUser(AbstractUser):
    objects = UserManager()


class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        NetworkUser,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts')
    published = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(NetworkUser, related_name='liked_posts', blank=True)
