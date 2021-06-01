from rest_framework import  serializers
from employee.models import Employee,Article
from datetime import date
from rest_framework.validators import UniqueValidator
from django.utils import timezone
from datetime import datetime



# Model serializatizer
class EmployeeSerializer(serializers.ModelSerializer):
    employee_email = serializers.EmailField(max_length=100, validators=[UniqueValidator(queryset=Employee.objects.all())])
    
    created_at = serializers.DateTimeField(read_only=True, default=timezone.now)
    employee_dob = serializers.DateField()
    employee_name = serializers.CharField(max_length=100)
    employee_regNo = serializers.IntegerField()


    class Meta:
        model = Employee
        fields = ['employee_regNo','employee_name','employee_email','employee_mobile','employee_dob','created_at']
        
    def validate_employee_dob(self, employee_dob):
        today = date.today()
        age = today.year - employee_dob.year - ((today.month, today.day) < (employee_dob.month, employee_dob.day))
        if (not(20 < age < 30)):
            raise serializers.ValidationError("You are no eligible for the job")
        return employee_dob


# normal serialization
class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()
    body = serializers.CharField()
    author_id = serializers.IntegerField()

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance,validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.body = validated_data.get('body',instance.body)
        instance.author_id = validated_data.get('author_id',instance.author_id)

        instance.save()
        return instance
