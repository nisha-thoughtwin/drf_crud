from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from employee.models import Employee


# Create your tests here.
# ------------------------------ Articles ----------------------------
class ArticleViewTestCases(TestCase):
    def setUp(self):
      self.client = APIClient()
      self.response = self.client.get(reverse('articles'))
    
    def test_01_api_can_list_articals(self):
        response=self.assertEqual(self.response.status_code, status.HTTP_200_OK)

# -------------------------------- Employee Test ----------------------       

class EmployeeTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.employee_data =   {
        "employee_regNo": 103,
        "employee_name": "nisha",
        "employee_email": "nisha@gmail.com",
        "employee_mobile": 9644247764,
        "employee_dob": "1997-05-19",
        "created_at": "2021-05-29T13:05:59.551255Z"
    }
    self.response = self.client.post(
        reverse('employee_create'),
        self.employee_data,
        format="json")

  def test_01_api_can_create_a_employee(self):
    response=self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

  def test_02_api_can_get_a_employeelist(self):
    employeelist = Employee.objects.last()  
    response = self.client.get(reverse('employee_list')) 
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertContains(response, employeelist)  

  def test_03_api_can_update_employeelist(self): 
    employeelist = Employee.objects.last()
    self.employee_data = {
        "employee_regNo": 103,
        "employee_name": "nisha",
        "employee_email": "nisha@gmail.com",
        "employee_mobile": 5465465465,
        "employee_dob": "1997-05-19",
        "created_at": "2021-05-29T13:05:59.551255Z"
    }
    response = self.client.put(
            reverse('employee_update', kwargs={'pk':employeelist.id}),self.employee_data,
            format='json'
        )
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_04_api_can_delete_employeelist(self):
    employeelist = Employee.objects.last()
    response = self.client.delete(
      reverse('employee_delete',kwargs={'pk':employeelist.id}),format='json'
    )
    self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)  