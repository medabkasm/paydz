from django.db import models
from accounts.models import User
from django.template.defaultfilters import slugify

class Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    text = models.CharField(max_length=160)
    created_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length = 50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:10]+" ..."

class HashTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    post = models.ManyToManyField(Post)

    def __str__(self):
        return '#'+slugiffy(self.name)
