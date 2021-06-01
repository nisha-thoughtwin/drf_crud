from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class Employee(models.Model):
  employee_regNo = models.IntegerField(unique=True)
  employee_name = models.CharField(max_length=100)
  employee_email = models.CharField(max_length=100)
  employee_mobile = models.IntegerField()
  employee_dob = models.DateField()
  # emplyee_age = models.IntegerField()
  created_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.employee_name

  class Meta:
    ordering=('id',)

class Author(models.Model):
  name = models.CharField(max_length=255)
  email = models.EmailField()
  def __str__(self):
    return self.name

class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    def __str__(self):
      return self.title 


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=True, **kwargs):
    if created:
        Token.objects.create(user=instance)
