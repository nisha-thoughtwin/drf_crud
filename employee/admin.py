from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from employee.models import Employee,Author,Article,Data
# Register your models here.
class DataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
     pass

admin.site.register(Employee)
admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Data,DataAdmin)