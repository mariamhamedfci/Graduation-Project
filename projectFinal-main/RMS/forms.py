from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from  django.contrib.auth.forms import UserCreationForm
from .models import  Applicant , company
from .models import *

class CreateNewUser(UserCreationForm):
    class Meta:
      model = User 
      
      fields = ['username' ,'email' ,'password1' ,'password2']


class ApplicantForms(ModelForm):
    class Meta:
      model = Applicant
      fields ="__all__"
      exclude = ['user'  , 'skills' ]



class CompanyForms(ModelForm):
    class Meta:
      model = company
      fields ="__all__"
      exclude = ['user','jobs', 'location']
      


class CreateNewjob(ModelForm):
    class Meta:
      model = job 
      fields ="__all__"
      exclude = ['companies','created_at','applicants']


class Createnoti(ModelForm):
    class Meta:
      model = Notification 
      fields ="__all__"
      exclude = ['timestamp']


class CreateNewjobAdmin(ModelForm):
    class Meta:
      model = job 
      fields ="__all__"
      exclude = ['created_at','applicants']


class JobForm(ModelForm):
    class Meta:
        model = job
        fields = '__all__' 
        exclude = ['companies','created_at','applicants']



class projectForm(ModelForm):
    class Meta:
        model = project
        fields = '__all__' 
        exclude = ['applicant']


class skilsForm(ModelForm):
    class Meta:
        model = skils
        fields = '__all__' 
        exclude = ['applicant']


class workexperienceForm(ModelForm):
    class Meta:
        model = workexperience
        fields = '__all__' 
        exclude = ['applicant']



class educationForm(ModelForm):
    class Meta:
        model = education
        fields = '__all__' 
        exclude = ['applicant']



class certificateForm(ModelForm):
    class Meta:
        model = certificate
        fields = '__all__' 
        exclude = ['applicant']






class ApplicantinfoForms(ModelForm):
    class Meta:
      model = Applicant
      fields ="__all__"
      exclude = ['user'  , 'skills' , 'about','volanteering','department']




class ApplicantbioForms(ModelForm):
    class Meta:
      model = Applicant
      fields ="__all__"
      exclude = ['user'  , 'name','volanteering','department','email','phone','jobname'
                 ,'userphoto','biography','location','birthdate','volanteering','department']




class ApplicantcontactForms(ModelForm):
    class Meta:
      model = Applicant
      fields ="__all__"
      exclude = ['user'  ,'volanteering','department','phone','jobname'
                 ,'userphoto','biography','volanteering','department','about']




class ApplicantvolForms(ModelForm):
    class Meta:
      model = Applicant
      fields ="__all__"
      exclude = ['user'  ,'about', 'name','biography','department','email','phone','jobname'
                 ,'userphoto','biography','location','birthdate','department']




class copamyinfo(ModelForm):
    class Meta:
      model = company
      fields ="__all__"
      exclude = ['user','companyphoto' ]
      
    
      


class userInfo(ModelForm):
    class Meta:
      model = Applicant
      fields ="__all__"
      exclude = ['user' ,'userphoto']



class OtherSectionForm(forms.ModelForm):
    class Meta:
        model = OtherSection
        fields ="__all__"
        exclude = ['applicant' ]




class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']        