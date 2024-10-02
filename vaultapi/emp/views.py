import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Document, Assets, SalarySlips, Project, Task,Email, Banks, SendSlip
from .forms import EmployeeForm, DocumentForm, AssetsForm, SalaryForm, ProjectForm, EmailForm, TaskForm, EmailFor, BankForm, SendSlipsForm
from django.contrib import messages
from .serializers import EmployeeSerializer, DocumentSerializer, AssetSerializer, SalarySlipsSerializer, \
    ProjectSerializer, TaskSerializer, BankSerializer
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .pagination import MyCursorPagination, MyPageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .throttling import AnoThrottle, UserThrottleRate
from django.http import JsonResponse, HttpResponse
import time
import psutil
import pyautogui
from django.contrib.auth.models import User
import pywhatkit as kit
from plyer import notification
import pygame
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings, Settings
import pyttsx3
from PIL import Image, ImageDraw, ImageFont
import io

# Create your views here.

def register_employee(request):
    data = None
    pyautogui.FAILSAFE = False
    if request.method == 'GET':
        txt = request.GET.get('txt')
        if txt:
            try:
                time.sleep(5)
                pyautogui.write(txt, interval=0.05)

            except Exception as e:
                return JsonResponse({'msg': str(e)}, status=400)
            return HttpResponse(f'Text typed: {txt}')
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.user = request.user
            emp.save()
            messages.success(request, 'Employee details added successfully')
            pygame_notify()
            return redirect('register_employee')
    else:
        form = EmployeeForm()

    # Retrieve all employee data
    data = Employee.objects.filter(user=request.user)
    # Get system information using psutil
    system_info = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_info': psutil.virtual_memory(),
        'disk_usage': psutil.disk_usage('/'),
        'network_info': psutil.net_io_counters(),
        'battery': psutil.sensors_battery()  # Get battery info
    }

    # Check if battery info is available
    if system_info['battery']:
        battery_percent = system_info['battery'].percent
        power_plugged = system_info['battery'].power_plugged
        time_left = system_info['battery'].secsleft if system_info[
                                                           'battery'].secsleft != psutil.POWER_TIME_UNLIMITED else None
    else:
        battery_percent = power_plugged = time_left = None

    # Prepare context to pass to the template
    context = {
        'form': form,
        'data': data,
        'cpu_usage': system_info['cpu_usage'],
        'total_memory': system_info['memory_info'].total / (1024 ** 3),
        'used_memory': system_info['memory_info'].used / (1024 ** 3),
        'memory_percent': system_info['memory_info'].percent,
        'total_disk': system_info['disk_usage'].total / (1024 ** 3),
        'used_disk': system_info['disk_usage'].used / (1024 ** 3),
        'disk_percent': system_info['disk_usage'].percent,
        'bytes_sent': system_info['network_info'].bytes_sent / (1024 ** 2),
        'bytes_recv': system_info['network_info'].bytes_recv / (1024 ** 2),
        'battery_percent': battery_percent,
        'power_plugged': power_plugged,
        'time_left': time_left,
    }

    return render(request, 'emp/register_employee.html', context)


@login_required
def delete_emp(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    try:
        employee.delete()
    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=400)
    pygame_notify()
    messages.success(request, f'{employee.name} has been deleted from database')
    return redirect('register_employee')


@login_required
def edit_emp(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                return JsonResponse({'msg': str(e)}, status=400)
            messages.success(request, f'{employee.name} s profile has been updated')
            pygame_notify()
            return redirect('register_employee')
    else:
        form = EmployeeForm(instance=employee)
    t = time.localtime()
    actual_time = time.strftime('%d-%m-%y %H:%M:%S', t)
    return render(request, 'emp/edit_emp.html', {'form': form, 'employee': employee, 'actual_time': actual_time})


@login_required
def emp_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    return render(request, 'emp/emp_detail.html', {'emp': emp})


@login_required
def shutdown(request):
    pygame_notify()
    kit.shutdown(6)
    return render(request, 'emp/shutdown.html')


@login_required
def upload_docs(request, pk):
    # doc = None
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            documents = form.save(commit=False)
            documents.user = request.user
            documents.employee = employee
            documents.save()
            messages.success(request, 'documents attached successfully')
            pygame_notify()
            return redirect('upload_docs', pk=employee.pk)
    else:
        form = DocumentForm
    doc = Document.objects.filter(employee=employee)
    return render(request, 'emp/upload_docs.html', {'form': form, 'doc': doc})


def delete_docs(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    messages.success(request, 'Document has been deleted')
    pygame_notify()
    return redirect('register_employee')


# asset section
@login_required
def asset(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = AssetsForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.employee = employee
            asset.user = request.user
            asset.save()
            messages.success(request, 'asset has been saved !')
            pygame_notify()
            return redirect('assets', pk=employee.pk)
    else:
        form = AssetsForm
    data = Assets.objects.filter(employee=employee)
    return render(request, 'emp/asset.html', {'form': form, 'data': data, 'employee': employee})


@login_required
def delete_asset(request, pk):
    employee = Employee
    asset = get_object_or_404(Assets, pk=pk)
    try:
        asset.delete()
    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=400)

    messages.success(request, f'Asset of {employee.name} s - {asset.asset_name} has been deleted successfully')
    pygame_notify()
    return redirect('register_employee')


# salary slips
@login_required
def salary_slips(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = SalaryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                slip = form.save(commit=False)
                slip.employee = employee
                slip.user = request.user
                slip.save()
                t = time.localtime()
                actual_time = time.strftime("%d-%m-%y %H:%M:%S", t)
            except Exception as e:
                return JsonResponse({'msg': str(e)}, status=400)
            pygame_notify()
            messages.success(request, f'salary slip attached to {employee.name} on {actual_time}')
            return redirect('salary_slips', pk=employee.pk)
    else:
        form = SalaryForm()

    # Get all salary slips related to the employee (removed pk=pk)
    data = SalarySlips.objects.filter(employee=employee, user=request.user)

    # Formatting the time for the page display
    t = time.localtime()
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", t)

    return render(request, 'emp/salary.html', {
        'form': form,
        'employee': employee,
        'actual_time': actual_time,
        'data': data
    })


@login_required
def delete_slips(request, pk):
    employee = Employee
    slip = get_object_or_404(SalarySlips, pk=pk)
    slip.employee.name = employee
    try:
        slip.delete()
    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=400)
    pygame_notify()
    messages.success(request, f'Salary sleep of {employee.name} - Amount {slip.amount} Deleted Successfully!')
    return redirect('register_employee')


@login_required
def guide(request):
    return render(request, 'emp/guide.html')


from django.core.mail import EmailMessage
from django.conf import settings
import os


@login_required
def create_project(request):
    pro = Project
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the form without committing (to access the project object)
                project = form.save(commit=False)
                project.user = request.user
                project.project = pro

                # First, save the project to generate an id
                project.save()

                # Now save the ManyToMany relationship (employees)
                form.save_m2m()

                # After saving, collect the emails of employees
                employee_emails = [employee.email for employee in project.employees.all()]

                # Prepare the HTML message
                html_message = f"""
                <h1 style="color: #333;">New Project Assigned: {project.name}</h1>
                <p style="font-size: 14px; color: #555;">
                    Dear Team,<br><br>
                    You have been assigned a new project. Please find the details below:
                </p>
                <ul>
                    <li><strong>Project Name:</strong> {project.name}</li>
                    <li><strong>Description:</strong> {project.description}</li>
                    <li><strong>Budget:</strong> {project.estimated_budget}</li>
                    <li><strong>Current Status:</strong> {project.status}</li>
                    <li><strong>Received Project:</strong> {project.created_at}</li>
                    <li><strong>Due Date:</strong> {project.due_date}</li>
                    <li><strong>Team Members:</strong> {project.employees.all()}</li>
                    <li><strong>Project Status:</strong> {project.status}</li>
                </ul>
                <p style="font-size: 14px; color: #555;">
                    Kindly review the attached file for more information.<br>
                    <strong>Thank you,<br>Team Django</strong>
                </p>
                """

                # Prepare the email
                email = EmailMessage(
                    subject=f'Project Assignment: {project.name}',
                    body=html_message,
                    from_email='vishaldudhabarve105@gmail.com',  # From email
                    to=employee_emails,  # List of To emails
                )

                # Set the content type to HTML
                email.content_subtype = 'html'

                # Attach the expected results file if it exists
                if project.expected_results:
                    file_path = os.path.join(settings.MEDIA_ROOT, project.expected_results.name)
                    email.attach_file(file_path)

                # Send the email
                email.send(fail_silently=False)

            except Exception as e:
                return JsonResponse({
                    'msg': str(e)
                }, status=400)

            # Create a success message
            messages.success(request,
                             f'Congratulations {request.user} Project Created successfully\n Summery of your project {project.name}\n Name : {project.name}\n Budget :{project.estimated_budget}\n Employees :{project.employees.all()}\n Current Status : {project.status}\n Created : {project.created_at}\n Deadline : {project.due_date}\n Kindly complete your project before {project.due_date} to avoid any potential losses to the company\n Thank you team Django.')

            # Notify and redirect
            pygame_notify()

            return redirect('create_project')
    else:
        form = ProjectForm()

    t = time.localtime()
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", t)
    return render(request, 'emp/create_project.html', {'form': form, 'actual_time': actual_time})


@login_required
def view_projects(request):
    data = Project.objects.filter(user=request.user)
    t = time.localtime()
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", t)
    return render(request, 'emp/view_projects.html', {'data': data, 'actual_time': actual_time})


def cancel_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Get employee details BEFORE deleting the project
    employee_emails = [employee.email for employee in project.employees.all()]
    employee_names = ', '.join([str(employee) for employee in project.employees.all()])

    try:
        # Prepare the HTML message BEFORE deletion
        html_message = f"""
            <h1 style="color: #333;">Project Cancelled: {project.name}</h1>
            <p style="font-size: 14px; color: #555;">
                Dear Team,<br><br>
                We have cancelled the project <strong>{project.name}</strong> due to unforeseen reasons.
                Kindly review the details below:
            </p>
            <ul>
                <li><strong>Project Name:</strong> {project.name}</li>
                <li><strong>Description:</strong> {project.description}</li>
                <li><strong>Budget:</strong> {project.estimated_budget}</li>
                <li><strong>Current Status:</strong> {project.status}</li>
                <li><strong>Received Project:</strong> {project.created_at}</li>
                <li><strong>Due Date:</strong> {project.due_date}</li>
                <li><strong>Team Members:</strong> {employee_names}</li>
                <li><strong>Project Status:</strong> {project.status}</li>
            </ul>
            <p style="font-size: 14px; color: #555;">
                Please contact the team for further details.<br>
                <strong>Thank you,<br>Team Django</strong>
            </p>
        """

        # Prepare the email before deletion
        email = EmailMessage(
            subject=f'Project Cancellation: {project.name}',
            body=html_message,
            from_email='vishaldudhabarve105@gmail.com',  # From email
            to=employee_emails,  # List of employee emails
        )

        # Set content type to HTML
        email.content_subtype = 'html'

        # Attach the expected results file if it exists
        if project.expected_results:
            file_path = os.path.join(settings.MEDIA_ROOT, project.expected_results.name)
            email.attach_file(file_path)

        # Send the email
        email.send(fail_silently=False)

        # Delete the project after gathering necessary info
        project.delete()


    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=400)

    # Feedback message after project cancellation
    messages.success(request,
                     f'{project.name} has been cancelled and info sent to assigned employees: {employee_names}')
    pygame_notify()
    return redirect('view_projects')


@login_required
def edit_update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Get employee details BEFORE deleting the project
    employee_emails = [employee.email for employee in project.employees.all()]
    employee_names = ', '.join([str(employee) for employee in project.employees.all()])

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            try:
                form.save()
                # Prepare the HTML message BEFORE deletion
                html_message = f"""
                       <h1 style="color: #333;">Project Updated: {project.name}</h1>
                       <p style="font-size: 14px; color: #555;">
                           Dear Team,<br><br>
                           We have updated the project <strong>{project.name}</strong>.
                           Kindly review the updated details below:
                       </p>
                       <ul>
                           <li><strong>Project Name:</strong> {project.name}</li>
                           <li><strong>Description:</strong> {project.description}</li>
                           <li><strong>Budget:</strong> {project.estimated_budget}</li>
                           <li><strong>Current Status:</strong> {project.status}</li>
                           <li><strong>Received Project:</strong> {project.created_at}</li>
                           <li><strong>Due Date:</strong> {project.due_date}</li>
                           <li><strong>Team Members:</strong> {employee_names}</li>
                           <li><strong>Project Status:</strong> {project.status}</li>
                       </ul>
                       <p style="font-size: 14px; color: #555;">
                           Please contact the team for further details.<br>
                           <strong>Thank you,<br>Team Django</strong>
                       </p>
                   """

                # Prepare the email before deletion
                email = EmailMessage(
                    subject=f'Project Update: {project.name}',
                    body=html_message,
                    from_email='vishaldudhabarve105@gmail.com',  # From email
                    to=employee_emails,  # List of employee emails
                )

                # Set content type to HTML
                email.content_subtype = 'html'

                # Attach the expected results file if it exists
                if project.expected_results:
                    file_path = os.path.join(settings.MEDIA_ROOT, project.expected_results.name)
                    email.attach_file(file_path)

                # Send the email
                email.send(fail_silently=False)
            except Exception as e:
                return JsonResponse({
                    'msg': str(e)
                }, status=400)
            messages.success(request,
                             f'Your project {project.name} updated successfully and the update details has been sent '
                             f'to your members in a team project {project.employees.all()}')
            pygame_notify()
            return redirect('view_projects')
    else:
        form = ProjectForm(instance=project)
    t = time.localtime()
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", t)
    return render(request, 'emp/update_project.html', {'form': form, 'project': project, 'actual_time': actual_time})


@login_required
def send_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    employee_names = ', '.join([str(employee) for employee in project.employees.all()])

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                recipient_name = form.cleaned_data['recipient_name']
                recipient_email = form.cleaned_data['recipient_email']
                t = time.localtime()
                actual_time = time.strftime("%d-%m-%y %H:%M:%S", t)

                # Prepare the HTML message
                html_message = f"""
                    <h1 style="color: #333;">Project Details: {project.name}</h1>
                    <p style="font-size: 14px; color: #555;">
                        Dear {recipient_name},<br><br>
                        Here are the details of my project <strong>{project.name}</strong>.<br>
                        Kindly review the updated details below:
                    </p>
                    <ul>
                        <li><strong>Project Name:</strong> {project.name}</li>
                        <li><strong>Description:</strong> {project.description}</li>
                        <li><strong>Budget:</strong> {project.estimated_budget}</li>
                        <li><strong>Current Status:</strong> {project.status}</li>
                        <li><strong>Received Project:</strong> {project.created_at}</li>
                        <li><strong>Due Date:</strong> {project.due_date}</li>
                        <li><strong>Team Members:</strong> {employee_names}</li>
                    </ul>
                    <p style="font-size: 14px; color: #555;">
                        Review the further details below.<br>
                        <strong>Thank you,<br>Team Django</strong>
                    </p>
                """

                # Prepare the email
                email = EmailMessage(
                    subject=f'Project Details: {project.name}',
                    body=html_message,
                    from_email='vishaldudhabarve105@gmail.com',
                    to=[recipient_email],  # Recipient email in list form
                )
                email.content_subtype = 'html'  # Set the content type to HTML

                # Attach file if it exists
                if project.expected_results:
                    file_path = os.path.join(settings.MEDIA_ROOT, project.expected_results.name)
                    if os.path.exists(file_path):
                        email.attach_file(file_path)

                email.send()  # Send the email
            except Exception as e:
                return JsonResponse({'msg': str(e)}, status=400)

            # Success message and notification
            messages.success(request,
                             f'Your project details for {project.name} have been sent to {recipient_name} via email to {recipient_email} on {actual_time}')
            pygame_notify()  # Assuming pygame_notify is a custom function to handle notifications
            return redirect('view_projects')
    else:
        form = EmailForm()

    return render(request, 'emp/send.html', {'form': form, 'project': project})


@login_required
def assign_task(request, pk):
    project = get_object_or_404(Project, pk=pk)  # Get the project by ID

    # Handle form submission
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                task = form.save(commit=False)  # Don't save the task yet
                task.project = project  # Assign the task to the project
                task.user = request.user  # Assign the current user as the task creator
                task.save()  # Save the task to the database
                form.save_m2m()  # Save the ManyToMany relations (assigned_to)

                # Get the emails of the employees assigned to the task
                employee_emails = [employee.email for employee in task.assigned_to.all()]
                employee_names = ', '.join([str(employee) for employee in project.employees.all()])

                # Prepare the HTML email message
                html_message = f"""
                    <h1 style="color: #333;">New Task Assigned: {task.task}</h1>
                    <p style="font-size: 14px; color: #555;">
                        Dear Team,<br><br>
                        A new task has been assigned to you related to the project <strong>{project.name}</strong>.
                        Kindly review the updated details below:
                    </p>
                    <ul>
                        <li><strong>Project Name:</strong> {project.name}</li>
                        <li><strong>Description:</strong> {project.description}</li>
                        <li><strong>Budget:</strong> {project.estimated_budget}</li>
                        <li><strong>Current Status:</strong> {project.status}</li>
                        <li><strong>Received Project:</strong> {project.created_at}</li>
                        <li><strong>Due Date:</strong> {project.due_date}</li>
                        <li><strong>Team Members:</strong> {employee_names}</li>
                        <li><strong>Project Status:</strong> {project.status}</li>
                    </ul>
                    <ul>
                        <li><strong>Task:</strong> {task.task}</li>
                        <li><strong>Description:</strong> {task.description}</li>
                        <li><strong>Time Of Assign:</strong> {task.time_assigned_task}</li>
                        <li><strong>Task Due Date:</strong> {task.due_date}</li>
                        <li><strong>Task Completed:</strong> {task.completed}</li>
                    </ul>
                    <p style="font-size: 14px; color: #555;">
                        Kindly complete the task before {task.due_date}. <br>
                        Please contact the team for further details.<br>
                        <strong>Thank you,<br>Team Django</strong>
                    </p>
                """

                # Prepare the email
                email = EmailMessage(
                    subject=f'Project Update: {project.name}',
                    body=html_message,
                    from_email='vishaldudhabarve105@gmail.com',  # From email
                    to=employee_emails,  # List of employee emails
                )
                email.content_subtype = 'html'  # Set content type to HTML

                # Attach file if task has media
                if task.if_media:
                    file_path = os.path.join(settings.MEDIA_ROOT, task.if_media.name)
                    email.attach_file(file_path)

                # Send the email
                email.send(fail_silently=False)

                # Notify via voice (optional)
                engine = pyttsx3.init()
                engine.say(f'Task-related emails have been sent to employees successfully.')
                engine.runAndWait()

                # Flash success message and redirect
                messages.success(request, f'Task has been assigned successfully.')
                pygame_notify()
                return redirect('view_projects')

            except Exception as e:
                return JsonResponse({'msg': str(e)}, status=400)

    else:
        form = TaskForm()

    # For rendering the form
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())
    return render(request, 'emp/assign_task.html', {"form": form, 'project': project, 'actual_time': actual_time})

from django.conf import settings


def send_mailt(request):
    if request.method == 'POST':
        form = EmailFor(request.POST)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.user = request.user
            mail.save()
            body='Email by DjangoMail'
            try:
                send_mail(
                    subject=mail.subject,
                    message=mail.message, 
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[mail.to],  # This should be a list
                )
            except Exception as e:
                return JsonResponse({'msg': str(e)}, status=400)

            messages.success(request, f'Email sent To {mail.receivers_name}')
            pygame_notify()
            return redirect('send_mail')
    else:
        form = EmailFor()
    mails=Email.objects.filter(user=request.user)    # Create a new instance of the form if GET request
    return render(request, 'emp/email.html', {'form': form, 'mails':mails})

@login_required
def sent_box(request):
    mails=Email.objects.filter(user=request.user)
    return render(request,'emp/sentbox.html',{"mails":mails})


@login_required
def detail_email(request,pk):
    mail=get_object_or_404(Email, pk=pk, user=request.user)
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())
    return render(request,'emp/detail_mail.html',{'mail':mail,'actual_time':actual_time})

@login_required
def clear_email(request,pk):
    mail=get_object_or_404(Email, pk=pk, user=request.user)
    try:
        mail.delete()
    except Exception as e:
        return JsonResponse({'msg':str(e)}, status=400)
    messages.success(request,f'{mail.receivers_name} s mail has been deleted successfully')
    pygame_notify()
    return redirect('sent_box')    


@login_required
def view_tasks(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project, user=request.user)
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())
    return render(request, 'emp/view_tasks.html', {'tasks': tasks, 'project': project,'actual_time':actual_time})


# for notification
def pygame_notify():
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load your audio file (replace 'your_audio_file.mp3' with your actual file path)
    pygame.mixer.music.load('notification.wav')

    # Play the audio file
    pygame.mixer.music.play()

    time.sleep(2)

    # Stop the music after 4 seconds
    pygame.mixer.music.stop()

    # Deactivate pygame mixer (optional, but good practice)
    pygame.mixer.quit()

# bank area 
@login_required
def set_accounts(request,pk):
    employee=get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = BankForm(request.POST, request.FILES)
        if form.is_valid:
            try:
              bank=form.save(commit=False)
              bank.employee=employee
              bank.user=request.user
              bank.save()
              send_mail(
                  subject="Bank Account Attached",
                  message=f'''Hey There {employee.name} we have attached your bank account to you kindly review bank account info\n
                  'Bank Account:\n
                         Bank Name: {bank.bank_name}\n
                         IFSC Code: {bank.ifsc_code}\n 
                         Account Number: {bank.account_number}\n
                         UPI ID: {bank.upi_id}\n
                         Updated At: {bank.updated_at}\n 
                  If you face any issues with this info kindly contact us on example@gmail.com\n
                  Thank You Team Django.
                  ''',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[employee.email],         
              )
            except Exception as e:
                return JsonResponse({'msg':str(e)}, status=400)
            messages.success(request, f'Bank account attached successfully to {employee.name}')
            time.sleep(1)
            pygame_notify()
            return redirect('set_accounts',pk=employee.pk)
    else:
        form=BankForm
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())         
    return render(request,'emp/set_accounts.html', {'form':form, 'employee':employee,'actual_time':actual_time})

# for sendslips
import re
# end of import materials
import io
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def send_slips(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = SendSlipsForm(request.POST, request.FILES)

        if form.is_valid():
            salary_slip = form.save(commit=False)
            total_salary = salary_slip.basic_salary + (salary_slip.allowances or 0) - (salary_slip.deductions or 0)

            # Generate the salary slip image
            img = Image.new('RGB', (600, 400), color='white')
            d = ImageDraw.Draw(img)

            # Load a font (you can adjust this or load a specific font if needed)
            font = ImageFont.load_default()

            # Define starting position for text
            x_start = 10
            y_start = 10
            line_height = 30  # Define spacing between lines

            # Draw text on the image
            d.text((x_start, y_start), f"Salary Slip for: {salary_slip.month}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Company Name: {salary_slip.company_name}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Employee Name: {employee.name}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Employee Role: {employee.role}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Present Days: {salary_slip.present_days}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Basic Salary: {salary_slip.basic_salary}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Allowances: {salary_slip.allowances or 0}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Deductions: {salary_slip.deductions or 0}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Total Salary: {total_salary}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Payment Method: {salary_slip.payment_method}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Status: {salary_slip.status}", fill=(0, 0, 0), font=font)
            y_start += line_height
            d.text((x_start, y_start), f"Generated At: {salary_slip.created_at}", fill=(0, 0, 0), font=font)

            # Save the image to a BytesIO object
            image_io = io.BytesIO()
            img.save(image_io, 'PNG')
            image_io.seek(0)  # Move the pointer to the start of the file

            # Save the SalarySlip instance
            salary_slip.employee = employee
            salary_slip.user = request.user
            salary_slip.save()

            # Create a professional HTML structure for the email body
            html_content = f"""
            <html>
            <body>
                <h2 style="color: #4CAF50;">Salary Slip for {salary_slip.month}</h2>
                <p>Dear {employee.name},</p>
                <p>Hello {employee.name} Your salary for the month <strong>{salary_slip.month}</strong> has been generated. Below are the details:</p>
                
                <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
                    <tr style="background-color: #f2f2f2;">
                        <th>Detail</th>
                        <th>Amount</th>
                    </tr>
                    <tr>
                        <td>Basic Salary</td>
                        <td>{salary_slip.basic_salary}</td>
                    </tr>
                    <tr>
                        <td>Allowances</td>
                        <td>{salary_slip.allowances or 0}</td>
                    </tr>
                    <tr>
                        <td>Deductions</td>
                        <td>{salary_slip.deductions or 0}</td>
                    </tr>
                    <tr>
                        <td><strong>Total Salary</strong></td>
                        <td><strong>{total_salary}</strong></td>
                    </tr>
                </table>
                
                <p><strong>Payment Method:</strong> {salary_slip.payment_method}</p>
                <p><strong>Status:</strong> {salary_slip.status}</p>
                <p><strong>Generated At:</strong> {salary_slip.created_at}</p>
                <p>Thank you for your hard work!</p>
                
                <p>Best regards,</p>
                <p><strong>{salary_slip.company_name}</strong></p>
            </body>
            </html>
            """

            subject = 'Salary Credit'
            from_email = settings.EMAIL_HOST_USER
            to_email = [employee.email]

            # Create EmailMessage object
            email = EmailMessage(subject, html_content, from_email, to_email)

            # Attach the image from memory (BytesIO object)
            email.attach('salary_slip.png', image_io.getvalue(), 'image/png')

            # Set content_subtype to 'html' so that the email is rendered as HTML
            email.content_subtype = 'html'

            # Send email
            email.send()

            messages.success(request, f'Email with salary slip has been sent to {employee.name}.')
            pygame_notify()

    else:
        form = SendSlipsForm
    actual_time = time.strftime("%d-%m-%y %H:%M:%S", time.localtime())    
    return render(request, 'emp/send_slip.html', {'form': form,'actual_time':actual_time,'employee':employee})



# serializer
class EmployeeSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^name']
    pagination_class = MyCursorPagination
    throttle_classes = [AnoThrottle, UserThrottleRate]


    def get_queryset(self):
        user = self.request.user
        return Employee.objects.filter(user=user) 


class DocumentSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^employee']
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user=self.request.user
        return Document.objects.filter(user=user)


class AssetSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^asset_name']
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user=self.request.user
        return Assets.objects.filter(user=user)


class SalarySleepSet(viewsets.ModelViewSet):
    serializer_class = SalarySlipsSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^amount']
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user=self.request.user
        return SalarySlips.objects.filter(user=user)


class ProjectSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^name']
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user=self.request.user
        return Project.objects.filter(user=user)


class TaskSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['^task']
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user=self.request.user
        return Task.objects.filter(user=user)


class BankSet(viewsets.ModelViewSet):
    serializer_class= BankSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]
    filter_backends=[SearchFilter]
    pagination_class=MyPageNumberPagination

    def get_queryset(self):
        user=self.request.user
        return Banks.objects.filter(user=user)




   
