from django.db import models
from users.models import User


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='like', default=None, blank=True)

    @property
    def num_likes(self):
        return self.like.all().count()

LIKE_CHOICES = {
    ('Like', 'Like'),
    ('unlike', 'unlike'),
}

class Like(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)