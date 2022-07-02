"""hospital_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from hospital_management import settings
from hospital_management_app.views import request_appointment_save
from hospital_management_app import views, HODviews
urlpatterns = [
   
    path('', views.showLoginPage), 
    path('login', views.getLogin),
    path('get_user_details', views.getUserDetails),
    path('logout', views.logoutUser),
    path('admin/', admin.site.urls),
     path('pie-chart/', views.pie_chart, name='pie-chart'),
      path('patient_homepage/', views.pie_chart_patient, name='pie-chart'),
    path("admin_homepage", views.pie_chart, name='pie-chart' ),
    path("add_appointment_template", views.add_appointment),
    path("add_doctors_template", HODviews.add_doctors),
    path("add_pharmacist_template", HODviews.add_pharmacist),
    path("add_doctor_save", HODviews.add_doctor_save),
    path("add_pharmacist_save", HODviews.add_pharmacist_save),
    path("add_receptionist_template", HODviews.add_receptionist),
    path("add_receptionist_save", HODviews.add_receptionist_save),
    path("patientSignup", views.patientSignUp ),
    path("patientSave", views.add_patient_save ),
   
    path("doctor_homepage", views.pie_chart_doctor, name = 'pie-chart'),
    path("receptionist_homepage", views.pie_chart_receptionist, name = 'pie-chart'),
    path("pharmacist_homepage", views.pie_chart_pharmacist, name = 'pie-chart'),
    path("add_appointment_save", views.add_appointment_save),
    path("add_medicine_template", views.add_medicine),
    path("add_medicine_save", views.add_medicine_save),
    path("add_prescription_template", views.add_prescription),
    path("add_prescription_save", views.add_prescription_save),
    path("view_doctors", HODviews.view_doctors),
     path("view_doctors_receptionist", views.view_doctors_receptionist),
     path("view_doctors_patient", views.view_doctors_patient),
      path("view_patients_receptionist", views.view_patients_receptionist),
    path("view_receptionists", HODviews.view_receptionists),
    path("view_patients", HODviews.view_patients),
    path("view_pharmacists", HODviews.view_pharmacists),
    path("view_medicine_template", views.view_medicine),
    path("appointment_view", views.appointment_view),
    path("view_appointment_patient", views.view_appointment_patient),
    path("view_appointment_doctor", views.view_appointment_doctor),
    path("view_prescription_patient", views.view_prescription_patient),
    path("view_prescriptions", views.view_prescription_doctor),
    path("view_patients_doctor", views.view_patients_doctor),
    path("edit_doctor/<str:doctor_id>", HODviews.edit_doctor),
    path("delete_doctor/<str:doctor_id>", HODviews.delete_doctor),
    path("edit_doctor_save", HODviews.edit_doctor_save),
    path("edit_receptionist/<str:receptionist_id>", HODviews.edit_receptionist),
    path("edit_receptionist_save", HODviews.edit_receptionist_save),
    path("edit_receptionist", HODviews.edit_receptionist),
    path("delete_receptionist", HODviews.delete_receptionist),
    path("edit_pharmacist/<str:pharmacist_id>", HODviews.edit_pharmacist),
    path("delete_pharmacist/<str:pharmacist_id>", HODviews.delete_pharmacist),
    path("edit_pharmacist_save", HODviews.edit_pharmacist_save),
    path("edit_appointment/<str:appointment_id>", views.edit_appointments),
    path("edit_appointment_save", views.edit_appointment_save),
    path("cancel_appointment/<str:appointment_id>", views.cancel_appointment),
    path("edit_medicine/<str:medicine_id>", views.edit_medicine),
    path("edit_medicine_save", views.edit_medicine_save),
    path("request_appointment", views.request_appointment),
    path("request_appointment_save", views.request_appointment_save),
    path("view_pending", views.view_pending),
    path("view_pending_requests", views.view_pending_requests),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

