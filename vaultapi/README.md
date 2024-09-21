Employee API Manager
The Employee API Manager is a Django-based application designed to manage employees, their assets, documents, salary slips, and more. This project incorporates robust features such as API management using Django Rest Framework, JWT authentication, and custom paginations and throttling.

Table of Contents
Project Overview
Features
Technologies Used
Installation & Setup
API Endpoints
Screenshots
Usage Examples
Contributions
License
Project Overview
The Employee API Manager allows organizations to manage employee data, assets, documents, and salary slips efficiently. It provides a comprehensive API with features like:

Employee registration and management
Uploading and managing documents
Managing assets and salary slips
User authentication and permissions using JWT
Efficient API pagination and throttling
Features
User Authentication: JWT and session-based authentication.
Employee Management: Add, edit, delete, and retrieve employee details.
Document Uploads: Attach and manage documents related to employees.
Asset Management: Register and manage assets assigned to employees.
Salary Slips: Upload, view, and manage salary slips.
System Monitoring: Display system information such as CPU usage, memory, disk space, etc.
Technologies Used
Django: Backend framework for building the application.
Django Rest Framework: To create APIs for employee, asset, and document management.
JWT Authentication: Secure API endpoints using JWT.
Psutil: For system monitoring (CPU, memory, network usage).
PyAutoGUI: For automating input actions.
HTML/CSS: For rendering the frontend templates.
Installation & Setup
Clone the repository:

bash
Copy code
git clone https://github.com/your-repo/employee-api-manager.git
cd employee-api-manager
Create a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply migrations:

bash
Copy code
python manage.py migrate
Create a superuser to access the admin panel:

bash
Copy code
python manage.py createsuperuser
Run the Django development server:

bash
Copy code
python manage.py runserver
API Endpoints
Employees
GET /api/employees/: List all employees.
POST /api/employees/: Register a new employee.
GET /api/employees/{id}/: Get details of a specific employee.
PUT /api/employees/{id}/: Update employee details.
DELETE /api/employees/{id}/: Delete an employee.
Assets
GET /api/assets/: List all assets.
POST /api/assets/: Register a new asset.
GET /api/assets/{id}/: Get details of a specific asset.
PUT /api/assets/{id}/: Update asset details.
DELETE /api/assets/{id}/: Delete an asset.
Documents
GET /api/documents/: List all documents.
POST /api/documents/: Upload a new document.
GET /api/documents/{id}/: Get details of a specific document.
DELETE /api/documents/{id}/: Delete a document.
Salary Slips
GET /api/salaryslips/: List all salary slips.
POST /api/salaryslips/: Upload a new salary slip.
GET /api/salaryslips/{id}/: Get details of a specific salary slip.
DELETE /api/salaryslips/{id}/: Delete a salary slip.
Screenshots
Employee Dashboard:

Asset Management:

Salary Slips:

Usage Examples
Registering an Employee
python
Copy code
import requests

url = 'http://127.0.0.1:8000/api/employees/'
data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'designation': 'Software Engineer',
    # other fields...
}

headers = {
    'Authorization': 'Bearer your_jwt_token_here'
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
Fetching Employee Details
python
Copy code
response = requests.get('http://127.0.0.1:8000/api/employees/1/')
print(response.json())
Contributions
Feel free to contribute by submitting a pull request or opening an issue for any bugs or features.

License
This project is licensed under the MIT License.