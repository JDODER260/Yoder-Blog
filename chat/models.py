from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Chat(models.Model):
    person_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_to')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s - %s' % (self.author, self.person_to, self.content)

    def get_absolute_url(self):
        return reverse('chat', kwargs={'pk': self.pk})


