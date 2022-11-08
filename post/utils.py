from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def NewPost(author, title, content, emails):
    for user in User.objects.all():
        if user.profile.notifications:
            emails.append(user.email)
    for email in emails:
        send_mail(
            subject=f'New Post by - {author}',
            message=content + "If you are getting this and dont want to go to your profile on Yoder Blog (https://jdswebsites.xyz) and deselect Recieve email notifications",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email])



def Backup():
    pass