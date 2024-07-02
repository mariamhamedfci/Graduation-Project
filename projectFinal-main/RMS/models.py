from django.db import models
from django.contrib.auth.models import Group,User




 
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,null=True)
    
    def __str__(self):
        return self.name
    
    


class company(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=1000,null=True)
    describtion=models.CharField(max_length=1000,null=True)
    companytype=models.CharField(max_length=100,null=True)
    about=models.CharField(max_length=1000,null=True)
    website=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=20,null=True)
    companyphoto=models.ImageField(blank=True,null=True,default="company.png")
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    followers = models.ManyToManyField(User, related_name='followed_companies', blank=True)


    def __str__(self):
       return str(self.name) if self.name else ''
    

    def get_number_of_companies():
        return company.objects.count()
   
  



class Applicant(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=20,null=True)
    email=models.CharField(max_length=100,null=True)
    phone= models.CharField(max_length=20,null=True)
    jobname=models.CharField(max_length=100,null=True)
    userphoto=models.ImageField(blank=True,null=True,default="user.png")
    biography=models.CharField(max_length=1000,null=True)
    about=models.CharField(max_length=1000,null=True)
    location=models.CharField(max_length=40,null=True)
    birthdate=models.DateField(max_length=40,null=True)
    volanteering=models.CharField(max_length=1000,null=True)
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    def __str__(self):
         return str(self.name) if self.name else ''
    
    def get_number_of_applicants():
        return Applicant.objects.count()

 


class skils(models.Model):
   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    applicant = models.ManyToManyField(Applicant)
    def __str__(self):
        return self.name

 
class project(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,null=True)
    role=models.CharField(max_length=1000,null=True)
    tools=models.CharField(max_length=1000,null=True)
    describtion=models.CharField(max_length=1000,null=True)
    applicant = models.ManyToManyField(Applicant)    
     
    def __str__(self):
        return self.title




 
class workexperience(models.Model):
    id = models.AutoField(primary_key=True)
    companyworked=models.CharField(max_length=100,null=True)
    jobworked=models.CharField(max_length=1000,null=True)
    describtion=models.CharField(max_length=1000,null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,null=True) 
    
    def __str__(self):
        return self.id




from django.db import models
from django.utils import timezone

class job(models.Model):
    id = models.AutoField(primary_key=True)
    salary = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=40, null=True)
    education = models.CharField(max_length=1000, null=True)
    workexperience = models.CharField(max_length=1000, null=True)
    technicalskills = models.CharField(max_length=1000, null=True)
    achievements = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    deletion_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True) 
    companies = models.ManyToManyField('company')
    applicants = models.ManyToManyField('Applicant')
    number_of_positions = models.IntegerField(default=1)  # New field
    

    def __str__(self):
        return self.title

    class Meta:
        get_latest_by = 'created_at'

    @staticmethod
    def get_number_of_jobs():
        return job.objects.count()

    def is_active_job(self):
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date




class OtherSection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    describtion=models.CharField(max_length=1000,null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name



class certificate(models.Model):
    id = models.AutoField(primary_key=True)
    place=models.CharField(max_length=1000,null=True)
    major=models.CharField(max_length=1000,null=True)
    about=models.CharField(max_length=1000,null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,null=True)
   
    def __str__(self):
        return self.major
          
          

class education(models.Model):
    
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=1000,null=True)
    degree=models.CharField(max_length=1000,null=True)
    major=models.CharField(max_length=1000,null=True)
    fromto=models.CharField(max_length=1000,null=True)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,null=True)
   
    def __str__(self):
        return self.title
          

class cv(models.Model):
   
    def __str__(self):
        return self
    

class Item(models.Model):
    def __str__(self):
        return self






class jobstatus(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(job, on_delete=models.CASCADE)
    percentage = models.FloatField(default=0)

    def __str__(self):
         return str(self.job) if self.job else ''

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message    
