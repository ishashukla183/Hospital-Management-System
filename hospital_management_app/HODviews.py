
import email
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from hospital_management_app.models import Doctor, Patient, Pharmacist, Receptionist

from django.db.models import Count
from hospital_management_app.models import CustomUser
result = (Doctor.objects
    .values('specialization')
    .annotate(count=Count('specialization'))
    .order_by()
)

total = Doctor.objects.all().count()
def admin_homepage(request):
    return render(request, 'hod_template/home_template.html', )

def add_doctors(request):
    return render(request, 'hod_template/add_doctors_template.html')

def add_pharmacist(request):
    return render(request, 'hod_template/add_pharmacist_template.html')




def add_doctor_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("email")
    pwd = request.POST.get("password")
    phNo = request.POST.get("phno")
    specialization = request.POST.get("specialization")
    try:
        user = CustomUser.objects.create_user(username=username, password = pwd,last_name=last_name, first_name=first_name, email=username, user_type = 3)
        user.doctor.specialization = specialization
        user.doctor.phNo = phNo
        user.save()
        print("success")
        messages.success(request, "Success")
        return HttpResponseRedirect('/add_doctors_template')
    except: 
        messages.error(request, "Failure")
        print("failure")
        return HttpResponseRedirect('/add_doctors_template')
    
    
def add_receptionist(request):
        return render(request, 'hod_template/add_receptionist_template.html')

def add_receptionist_save(request):
     if request.method!="POST":
        return HttpResponse("Method Not Allowed")
     
     else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("email")
        pwd = request.POST.get("password")
        phNo = request.POST.get("phno")
        try:
            user = CustomUser.objects.create_user(username=username, password = pwd,last_name=last_name, first_name=first_name, email=username, user_type = 2)
            user.receptionist.phNo = int(phNo)
            user.save()
            user.receptionist.save()
            print("success")
            messages.success(request, "Success")
            return HttpResponseRedirect('/add_receptionist_template')
        except: 
            messages.error(request, "Failure")
            print("failure")
            return HttpResponseRedirect('/add_receptionist_template')
        
        
def add_pharmacist_save(request):
     if request.method!="POST":
        return HttpResponse("Method Not Allowed")
     
     else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("email")
        pwd = request.POST.get("password")
        phNo = request.POST.get("phno")
        try:
            user = CustomUser.objects.create_user(username=username, password = pwd,last_name=last_name, first_name=first_name, email=username, user_type = 5)
            user.pharmacist.phNo = int(phNo)
            user.save()
            user.pharmacist.save()
            print("success")
            messages.success(request, "Success")
            return HttpResponseRedirect('/add_pharmacist_template')
        except: 
            messages.error(request, "Failure")
            print("failure")
            return HttpResponseRedirect('/add_pharmacist_template')


def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, "hod_template/view_doctors_template.html", {"doctors":doctors})

def view_receptionists(request):
    receptionists = Receptionist.objects.all()
    return render(request, "hod_template/view_receptionists_template.html", {"receptionists":receptionists})

def view_patients(request):
    patients = Patient.objects.all()
    return render(request, "hod_template/view_patients_template.html", {"patients":patients})

def view_pharmacists(request):
    pharmacists = Pharmacist.objects.all()
    return render(request, "hod_template/view_pharmacists_template.html", {"pharmacists":pharmacists})

def edit_doctor_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        doctor_id = request.POST.get("doctor_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("email")
        phNo = request.POST.get("phno")
        specialization = request.POST.get("specialization")
        try:
            user = CustomUser.objects.get(id = doctor_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = username
            user.username = username
            user.save()
            
            doctor_model = Doctor.objects.get(admin = doctor_id)
            doctor_model.phNo = phNo
            doctor_model.specialization = specialization
            doctor_model.save()
            messages.success(request, "Success")
            return HttpResponseRedirect('/view_doctors')
        except:
           messages.error(request, "Failure")
           return HttpResponseRedirect('/view_doctors')
     
       


def edit_doctor(request, doctor_id):
   doctor = Doctor.objects.get(admin = doctor_id)
   return render(request, "hod_template/edit_doctor_template.html", {"doctor" : doctor})

def edit_receptionist(request, receptionist_id):
    receptionist = Receptionist.objects.get(admin = receptionist_id)
    return render(request, "hod_template/edit_receptionist_template.html", {"receptionist" : receptionist})

def edit_receptionist_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        receptionist_id = request.POST.get("receptionist_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("email")
        phNo = request.POST.get("phno")
        try:
            user = CustomUser.objects.get(id = receptionist_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = username
            user.username = username
            user.save()
            
            receptionist_model = Receptionist.objects.get(admin = receptionist_id)
            receptionist_model.phNo = phNo
           
            receptionist_model.save()
            messages.success(request, "Success")
            return HttpResponseRedirect('/view_receptionists')
        except:
           messages.error(request, "Failure")
           return HttpResponseRedirect('/view_receptionists')
       
       
def edit_pharmacist(request, pharmacist_id):
    pharmacist = Pharmacist.objects.get(admin = pharmacist_id)
    return render(request, "hod_template/edit_pharmacist_template.html", {"pharmacist" : pharmacist})

def delete_doctor(request, doctor_id):
    CustomUser.objects.filter(id = doctor_id).delete()
   
    return HttpResponseRedirect("/view_doctors")

def delete_pharmacist(request, pharmacist_id):
    CustomUser.objects.filter(id = pharmacist_id).delete()
    
    return HttpResponseRedirect("/view_pharmacists")

def delete_receptionist(request, receptionist_id):
    CustomUser.objects.filter(id = receptionist_id).delete()
    
    return HttpResponseRedirect("/view_receptionists")

def edit_pharmacist_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        pharmacist_id = request.POST.get("pharmacist_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("email")
        phNo = request.POST.get("phno")
        #try:
        user = CustomUser.objects.get(id = pharmacist_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = username
        user.username = username
        user.save()
        
        pharmacist_model = Pharmacist.objects.get(admin = pharmacist_id)
        pharmacist_model.phNo = phNo
        pharmacist_model.save()
        messages.success(request, "Success")
        return HttpResponseRedirect('/view_pharmacists')
    #except:
        messages.error(request, "Failure")
        return HttpResponseRedirect('/view_pharmacists')
            
        

