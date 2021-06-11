from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
import stripe
from stripe.api_resources import source

from employee.models import Author,Article,Employee
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
          

    
    
   