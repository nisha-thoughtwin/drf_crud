from django.shortcuts import render,HttpResponse,redirect
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
import stripe
from stripe.api_resources import source

from employee.models import Author,Article,Employee,Data
from .serializers import ArticleSerializer,EmployeeSerializer
from rest_framework import status

from django.db.models import query
from rest_framework import generics,viewsets
from rest_framework.response import Response
from . import serializers
# from . import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .tasks import add,mail

from tablib import Dataset
from employee.resources import DataResource
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView

 
# Create your views here.

def adds(request):
    if request.method =="POST":
        email=request.POST["email"]
        msg=request.POST["msg"]
        # email =['mdeeppatidar@gmail.com','nisha.thoughtwin@gmail.com']
        mail.delay(email,msg)
        return HttpResponse("Success")
    return render(request,'add.html')


class ClickMe(TemplateView):
    template_name="clickme.html"

# --------------------------------------- Payment Gateway --------------------
stripe.api_key = settings.STRIPE_SECRATE_KEY
class PaymentGateway(TemplateView):
    template_name="paymentgateway.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount = 100000,
            currency = 'inr', 
            description = 'Payment gateway',
            source = request.POST['stripeToken']
            )
        return render(request,'charge.html')
    
# --------------------------------------class based APIView--------------------

class ArticleView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        return Response({"articles": serializer.data})
    
    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleRetrive(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        articles = self.get_object(pk)
        serializer = ArticleSerializer(articles)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        articles = self.get_object(pk)
        serializer = ArticleSerializer(articles, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, pk, format=None):
        articles = self.get_object(pk)
        if not articles:
            return Response(
                {"res": "Object with artical id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        articles.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)    
    
# -------------------------------- Generic ------------------------------ 

class EmployeeCreateApi(generics.CreateAPIView):
  queryset = Employee.objects.all()
  serializer_class = EmployeeSerializer

class EmployeeListApi(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDeleteApi(generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    

#   --------------------------------- ModelViewset-------------------------------

class Employeeviewset(viewsets.ModelViewSet):
  queryset = Employee.objects.all()
  serializer_class = serializers.EmployeeSerializer
  authentication_classes = [TokenAuthentication]
#   permission_classes = [IsAuthenticated]
          
#   --------------------------------- Export Data-------------------------------
def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        data_resource = DataResource()
        dataset = data_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response
        elif file_format == 'XLSX':
            response = HttpResponse(dataset.xlsx, content_type='application/xlsx')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            return response
        elif file_format == 'TSV':
            response = HttpResponse(dataset.tsv, content_type='application/tsv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.tsv"'
            return response  
        elif file_format == 'YAML':
            response = HttpResponse(dataset.yaml, content_type='application/yaml')
            response['Content-Disposition'] = 'attachment; filename="exported_data.yaml"'
            return response     

    return render(request, 'export.html')   
    
#   --------------------------------- Import Data-------------------------------
def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        data_resource = DataResource()
        dataset = Dataset()
        new_data = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_data.read().decode('utf-8'),format='csv')
            result = data_resource.import_data(dataset, dry_run=True) 
        elif file_format == 'JSON':
            imported_data = dataset.load(new_data.read().decode('utf-8'),format='json')
            result = data_resource.import_data(dataset, dry_run=True) 
        elif file_format == 'XLSX':
            imported_data = dataset.load(new_data.read().decode('utf-8'),format='xlsx')
            result = data_resource.import_data(dataset, dry_run=True) 
        elif file_format == 'TSV':
            imported_data = dataset.load(new_data.read().decode('utf-8'),format='tsv')
            result = data_resource.import_data(dataset, dry_run=True) 
        elif file_format == 'YAML':
            imported_data = dataset.load(new_data.read().decode('utf-8'),format='yaml')
            result = data_resource.import_data(dataset, dry_run=True)             

        if not result.has_errors():
            # Import now
            data_resource.import_data(dataset, dry_run=False)
            return redirect('/employee/data_view/')


    return render(request, 'import.html')    

class DataAdd(CreateView):
    model = Data
    template_name = "dataadd.html"
    fields = ["First_name","Last_name","Age","Dob"]
    success_url = reverse_lazy('data_view')

class DataView(ListView):
    model = Data
    template_name = "dataview.html"
    fields = ("First_name","Last_name","Age","Dob")
    context_object_name = "data"

class DataUpdate(UpdateView):
    model = Data
    fields = ["First_name","Last_name","Age","Dob"]
    template_name = "dataupdate.html"
    context_object_name = "object"
    success_url = reverse_lazy('data_view')

class DataDelete(DeleteView): 
    model = Data
    template_name = "datadelete.html"
    success_url = reverse_lazy('data_view')