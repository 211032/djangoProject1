from django.urls import path
from .views import login, employee_registration, home, employee_update_form, employee_update, change_password, \
    shiire_home, shiire_registration, shiire_list, shiire_search, patient_registration, patient_insurance_change, \
    patient_search, patients, confirm_prescription, prescribe_medicine, doctor_home, prescription_list, \
    treatment_history, treatment_history_results, reception_home, tabyouin_home, tabyouin_registration, tabyouin_list, \
    tabyouin_search, tabyouin_update, tabyouin_update_confirm, tabyouin_update_save

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
    path('reception_home/', reception_home, name='reception_home'),
    path('patient_registration/', patient_registration, name='patient_registration'),
    path('patient_insurance_change/', patient_insurance_change, name='patient_insurance_change'),
    path('patient_search/', patient_search, name='patient_search'),
    path('patients/', patients, name='patients'),
    path('doctor_home/', doctor_home, name='doctor_home'),
    path('prescribe_medicine/', prescribe_medicine, name='prescribe_medicine'),
    path('confirm_prescription/', confirm_prescription, name='confirm_prescription'),
    path('prescription_list/', prescription_list, name='prescription_list'),
    path('treatment_history/', treatment_history, name='treatment_history'),
    path('treatment_history_results/<str:patid>/', treatment_history_results, name='treatment_history_results'),
    path('tabyouin_home', tabyouin_home, name='tabyouin_home'),
    path('tabyouin/register/', tabyouin_registration, name='tabyouin_registration'),
    path('tabyouin/list/', tabyouin_list, name='tabyouin_list'),
    path('tabyouin/search/', tabyouin_search, name='tabyouin_search'),

    path('tabyouin/update/search/', tabyouin_update, name='tabyouin_update_search'),
    path('tabyouin/update/confirm/', tabyouin_update_confirm, name='tabyouin_update_confirm'),
    path('tabyouin/update/save/', tabyouin_update_save, name='tabyouin_update_save'),


]
