from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
    

# ORM

class Tag(models.Model):
    title = models.CharField(max_length=35, unique=True)
    
    def clean(self) -> None:
        if not self.title.islower():
            raise ValidationError({
                'title': 'Title should be only in lower case'
            })
    
    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    title = models.CharField(max_length=255)
    text = models.TextField()

    create_time = models.DateTimeField(auto_now_add=True)
    
    modify_time = models.DateTimeField(auto_now=True)

    views = models.PositiveIntegerField(default=0)



    def __str__(self) -> str:
        return f'{self.title}'
    # method to count view for each user
    def increase_views(self):
        self.views += 1
        self.save()
    




class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'question']

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    text = models.TextField()

    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.text