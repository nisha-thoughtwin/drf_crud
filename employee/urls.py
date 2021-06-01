from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from employee.views import EmployeeCreateApi,EmployeeListApi,EmployeeUpdateApi,EmployeeDeleteApi

from employee.views import ArticleView,ArticleRetrive
from employee import views as api

router = routers.DefaultRouter()
router.register('employee', api.Employeeviewset)

urlpatterns =[
  path('api/create',EmployeeCreateApi.as_view(),name='employee_create'),
  path('api/list',EmployeeListApi.as_view(),name='employee_list'),
  path('api/<int:pk>',EmployeeUpdateApi.as_view(),name='employee_update'),
  path('api/<int:pk>/delete',EmployeeDeleteApi.as_view(),name='employee_delete'),

  path('articles/', ArticleView.as_view(),name="articles"),
  path('articles_retrive/<int:pk>/', ArticleRetrive.as_view()),
  path('api/', include(router.urls)),

  ]
# urlpatterns = router.urls