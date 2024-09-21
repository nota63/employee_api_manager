from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenObtainPairView

router = DefaultRouter()
router.register('emp', EmployeeSet, basename='emp')  # Removed trailing '/'
router.register('docs', DocumentSet, basename='docs')  # Removed trailing '/'
router.register('asset/', AssetSet, basename='asset')
router.register('slips/', SalarySleepSet, basename='slips')
router.register('project/', ProjectSet, basename='project')
router.register('task/', TaskSet, basename='task')


urlpatterns = [
    path('register_employee/', register_employee, name='register_employee'),
    path('emp_detail/<int:pk>/', emp_detail, name='emp_detail'),
    path('upload_docs/<int:pk>/', upload_docs, name='upload_docs'),
    path('emp/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
    path('assets/<int:pk>/', asset, name='assets'),
    path('delete_docs/<int:pk>/', delete_docs, name='delete_docs'),
    path('salary_slips/<int:pk>/', salary_slips, name='salary_slips'),
    path('delete_slips/<int:pk>/', delete_slips, name='delete_slips'),
    path('delete_asset/<int:pk>/', delete_asset, name='delete_asset'),
    path('delete_emp/<int:pk>/', delete_emp, name='delete_emp'),
    path('edit_emp/<int:pk>/', edit_emp, name='edit_emp'),
    path('guide/', guide, name='guide'),
    path('shutdown/', shutdown, name='shutdown'),
    path('create_project/', create_project, name='create_project'),
    path('view_projects/', view_projects, name='view_projects'),
    path('cancel_project/<int:pk>/', cancel_project, name='cancel_project'),
    path('update_project/<int:pk>/', edit_update_project, name='update_project'),
    path('send_project/<int:pk>/', send_project, name='send_project'),
    path('assign_task/<int:pk>/', assign_task, name='assign_task'),
    path('view_task/<int:pk>/', view_tasks, name='view_task'),
    path('send_mail/', send_mailt, name='send_mail'),
    path('detail_email/<int:pk>/', detail_email, name='detail_email'),
    path('sent_box/', sent_box, name='sent_box'),
    path('clear_email/<int:pk>/', clear_email, name='clear_email'),
]
