from .models import Employee, Document, Assets, SalarySlips, Project, Task, Banks
from rest_framework import serializers


# DOCUMENT SERIALIZER
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields =['id','employee','id_proof','address_proof', 'passport_photo','degree_certificate','transcript','professional_certifications','offer_letter','relieving_letter','experience_letter','pay_slip','pan_card','tax_documents','bank_details','police_verification','medical_certificate','reference_letter','other_documents']


# asset serializer
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields =['id','employee', 'asset_name', 'asset_description', 'asset_image', 'present']


# salary slips serializer

class SalarySlipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalarySlips
        fields =['id','employee', 'salary_slip', 'amount']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','name', 'description', 'estimated_budget', 'expected_results', 'employees', 'status']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['id','task','if_media','description','due_date','completed','project','assigned_to']

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banks
        fields=['id','bank_name','account_number','ifsc_code','upi_id','employee','updated_at']


class EmployeeSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    assets = AssetSerializer(many=True, read_only=True)
    slips = SalarySlipsSerializer(many=True, read_only=True)
    project=ProjectSerializer(many=True, read_only=True)
    tasks=TaskSerializer(many=True, read_only=True)
    banks=BankSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['profile_pic','name', 'email','contact','role', 'salary','resume','date_joined','documents','assets','slips','banks','project','tasks']