

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminHOD"), (2, "Receptionist"), (3, "Doctor"), (4, "Patient"), (5, "Pharmacist"))
    user_type = models.CharField(default=1, choices = user_type_data, max_length=10)
    
class AdminHOD(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at =  models.DateTimeField(auto_now_add = True)
    objects = models.Manager()


class Doctor(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phNo = models.DecimalField(max_digits=10, decimal_places=0, default = '000000000')
    specialization =  models.CharField(max_length = 255, default = "General")
    objects = models.Manager()
    
class Patient(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phNo = models.DecimalField(max_digits=10, decimal_places=0, default = '000000000')
    dob = models.DateField(default = '2022-05-26')
    height = models.DecimalField(max_digits=4, decimal_places=1, default = 160)
    weight = models.DecimalField(max_digits=4, decimal_places=1, default = 80)
    objects = models.Manager()
    
    
class Receptionist(models.Model):
    id = models.AutoField(primary_key = True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phNo = models.DecimalField(max_digits=10, decimal_places=0)
    objects = models.Manager()




class Appointment(models.Model):
    id = models.AutoField(primary_key = True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    receptionist_id = models.ForeignKey(Receptionist, on_delete=models.CASCADE)
    time = models.DateTimeField()
    status = models.BooleanField(default = True)
    objects = models.Manager()

class Pending(models.Model):
    id = models.AutoField(primary_key = True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default = False)
    
class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=255)
    
class Prescription(models.Model):
    id = models.AutoField(primary_key = True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, null= True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()



class Pharmacist(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phNo = models.DecimalField(max_digits=10, decimal_places=0)
    objects = models.Manager()




@receiver(post_save, sender = CustomUser)

def create_user_profile(sender, instance, created, **kwargs):
    if(created):
        if instance.user_type == 1:
            AdminHOD.objects.create(admin = instance)
        if instance.user_type == 3:
            Doctor.objects.create(admin=instance, phNo = 120201211, specialization = "General")
        if(instance.user_type == 2):
            Receptionist.objects.create(admin=instance, phNo = 120201211)
        if(instance.user_type == 4):
            Patient.objects.create(admin = instance, phNo =120201211, height = 0, weight = 0, dob = '2022-05-26')
        if(instance.user_type == 5):
            Pharmacist.objects.create(admin = instance, phNo =120201211)
        

@receiver(post_save, sender = CustomUser)
def save_user_profile(sender,  instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.receptionist.save()
    if instance.user_type == 3 :
        instance.doctor.save()
    if instance.user_type == 4:
        instance.patient.save()
    if instance.user_type == 5:
        instance.pharmacist.save()
        
        
# Trigger used :         
# delimiter //
# CREATE trigger CHANGE_STATUS_PENDING AFTER INSERT on hospital_management_app_appointment for each row begin update hospital_management_app_pending set status = True where hospital_management_app_pending.patient_id_id = new.patient_id_id and hospital_management_app_pending.doctor_id_id = new.doctor_id_id ; end; //
# delimiter ;


