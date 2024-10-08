from django import forms
from .models import Employee, Document, Assets, SalarySlips, Project, Task, Email, Banks, SendSlip


class EmployeeForm(forms.ModelForm):
    class Meta():
        model = Employee
        fields = '__all__'
        exclude = ['user', 'date_joined']


class DocumentForm(forms.ModelForm):
    class Meta():
        model = Document
        fields = '__all__'
        exclude = ['uploaded_at', 'employee', 'user']


class AssetsForm(forms.ModelForm):
    class Meta():
        model = Assets
        fields = '__all__'
        exclude = ['employee', 'date_assigned', 'user']


class SalaryForm(forms.ModelForm):
    class Meta:
        model = SalarySlips
        fields = '__all__'
        exclude = ['employee', 'date', 'user']


class ProjectForm(forms.ModelForm):
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),  # Fetch all employees
        widget=forms.CheckboxSelectMultiple  # This creates checkboxes for selecting multiple employees
    )

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['user', 'created_at']


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),  # Fetch all employees
        widget=forms.CheckboxSelectMultiple  # This creates checkboxes for selecting multiple employees
    )

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['project', 'time_assigned_task', 'user']


class EmailForm(forms.Form):
    recipient_name = forms.CharField(max_length=100)
    recipient_email = forms.EmailField()

class EmailFor(forms.ModelForm):
    class Meta:
        model=Email
        fields='__all__'
        exclude=['user','date','status']

class BankForm(forms.ModelForm):
    class Meta:
        model=Banks
        fields='__all__'
        exclude=['user','employee','updated_at']
        widgets = {
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account Number'}),
            'bank_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Bank Name'}),
            'ifsc_code':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter IFSC Code'}),
            'upi_id':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter UPI ID'}),       
        }


class SendSlipsForm(forms.ModelForm):
    class Meta:
        model = SendSlip
        fields ='__all__'
        exclude=['user','employee']
        widgets = {
            'month': forms.TextInput(attrs={'required': True}),
            'basic_salary': forms.NumberInput(attrs={'required': True}),
            'allowances': forms.NumberInput(attrs={'required': False}),
            'deductions': forms.NumberInput(attrs={'required': False}),
        }