from django.urls import path
from .views import login, employee_registration, home, employee_update_form, employee_update, change_password

urlpatterns = [
    path('', login, name='index'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path('employee_registration/', employee_registration, name='employee_registration'),
    path('employee_update/', employee_update, name='employee_update'),
    path('employee_update_form', employee_update_form,  name='employee_update_form'),
    path('change_password/', change_password, name='change_password')


]
