from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField(default='This is my bio')
    likes = models.ManyToManyField(User, related_name='user_likes')
    theme = models.BooleanField(default=True)
    notifications = models.BooleanField(default=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


