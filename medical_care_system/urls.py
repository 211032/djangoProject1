from django.urls import path
from .views import login, employee_registration, home, employee_update_form, employee_update, change_password, \
    shiire_home, shiire_registration, shiire_list, shiire_search, patient_registration, insurance_change, \
    patient_search, patients

urlpatterns = [
    path('', login, name='index'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path('employee_registration/', employee_registration, name='employee_registration'),
    path('employee_update/', employee_update, name='employee_update'),
    path('employee_update_form', employee_update_form,  name='employee_update_form'),
    path('change_password/', change_password, name='change_password'),
    path('shiire_home/', shiire_home, name='shiire_home'),
    path('shiire_registration/', shiire_registration, name='shiire_registration'),
    path('shiire_list/', shiire_list, name='shiire_list'),
    path('shiire_search/', shiire_search, name='shiire_search'),
    path('patient_registration/', patient_registration, name='patient_registration'),
    path('insurance_change/', insurance_change, name='insurance_change'),
    path('patient_search/', patient_search, name='patient_search'),
    path('patients/', patients, name='patients'),



]
