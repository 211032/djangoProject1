from django.urls import path
from .views import login, employee_registration, home, employee_update_form, employee_update, change_password, \
    shiire_home, shiire_registration, shiire_list

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
    path('shiire_list/', shiire_list, name='shiire_list')



]
