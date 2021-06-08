from celery import shared_task
from django.http import HttpResponse  
from drf import settings
from django.core.mail import send_mail  
from celery import Celery

app = Celery('tasks',broker="redis://localhost:6379/0")
@shared_task
def add(x,y):
    return x+y

@shared_task
def mail(email):  
    subject = "Greetings"  
    msg     = "'http://127.0.0.1:8000/employee/clickme/'"  
    to      = email
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to],fail_silently=False)  
   

# app.conf.beat_schedule = {
# "run-me-every-ten-seconds": {
# "task": "tasks.mail",
# "schedule": 10.0
#  }
# } 