from django.contrib import admin
from employee.models import Employee,Author,Article
# Register your models here.

admin.site.register(Employee)
admin.site.register(Author)
admin.site.register(Article)