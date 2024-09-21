from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='images', blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    salary = models.IntegerField()
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, related_name='documents', on_delete=models.CASCADE)
    id_proof = models.FileField(upload_to='documents/id_proof/', null=True, blank=True)
    address_proof = models.FileField(upload_to='documents/address_proof/', null=True, blank=True)
    passport_photo = models.FileField(upload_to='documents/photos/', null=True, blank=True)

    # Educational Certificates
    degree_certificate = models.FileField(upload_to='documents/education/', null=True, blank=True)
    transcript = models.FileField(upload_to='documents/education/', null=True, blank=True)
    professional_certifications = models.FileField(upload_to='documents/certifications/', null=True, blank=True)

    # Employment Documents
    offer_letter = models.FileField(upload_to='documents/employment/', null=True, blank=True)
    relieving_letter = models.FileField(upload_to='documents/employment/', null=True, blank=True)
    experience_letter = models.FileField(upload_to='documents/employment/', null=True, blank=True)
    pay_slip = models.FileField(upload_to='documents/employment/', null=True, blank=True)

    # Tax and Financial Documents
    pan_card = models.FileField(upload_to='documents/tax/', null=True, blank=True)  # Specific to India
    tax_documents = models.FileField(upload_to='documents/tax/', null=True, blank=True)
    bank_details = models.FileField(upload_to='documents/bank/', null=True, blank=True)

    # Compliance and Verification
    police_verification = models.FileField(upload_to='documents/compliance/', null=True, blank=True)
    medical_certificate = models.FileField(upload_to='documents/medical/', null=True, blank=True)
    reference_letter = models.FileField(upload_to='documents/references/', null=True, blank=True)

    # Other documents
    other_documents = models.FileField(upload_to='documents/others/', null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.name}, {self.id_proof}, {self.address_proof}, {self.passport_photo}, {self.degree_certificate}, {self.transcript}, {self.professional_certifications}, {self.offer_letter}, {self.relieving_letter}, {self.experience_letter}, {self.pay_slip}, {self.pan_card}, {self.tax_documents}, {self.bank_details}, {self.police_verification}, {self.medical_certificate}, {self.reference_letter}, {self.other_documents}'


# assets
class Assets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assets')
    asset_name = models.CharField(max_length=200)
    asset_description = models.CharField(max_length=500)
    asset_image = models.ImageField(upload_to='asset_images/')
    present = models.BooleanField(default=True)
    date_assigned = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.asset_name} - {self.employee.name}'


# salary slips
class SalarySlips(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='slips')
    salary_slip = models.FileField(upload_to='salary_slips/')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee.name} - {self.amount}'


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    estimated_budget = models.IntegerField()
    expected_results = models.FileField(upload_to='expected_project_results/')
    employees = models.ManyToManyField(Employee, related_name='project')
    status = models.CharField(max_length=50, choices=(
        ('pending', 'pending'), ('initialized', 'initialized'), ('completed', 'completed'),
        ('in progress', 'in progress')),
                              default='pending')
    created_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField()

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    task = models.CharField(max_length=200, null=True)
    if_media = models.FileField(upload_to='tasks/', null=True, blank=True)
    description = models.TextField()
    time_assigned_task = models.DateTimeField(auto_now=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    receivers_name=models.CharField(max_length=100, null=True)# Corrected the class name to ForeignKey
    subject = models.CharField(max_length=255)
    status = models.CharField(
    max_length=100,
    choices=(('delivered', 'delivered'), ('failed', 'failed')),
    default='delivered',
    null=True
   )
    message=models.TextField()# Changed to CharField for subject length
    to = models.EmailField()  # Changed to EmailField for email validation
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"