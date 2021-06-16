from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from employee.views import ClickMe,PaymentGateway,charge, EmployeeCreateApi,EmployeeListApi,EmployeeUpdateApi,EmployeeDeleteApi

from employee.views import ArticleView,ArticleRetrive,adds,export_data,import_data,DataAdd,DataView,DataUpdate,DataDelete
from employee import views as api

router = routers.DefaultRouter()
router.register('employee', api.Employeeviewset)

urlpatterns =[
  path('add/',adds,name="add"),
  path('clickme/',ClickMe.as_view(),name="clickme21"),

  path('paymentgateway/',PaymentGateway.as_view(),name="paymentgateway"),
  path('charge/',charge,name="charge"),

  path('api/create',EmployeeCreateApi.as_view(),name='employee_create'),
  path('api/list',EmployeeListApi.as_view(),name='employee_list'),
  path('api/<int:pk>',EmployeeUpdateApi.as_view(),name='employee_update'),
  path('api/<int:pk>/delete',EmployeeDeleteApi.as_view(),name='employee_delete'),
   
  path('articles/', ArticleView.as_view(),name="articles"),
  path('articles_retrive/<int:pk>/', ArticleRetrive.as_view()),
  path('api/', include(router.urls)),

  path('export_data/',export_data,name="export_data"),
  path('import_data/',import_data,name="import_data"),
  path('data_add/', DataAdd.as_view(), name='data_add'),
  path('data_view/', DataView.as_view(), name='data_view'),
  path('data_update/<int:pk>/update/', DataUpdate.as_view(), name='data_update'),
  path('data_delete/<int:pk>/delete/', DataDelete.as_view(), name='data_delete'),
  ]
# urlpatterns = router.urls