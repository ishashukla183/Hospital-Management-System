

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Count

from hospital_management_app.models import Appointment, Patient, Doctor, Receptionist, Medicine, Pharmacist, Prescription, Pending
from hospital_management_app.models import CustomUser
from hospital_management_app.emailBackend import EmailBackend


queryset = (Doctor.objects.values('specialization').annotate(count=Count('specialization')).order_by())


def pie_chart(request):
    result = []
    total = []
   
    for doctor in queryset:
        result.append(doctor['specialization'])
        total.append(doctor['count'])
    
    return render(request, 'hod_template/pie-chart.html', {
       "result" : result, "total" :total, 'results' : queryset
    })
total = Doctor.objects.all().count()

def pie_chart_patient(request):
    result = []
    total = []
   
    for doctor in queryset:
        result.append(doctor['specialization'])
        total.append(doctor['count'])
    
    return render(request, 'patient_template/pie-chart.html', {
       "result" : result, "total" :total, 'results' : queryset
    })
total = Doctor.objects.all().count() 


def pie_chart_doctor(request):
    result = []
    total = []
   
    for doctor in queryset:
        result.append(doctor['specialization'])
        total.append(doctor['count'])
    
    return render(request, 'doctor_template/pie-chart.html', {
       "result" : result, "total" :total, 'results' : queryset
    })
total = Doctor.objects.all().count() 


def pie_chart_receptionist(request):
    result = []
    total = []
   
    for doctor in queryset:
        result.append(doctor['specialization'])
        total.append(doctor['count'])
    
    return render(request, 'receptionist_template/pie-chart.html', {
       "result" : result, "total" :total, 'results' : queryset
    })
total = Doctor.objects.all().count() 


def pie_chart_pharmacist(request):
    result = []
    total = []
   
    for doctor in queryset:
        result.append(doctor['specialization'])
        total.append(doctor['count'])
    
    return render(request, 'pharmacist_template/pie-chart.html', {
       "result" : result, "total" :total, 'results' : queryset
    })
total = Doctor.objects.all().count() 

def receptionist_homepage(request):
    return render(request, 'receptionist_template/pie-chart.html')

def doctor_homepage(request):
    return render(request, 'doctor_template/pie-chart.html')
def patient_homepage(request):
    return render(request, 'patient_template/pie-chart.html') 
def pharmacist_homepage(request):
    return render(request, 'pharmacist_template/pie-chart.html') 
def showLoginPage(request):
    return render(request, "login_page.html")

def getLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        user = EmailBackend.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user!=None :
            login(request, user)
            if user.user_type == '1':
               return HttpResponseRedirect("admin_homepage")
            if user.user_type == '2':
                   return HttpResponseRedirect("receptionist_homepage")
            if user.user_type == '3':
                   return HttpResponseRedirect("doctor_homepage")
            if user.user_type == '4':
                   return HttpResponseRedirect("patient_homepage")
            if user.user_type == '5':
                   return HttpResponseRedirect("pharmacist_homepage")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")

def getUserDetails(request):
    if request.user!=None:
       return HttpResponse("User : " + request.user.email + " usertype : " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")
    
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect("/")
    
def patientSignUp(request):
    return render(request, 'patient_signup.html')

def add_patient_save(request):
     if request.method!="POST":
        return HttpResponseRedirect("<h2> Method not allowed </h2>")
     else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dob = request.POST.get("dob")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        username = request.POST.get("email")
        pwd = request.POST.get("password")
        phNo = request.POST.get("phno")
        try:
            user = CustomUser.objects.create_user(username = username, email = username, password = pwd, first_name = first_name, last_name = last_name, user_type = 4)
            user.patient.height =int(height)
            user.patient.weight = int(weight)
            user.patient.dob = dob
            user.patient.phNo = phNo 
            user.save()
            messages.success(request, "Success")
            return HttpResponseRedirect('/')
        except: 
            messages.error(request, "Failure")
            print("failure")
            return HttpResponseRedirect('/patientSignup')
      
def add_appointment(request):
    return render(request, 'receptionist_template/add_appointment_template.html')  

def add_appointment_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("<h2> Method not allowed </h2>")
    else:
        receptionist_id = request.user.receptionist.id
        receptionist = Receptionist.objects.get(id = receptionist_id)
        patient_id = int(request.POST.get("patient_id")) 
        patient = Patient.objects.get(id = patient_id)
        doctor_id = int(request.POST.get("doctor_id"))  
        doctor = Doctor.objects.get(id = doctor_id)
        time = request.POST.get("date") +" "+ request.POST.get("time")
        try:
            appointment_model = Appointment(receptionist_id = receptionist, patient_id = patient, doctor_id = doctor, time = time)
            appointment_model.save()
            messages.success(request, "Success")
            return HttpResponseRedirect("/add_appointment_template")
        except:
            messages.error(request, "Failure")
            print("failure")
            return HttpResponseRedirect('/patientSignup')

def add_medicine(request):
    return render(request, 'pharmacist_template/add_medicine_template.html')  

def add_medicine_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("<h2> Method not allowed </h2>")
    medicine_name = request.POST.get("medicine_name")
    try:
        medicine_model = Medicine(medicine_name = medicine_name)
        medicine_model.save()
        messages.success(request, "Success")
        return HttpResponseRedirect("/add_medicine_template")
    except:
         messages.error(request, "Failure")
         return HttpResponseRedirect("/add_medicine_template")   
     
def add_prescription(request):
    return render(request, 'doctor_template/add_prescription_template.html')  

def add_prescription_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("<h2> Method not allowed </h2>")
    patient_id = request.POST.get("patient_id")
    patient = Patient.objects.get(id = patient_id)
    doctor_id = request.user.doctor.id
    doctor = Doctor.objects.get(id = doctor_id)
    diagnosis = request.POST.get("diagnosis")
    treatment = request.POST.get("treatment")
    medicine_id = request.POST.get("medicine_id")
    medicine = Medicine.objects.get(id = medicine_id)
    
    try:
        prescription_model = Prescription(patient_id = patient, medicine_id = medicine, doctor_id = doctor, diagnosis = diagnosis, treatment = treatment)
        prescription_model.save()
        messages.success(request, "Success")
        return HttpResponseRedirect("/add_prescription_template")
    except: 
        messages.error(request, "Failure")
        return HttpResponseRedirect("/add_prescription_template")
    
def view_medicine(request):
    medicines = Medicine.objects.all()
    return render(request, "pharmacist_template/view_medicine_template.html", {"medicines":medicines})


def appointment_view(request):
    appointment_view = Appointment.objects.select_related('patient_id', 'doctor_id')
    return render (request, "receptionist_template/view_appointments_template.html", {"appointment_view" : appointment_view})

def view_doctors_receptionist(request):
    doctors = Doctor.objects.all()
    return render(request, "receptionist_template/view_doctors_template.html", {"doctors":doctors})

def view_doctors_patient(request):
    doctors = Doctor.objects.all()
    return render(request, "patient_template/view_doctors_patient.html", {"doctors":doctors})

def view_patients_receptionist(request):
    patients = Patient.objects.all()
    return render(request, "receptionist_template/view_patients_template.html", {"patients":patients})

def view_appointment_patient(request):
    appointments = Appointment.objects.filter(patient_id = request.user.patient.id).order_by('-time')
    return render (request, "patient_template/view_appointments_template.html", {"appointment_view" : appointments})

def view_appointment_doctor(request):
    appointments = Appointment.objects.filter(doctor_id = request.user.doctor.id).order_by('-time')
    return render (request, "doctor_template/view_appointments_template.html", {"appointment_view" : appointments})


def view_prescription_patient(request):
    prescriptions = Prescription.objects.filter(patient_id = request.user.patient.id).select_related("medicine_id", "doctor_id")
    return render(request, "patient_template/view_prescription_template.html", {"prescriptions" : prescriptions})

def view_patients_doctor(request):
    appointments = Appointment.objects.select_related('patient_id').filter(doctor_id = request.user.doctor.id, status = True)
    
    return render(request, "doctor_template/view_patients_template.html", {"appointments": appointments})

def view_prescription_doctor(request):
    prescriptions = Prescription.objects.filter(doctor_id = request.user.doctor.id).select_related("medicine_id", "patient_id")
    return render(request, "doctor_template/view_prescriptions_template.html", {"prescriptions" : prescriptions})

def edit_appointments(request, appointment_id):
    appointment = Appointment.objects.get(id = appointment_id)
    return render(request, "receptionist_template/edit_appointment_template.html", {"appointment" : appointment})


def edit_appointment_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("<h2> Method not allowed </h2>")
    else:
        appointment_id = request.POST.get("appointment_id")
        patient_id = int(request.POST.get("patient_id")) 
        patient = Patient.objects.get(id = patient_id)
        doctor_id = int(request.POST.get("doctor_id"))  
        doctor = Doctor.objects.get(id = doctor_id)
        time = request.POST.get("date") +" "+ request.POST.get("time")
        try:
            appointment_model = Appointment.objects.get(id = appointment_id)
            appointment_model.patient_id = patient
            appointment_model.doctor_id = doctor
            appointment_model.time = time
            appointment_model.save()
            messages.success(request, "Success")
            return HttpResponseRedirect("/appointment_view")
        except:
            messages.error(request, "Failure")
            print("failure")
            return HttpResponseRedirect('/appointment_view')
        
def edit_medicine(request, medicine_id):
    medicine = Medicine.objects.get(id = medicine_id)
    return render(request, "pharmacist_template/edit_medicine_template.html", { "medicine" : medicine})
def edit_medicine_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("<h2> Method not allowed </h2>")
    try:
        medicine_id = request.POST.get("medicine_id")
        medicine_name = request.POST.get("medicine_name")
        medicine_model = Medicine.objects.get(id = medicine_id)
        medicine_model.medicine_name = medicine_name
        medicine_model.save()
        messages.success(request, "Success")
        return HttpResponseRedirect("/view_medicine_template")
    except: 
        messages.error(request, "Failure")
        return HttpResponseRedirect("/view_medicine_template")
        
def request_appointment(request):
    return render(request, "patient_template/request_appointment_template.html")
def request_appointment_save(request):
    patient_id = request.user.patient.id
    patient = Patient.objects.get(id = patient_id)
    doctor_id = int(request.POST.get("doctor_id"))  
    doctor = Doctor.objects.get(id = doctor_id)
    date = request.POST.get("date")
    pending_model = Pending(patient_id = patient, doctor_id = doctor, date = date)
    pending_model.save()
    return HttpResponseRedirect("/request_appointment")
def cancel_appointment(request, appointment_id):
    try:
        appointment_model = Appointment.objects.get(id = appointment_id)
        appointment_model.status = False
        appointment_model.save()
        messages.success(request, "Success")
        if request.user.user_type == 3 :
            return HttpResponseRedirect("/view_appointment_doctor")
        else:
            return HttpResponseRedirect("/view_appointment_patient")
    except:
        messages.error(request, "Failure")
        if request.user.user_type == 3 :
            return HttpResponseRedirect("/view_appointment_doctor")
        else:
            return HttpResponseRedirect("/view_appointment_patient")


def view_pending(request):
    appointment_view = Pending.objects.filter(status= False).select_related('patient_id', 'doctor_id').order_by('date')
    return render (request, "receptionist_template/view_pending_requests.html", {"appointment_view" : appointment_view})

def view_pending_requests(request):
    appointment_view = Pending.objects.filter(patient_id = request.user.patient.id).select_related( 'doctor_id')
    return render (request, "patient_template/view_pending_requests.html", {"appointment_view" : appointment_view})