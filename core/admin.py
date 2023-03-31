from django.contrib import admin
from core.models import Question, Answer, Vote, Tag
from users.models import User

# Register your models here.
admin.site.register([Question, Answer, Vote, Tag, User])
