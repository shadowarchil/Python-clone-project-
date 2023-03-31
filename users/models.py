from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User #custom
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    def get_num_questions(self):
        """
        Returns the number of questions created by this user.
        """
        return self.question_set.count()

    def get_total_question_views(self):
        """
        Returns the total number of views for all the questions created by this user.
        """
        return sum(q.views for q in self.question_set.all())
#custom
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'