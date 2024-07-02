
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
import numpy as np

from django.shortcuts import render
from .models import education
from .models import job
from .models import workexperience
from .models import certificate



import json
from django.views.decorators.csrf import csrf_exempt
from sentence_transformers import SentenceTransformer
from .models import *
from .models import company
from .forms import CreateNewUser
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .decorators import allowedUsers
from django.contrib.auth.models import Group
from .forms import *
import json
from django.views.decorators.csrf import csrf_exempt
from sentence_transformers import SentenceTransformer
from .filters import * 


from django.shortcuts import render, get_object_or_404


from .utils import send_notification

@login_required(login_url='welcome')
def home(request):
    companies = company.objects.all()
    
    companyfilter = companyFilter(request.GET, queryset=companies)
    companies = companyfilter.qs

    return render(request, "RMS/home.html", {'companies': companies, 'companyfilter': companyFilter})



def welcome(request):
     return render(request,"RMS/welcome.html")



def userLogin(request):  
    if request.user.is_authenticated:
        if request.user.groups.filter(name='admin').exists():
            return redirect('dashboard')  
        else:
            return redirect('/') 
    else :
      if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if request.user.groups.filter(name='company').exists():
                           return redirect('profileinfo')  
                    elif request.user.groups.filter(name='applicant').exists():
                             return redirect('userinfo')  
                else:
                    messages.error(request, 'Invalid username or password.')    
      return render(request, 'RMS/login.html')
   





def userLogout(request):
     logout(request)
     return redirect ('login')



def register (request):
   if request.user.is_authenticated:
          return redirect('/')
   else :
          form = CreateNewUser()
          if request.method == 'POST' :   
                 form = CreateNewUser(request.POST)
                 if form.is_valid():
                         user = form.save()
                         username = form.cleaned_data.get('username')
                         registration_type = request.POST.get('registration_type', '')
                         if registration_type == 'applicant':
                              group = Group.objects.get(name="applicant")
                              
                         elif registration_type == 'company':
                              group = Group.objects.get(name="company")
  
                         else:
                              group = None
                       
                         if group:
     
                            user.groups.add(group)
                            messages.success(request , username + 'Create Successfully !')
                            return redirect('login')
          context = {'form' : form }
          return render(request ,"RMS/register.html"  ,context )



@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def userprofile(request):
     return render(request,"RMS/userprofile.html")


@login_required(login_url= 'login')
def companyprofile(request):#,company_id)
     #company_instance = get_object_or_404(company, .id=company_id)
     return render(request,"RMS/companyprofile.html")#,{'company'}): company_instance})

@login_required(login_url='login')
def followers(request):
    company_instance = request.user.company
    followers = company_instance.followers.all()
    
    followers_data = []
    for follower in followers:
        try:
            applicant = Applicant.objects.get(user=follower)
            followers_data.append({
                'id': applicant.id,
                'username': follower.username,
                'photo_url': applicant.userphoto.url,
                'profile_url': 'applicantprof',
                'is_applicant': True
            })
        except Applicant.DoesNotExist:
            company_follower = company.objects.get(user=follower)
            followers_data.append({
                'id': company_follower.id,
                'username': follower.username,
                'photo_url': company_follower.companyphoto.url,
                'profile_url': 'companyPro',
                'is_applicant': False
            })
    
    context = {
        'followers': followers_data
    }
    
    return render(request, 'RMS/followers.html', context)

@login_required(login_url= 'login')
def department(request):
     return render(request,"RMS/department.html")

@login_required(login_url='login')
def noti(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, "RMS/noti.html", {'notifications': notifications})

@login_required(login_url='login')
def follow_unfollow_company(request, company_id):
    company_instance = get_object_or_404(company, id=company_id)

    # Prevent the company from following itself
    if request.user == company_instance.user:
        return redirect('noti')

    if request.user in company_instance.followers.all():
        company_instance.followers.remove(request.user)
        send_notification(request.user, company_instance.user, company_instance, action='unfollow')
    else:
        company_instance.followers.add(request.user)
        send_notification(request.user, company_instance.user, company_instance, action='follow')

    return redirect('noti')
    



@login_required(login_url= 'login')
def test(request):
     return render(request,"RMS/test.html")




@login_required(login_url= 'login')
def companies(request):
    department = None
    
    if hasattr(request.user, 'company'):
     
        department = request.user.company.department
    elif hasattr(request.user, 'applicant'):
       
        department = request.user.applicant.department

    if department:
        companies_in_department = company.objects.filter(department=department)
        
        companyfilter=companyFilter(request.GET,queryset=companies_in_department)

        companies_in_department=companyfilter.qs
        return render(request, "RMS/companies.html", {'companies': companies_in_department ,'companyfilter':companyFilter})
    else:
    
        return render(request, "RMS/companies.html", {'companies': []})


@login_required(login_url= 'login')
def applicantsdepartment(request):
    department = None
    
    # Check if the user is a company or an applicant
    if hasattr(request.user, 'company'):
        # User is a company
        department = request.user.company.department
    elif hasattr(request.user, 'applicant'):
        # User is an applicant
        department = request.user.applicant.department

    if department:
        applicants_in_department = Applicant.objects.filter(department=department)
        applicantfilter=applicantFilter(request.GET,queryset=applicants_in_department)
        applicants_in_department=applicantfilter.qs
        return render(request, "RMS/applicantsdepartment.html", {'applicants': applicants_in_department,'applicantfilter':applicantFilter})
    else:
        
        return render(request, "RMS/applicantsdepartment.html", {'applicants': []})
    


@login_required(login_url= 'login')
def department(request):
    department_list = Department.objects.all()
    return render(request, "RMS/department.html", {'department_list': department_list})



@login_required(login_url= 'login')
def usercv(request):
     return render(request,"RMS/usercv.html")





@login_required(login_url= 'login')
def changepassword(request):
     return render(request,"RMS/changepassword.html")

@login_required(login_url= 'login')
def usereducation(request):
     return render(request,"RMS/usereducation.html")


@login_required(login_url= 'login')
def userexperience(request):
     return render(request,"RMS/userexperience.html")



@login_required(login_url= 'login')
def usercertificates(request):
     return render(request,"RMS/usercertificates.html")

@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def addusercertificates(request):
     return render(request,"RMS/addusercertificates.html")

@login_required(login_url= 'login')
def userprojects(request):
     return render(request,"RMS/userprojects.html")

    
@login_required(login_url= 'login')
def usersections(request):
     return render(request,"RMS/usersections.html")


@login_required(login_url= 'login')
def userskills(request):
     return render(request,"RMS/userskills.html")

@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def addskills(request):
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name')  
        applicant = request.user.applicant  
        

    
        skill = skils.objects.create(name=skill_name)
        skill.applicant.add(applicant)
        skill.save()

        return redirect('usercv') 

    return render(request, "RMS/addskills.html")



@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def addusereducation(request):
     if request.method == 'POST':
        title = request.POST.get('title')
        degree = request.POST.get('degree')
        major = request.POST.get('major')
        fromto = request.POST.get('fromto')
        applicant = request.user.applicant 
       
        new_education = education.objects.create(
            title=title,
            degree=degree,
            major=major,
            fromto=fromto,
            applicant=applicant
        )
        return redirect('usercv')  

     return render(request,"RMS/addusereducation.html")


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def addsection(request):
    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        describtion = request.POST.get('describtion')
        applicant = request.user.applicant
        section = OtherSection.objects.create(name=section_name, describtion=describtion, applicant=applicant)
        return redirect('usercv') 
    
    applicant_sections = request.user.applicant.othersection_set.all()
    return render(request, "RMS/addsection.html",{'sections': applicant_sections})


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def adduserexperience(request):
     if request.method == 'POST':
        companyworked = request.POST.get('companyworked')
        jobworked = request.POST.get('jobworked')
        describtion = request.POST.get('describtion')
        applicant = request.user.applicant 
     
        new_education = workexperience.objects.create(
            companyworked=companyworked,
            jobworked=jobworked,
            describtion=describtion,
            applicant=applicant
        )
       
        return redirect('usercv')

     return render(request,"RMS/adduserexperience.html")


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def addproject(request):
   
     if request.method == 'POST':
        title = request.POST.get('title')
        role = request.POST.get('role')
        tools = request.POST.get('tools')
        describtion = request.POST.get('describtion')
        applicant = request.user.applicant

     
        new_project = project.objects.create(
            title=title,
            role=role,
            tools=tools,
            describtion=describtion
        )
        applicant.project_set.add(new_project)

        return redirect('usercv')




     return render(request,"RMS/addproject.html")

@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def addusercertificates(request):
     if request.method == 'POST':
        place = request.POST.get('place')
        major = request.POST.get('major')
        about = request.POST.get('about')
        applicant = request.user.applicant

       
        new_certificate = certificate.objects.create(
            place=place,
            major=major,
            about=about,
           
        )
        applicant.certificate_set.add(new_certificate)

        return redirect('usercv')




     return render(request,"RMS/addusercertificates.html")


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})
def JobRequirements(request):
    form = CreateNewjob()
    if request.method == 'POST':
        form = CreateNewjob(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            company = request.user.company
            job.companies.add(company)
            
            # Send notifications to followers
            followers = company.followers.all()
            for follower in followers:
                send_notification(user_from=request.user, user_to=follower, company=company, action='new_job', job=job)
            
            return redirect('companyprofile')
    
    context = {'form': form}
    return render(request, "RMS/JobRequirements.html", context)



@login_required(login_url= 'register')
@allowedUsers(allowedGroups={'admin','company'})
def profileinfo(request):
     if request.method == 'POST':
        form = copamyinfo(request.POST, request.FILES)  
        if form.is_valid():
            new_company = form.save(commit=False)
            new_company.user = request.user  
            new_company.save()
            
            return redirect('/')
        
     else:
        form = copamyinfo(initial={'user': request.user}) 
 
     if hasattr(request.user, 'company'):
             return redirect('/')  
     else:
             contxet={'form':form} 
             return render(request,"RMS/profileinfo.html", contxet) 
     
    


@login_required(login_url= 'register')
@allowedUsers(allowedGroups={'admin','applicant'})
def userinfo(request):
     if request.method == 'POST':
        form = userInfo(request.POST, request.FILES)  
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user  
            new_user.save()
            return redirect('/')
     else:
        form = userInfo(initial={'user': request.user}) 
     
     if hasattr(request.user, 'applicant'):
             return redirect('/')
     else:
             contxet={'form':form}
             return render(request,"RMS/userinfo.html",contxet)
         

    


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})
def NewJob(request):
     return render(request,"RMS/NewJob.html")

@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin', 'company'})
def Status(request, job_id):
    job_instance = get_object_or_404(job, id=job_id)
    # Retrieve top applicants list
    number_of_applicants = job_instance.number_of_positions
    
    job_status_list = jobstatus.objects.filter(job=job_instance).order_by('-percentage')[:number_of_applicants]

    return render(request, "RMS/Status.html", {'job_status_list': job_status_list})



@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})
def jobsStatus(request): 
    company = request.user.company  # Adjust this line according to your actual user-company relationship
    job_status_list = jobstatus.objects.filter(company=company).order_by('-percentage')
    return render(request, "RMS/jobsStatus.html", {'job_status_list': job_status_list})


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})
def JobsHistory(request):
     return render(request,"RMS/JobsHistory.html")




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})
def EditCompanyProf(request):
      company = request.user.company
      form = CompanyForms(instance=company)
      if request.method == 'POST':
       form = CompanyForms(request.POST , request.FILES ,instance=company)
       if form.is_valid():
           form.save()
           return redirect('companyprofile')
      context = {'form':form}

      return render(request,"RMS/EditCompanyProf.html" ,context)


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})

def Editprof(request):
     applicant = request.user.applicant
     form = ApplicantForms(instance=applicant)
     if request.method == 'POST':
       form = ApplicantForms(request.POST , request.FILES ,instance=applicant)
       if form.is_valid():
           form.save()
           return redirect('userprofile')

     context = {'form':form}
     return render(request,"RMS/Editprof.html" ,context)


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def Editcvinfo(request):
     applicant = request.user.applicant
     form = ApplicantinfoForms(instance=applicant)
     if request.method == 'POST':
       form = ApplicantinfoForms(request.POST , request.FILES ,instance=applicant)
       if form.is_valid():
           form.save()
           return redirect('usercv')
     context = {'form':form} 
     return render(request,"RMS/Editcvinfo.html",context)

@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def edituserbio(request):
     applicant = request.user.applicant
     form = ApplicantbioForms(instance=applicant)
     if request.method == 'POST':
       form = ApplicantbioForms(request.POST , request.FILES ,instance=applicant)
       if form.is_valid():
           form.save()
           return redirect('usercv')
     context = {'form':form}
     return render(request,"RMS/edituserbio.html",context)




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def uservolant(request):
     volant = request.user.applicant
     form = ApplicantvolForms(instance=volant)
     if request.method == 'POST':
       form = ApplicantvolForms(request.POST , request.FILES ,instance=volant)
       if form.is_valid():
           form.save()
           return redirect('usercv')
     context = {'form':form}
     return render(request,"RMS/uservolant.html",context)





@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def editusercontact(request):
     applicant = request.user.applicant
     form = ApplicantcontactForms(instance=applicant)
     if request.method == 'POST':
       form = ApplicantcontactForms(request.POST , request.FILES ,instance=applicant)
       if form.is_valid():
           form.save()
           return redirect('usercv')
     context = {'form':form}
     return render(request,"RMS/editusercontact.html",context)




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})

def EditJobReq(request, job_id):
    jobs = get_object_or_404(job, id=job_id)
    form = JobForm(instance=jobs)
    if request.method == 'POST':
         form = JobForm(request.POST , request.FILES ,instance=jobs)
         if form.is_valid():
           form.save()
           return redirect('companyprofile')
         else:
            print(form.errors)

 
    return render(request, "RMS/EditJobReq.html", {'job': job, 'form': form})





@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def Editsection(request, sec_id):
    sections = get_object_or_404(OtherSection, id=sec_id)
    form = OtherSectionForm(instance=sections)
    if request.method == 'POST':
         form = OtherSectionForm(request.POST , request.FILES ,instance=sections)
         if form.is_valid():
           form.save()
           return redirect('usersections')
         else:
            print(form.errors)

 
    return render(request, "RMS/Editsection.html", {'sections': sections, 'form': form})




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def Editeducation(request, edu_id):
    eduacion = get_object_or_404(education, id=edu_id)
    form = educationForm(instance=eduacion)
    if request.method == 'POST':
         form = educationForm(request.POST , request.FILES ,instance=eduacion)
         if form.is_valid():
           form.save()
           return redirect('usereducation')
         else:
            print(form.errors)

   
    return render(request, "RMS/Editeducation.html", {'eduacion': eduacion, 'form': form})



@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def Editedexperience(request, exp_id):
    exp = get_object_or_404(workexperience, id=exp_id)
    form = workexperienceForm(instance=exp)
    if request.method == 'POST':
         form = workexperienceForm(request.POST , request.FILES ,instance=exp)
         if form.is_valid():
           form.save()
           return redirect('userexperience')
         else:
            print(form.errors)

   
    return render(request, "RMS/Editedexperience.html", {'exp': exp, 'form': form})




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def Editcertificate(request, cer_id):
    cer = get_object_or_404(certificate, id=cer_id)
    form = certificateForm(instance=cer)
    if request.method == 'POST':
         form = certificateForm(request.POST , request.FILES ,instance=cer)
         if form.is_valid():
           form.save()
           return redirect('usercertificates')
         else:
            print(form.errors)

   
    return render(request, "RMS/Editcertificate.html", {'exp': cer, 'form': form})




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def Editproject(request, project_id):
    projects = get_object_or_404(project, id=project_id)
    form = projectForm(instance=projects)
    if request.method == 'POST':
         form = projectForm(request.POST , request.FILES ,instance=projects)
         if form.is_valid():
           form.save()
           return redirect('userprojects')
         else:
            print(form.errors)

    return render(request, "RMS/Editproject.html", {'projects': projects, 'form': form})






@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def EditSkill(request, skil_id):
    skil = get_object_or_404(skils, id=skil_id)
    form = skilsForm(instance=skil)
    if request.method == 'POST':
         form = skilsForm(request.POST , request.FILES ,instance=skil)
         if form.is_valid():
           form.save()
           return redirect('userskills')
         else:
            print(form.errors)


    return render(request, "RMS/EditSkill.html", {'skil': skil, 'form': form})


@login_required(login_url= 'login')
def userskills(request):
     return render(request,"RMS/userskills.html")


@login_required(login_url= 'login')
def similarity_form(request):
     return render(request,"RMS/similarity.html")

@login_required(login_url= 'login')
def similarity_result(request):
     return render(request,"RMS/similarity.html")


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})
def deletejob(request, job_id):
    
    jobs = get_object_or_404(job, pk=job_id)  
   
  
    if request.method == 'POST':
        
            jobs.delete()
       
            return redirect('JobsHistory')
 
    return render(request, 'RMS/companyprofile.html', {'Job': jobs })



@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def deleteskill(request, skill_id):
    
    skill = get_object_or_404(skils, pk=skill_id)  
   
   
    if request.method == 'POST':
        
            skill.delete()
       
            return redirect('usercv')
    
    return render(request, 'RMS/userskills.html', {'skill': skill })



@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def deleteeducation(request, edu_id):
    
    edu = get_object_or_404(education, pk=edu_id) 
    
   

    if request.method == 'POST':
        
            edu.delete()
        
            return redirect('usercv')
  
    return render(request, 'RMS/usereducation.html', {'edu': edu })


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def deletesection(request, sec_id):
    
    sec = get_object_or_404(OtherSection, pk=sec_id)  
   
    
    if request.method == 'POST':
        
            sec.delete()
       
            return redirect('usercv')
   
    return render(request, 'RMS/usersections.html', {'edu': sec })




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def deleteexpeience(request, exp_id):
    
    exp = get_object_or_404(workexperience, pk=exp_id)  
   

    if request.method == 'POST':
        
            exp.delete()
       
            return redirect('usercv')
    
    return render(request, 'RMS/usereducation.html', {'edu': exp })



@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def deleteproject(request, Project_id):
    
    Project = get_object_or_404(project, pk=Project_id)  # Fix: Use 'Job' instead of 'job'
   

    if request.method == 'POST':
        
            Project.delete()
        
            return redirect('usercv')
    
    return render(request, 'RMS/userprojects.html', {'Project': Project })


@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','applicant'})
def deletecertificate(request,certificate_id):
    
    certificates = get_object_or_404(certificate, pk=certificate_id)  # Fix: Use 'Job' instead of 'job'
   
  
    if request.method == 'POST':
        
            certificates.delete()
        
            return redirect('usercv')
   
    return render(request, 'RMS/userprojects.html', {'Project': certificates })



@login_required(login_url= 'login')
def companydepartment(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    companies_in_department = company.objects.filter(department=department)
    return render(request, "RMS/companydepartment.html", {'companies': companies_in_department })



@login_required(login_url= 'login')
def companyPro(request, company_id, job_id=None):
    company_instance = get_object_or_404(company, id=company_id)
    
    if job_id is not None:
        job_instance = get_object_or_404(job, id=job_id)
        
    else:
        job_instance = None

        company_jobs = company_instance.job_set.all()

    # Fetch all jobs from all companies
    #jobs_id = job.objects.id

    return render(request, "RMS/companyPro.html", {'company': company_instance, 'job': job_instance ,'company_jobs': company_jobs })






@login_required(login_url='login')
def applicantprof(request, applicant_id, educations_id=None):
   
    applicant_instance = get_object_or_404(Applicant, id=applicant_id)

    if educations_id is not None:
     
        education_instance = get_object_or_404(education, id=educations_id)
        applicant_educations = applicant_instance.education_set.all()
    else:
       
        education_instance = None
        applicant_educations = applicant_instance.education_set.all()

    return render(request, "RMS/applicantprof.html", {'applicant_instance': applicant_instance,
                                                       'applicant_educations': applicant_educations,
                                                       'education_instance': education_instance})
    




@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin'})
def dashboard(request):
    number_of_companies = company.objects.count()
    number_of_applicants = Applicant.objects.count()
    number_of_jobs=job.objects.count()

    context = {
        'number_of_companies': number_of_companies,
        'number_of_applicants': number_of_applicants,
        'number_of_jobs':number_of_jobs,
    }

    return render(request, 'RMS/dashboard.html', context)





@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def departmentForAdmin(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, "RMS/departmentForAdmin.html", context)



@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def delete_department(request):
    if request.method == 'POST':
        if 'delete_department_name' in request.POST:
            delete_department_name = request.POST.get('delete_department_name')
            try:
                department_to_delete = Department.objects.get(name=delete_department_name)
                department_to_delete.delete()
                messages.success(request, f'Department "{department_to_delete.name}" deleted successfully.')
            except Department.DoesNotExist:
                messages.error(request, 'Department not found.')

    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, "RMS/departmentForAdmin.html", context)


@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def add_department(request):
    if request.method == 'POST':
        form = AddDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully.')
            return redirect('departmentForAdmin')  
        else:
            messages.error(request, 'Error in the form submission. Please check the details.')
    else:
        form = AddDepartmentForm()

    return render(request, 'RMS/addDepartmentForAdmin.html', {'form': form})





@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def addApplicantForAdmin(request):
    form = CreateNewUser()
    if request.method == 'POST' :   
         form = CreateNewUser(request.POST)
         if form.is_valid():
                         user = form.save()
                         username = form.cleaned_data.get('username')
                         registration_type = request.POST.get('registration_type', '')
                         if registration_type == 'applicant':
                              group = Group.objects.get(name="applicant")
                              
                         elif registration_type == 'company':
                              group = Group.objects.get(name="company")
  
                         else:
                              group = None
                       
                         if group:
     
                            user.groups.add(group)
                            messages.success(request , username + 'Create Successfully !')
                            return redirect('applicantsForAdmin')
    context = {'form' : form }
    return render(request, "RMS/addApplicantForAdmin.html",context )



 
@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def addDepartmentForAdmin(request):
    return render(request, "RMS/addDepartmentForAdmin.html")


 
@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def companiesForAdmin(request):
    companies = company.objects.all()  
    
    context = {'companies': companies}
    return render(request, "RMS/companiesForAdmin.html", context)



@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def applicantsForAdmin(request):
    applicants = Applicant.objects.all()  
    context = {'applicants': applicants}
    return render(request, "RMS/applicantsForAdmin.html", context)



@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def deleteapplicant(request):
    if request.method == 'POST':
        
        if 'delete_applicant_email' in request.POST:
            applicant_email_to_delete = request.POST.get('delete_applicant_email')
            try:
                applicant_to_delete = Applicant.objects.get(email=applicant_email_to_delete)
                applicant_to_delete.delete()
                messages.success(request, f'Applicant "{applicant_to_delete.name}" deleted successfully.')
            except Applicant.DoesNotExist:
                messages.error(request, 'Applicant not found.')

    applicants = Applicant.objects.all()
    context = {'applicants': applicants}
    return render(request, "RMS/applicantsForAdmin.html", context)


@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def delete_company(request):
    if request.method == 'POST':
        
        if 'delete_company_email' in request.POST:
            company_email_to_delete = request.POST.get('delete_company_email')
            try:
                company_to_delete = company.objects.get(email=company_email_to_delete)
                company_to_delete.delete()
                messages.success(request, f'Company "{company_to_delete.name}" deleted successfully.')
            except company.DoesNotExist:
                messages.error(request, 'Company not found.')

   
    return redirect('companiesForAdmin')
@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})

def jobForAdmin(request):
    jobs = job.objects.all()  # Retrieve all companies from the database
    return render(request, "RMS/jobForAdmin.html", {'jobs': jobs})  
@login_required(login_url= 'login')
@allowedUsers(allowedGroups={'admin','company'})


def deletejobdash(request, job_id):
    
    jobs = get_object_or_404(job, pk=job_id)  # Fix: Use 'Job' instead of 'job'
   
    # Check if the request method is POST
    if request.method == 'POST':
        
            jobs.delete()
        # Redirect to the appropriate page after deletion
            return redirect('jobForAdmin')
    # If the request method is not POST, render a confirmation page
    return render(request, 'RMS/jobForAdmin.html', {'Job': jobs })

def editjobreqdash(request, job_id):
    jobs = get_object_or_404(job, id=job_id)
    form = CreateNewjobAdmin(instance=jobs)
    if request.method == 'POST':
         form = CreateNewjobAdmin(request.POST , request.FILES ,instance=jobs)
         if form.is_valid():
           form.save()
           return redirect('jobForAdmin')
         else:
            print(form.errors)

    return render(request, "RMS/editjobreqdash.html", {'job': job, 'form': form})






@login_required(login_url='login')
@allowedUsers(allowedGroups={'admin'})
def JobRequirementsdash(request):
     form = CreateNewjobAdmin() 
     if request.method == 'POST':
          form = CreateNewjobAdmin(request.POST)
          if form.is_valid():
               job = form.save(commit=False)
               job.save()
               if hasattr(request.user, 'company'):  # Check if user has company
                    company = request.user.company
                    job.companies.add(company)
               else:
                    # Handle the case when the user doesn't have a company
                    messages.error(request, 'User does not have a company.')

               return redirect('jobForAdmin')

     context = {'form': form}
     return render(request, "RMS/JobRequirementsdash.html", context)

@login_required(login_url='login')
def education_data(request):
    # Get the currently logged-in user
    user = request.user
    
    # Retrieve the applicant linked with the logged-in user
    applicant = user.applicant
    
    # Retrieve the education data for the applicant
    education_data = applicant.education_set.all()
    
    # Convert education data to a string
    education_string = ""
    for education in education_data:
        education_string += f"Degree: {education.degree}, Institution: {education.title}, Start Date: {education.fromto}, End Date: {education.major}\n"
    
    # Prepare the context to pass to the template
    context = {'education_string': education_string}
    
    # Render the template with the education data
    return render(request, 'RMS/test.html',context)

model = SentenceTransformer('nickmuchi/setfit-finetuned-financial-text-classification')

@login_required(login_url='welcome')
def home(request):
    companies = company.objects.all()
    latest_job = job.objects.latest('created_at')  
    
    companyfilter = companyFilter(request.GET, queryset=companies)
    companies = companyfilter.qs

    for Company in companies:
        Company.jobs = Company.job_set.all().order_by('-created_at')  # Reverse order of jobs

    return render(request, "RMS/home.html", {'companies': companies, 'latest_job': latest_job, 'companyfilter':companyFilter})


@csrf_exempt
@login_required(login_url='login')
def similarity_form(request):
    return render(request, 'RMS/similarity_form.html')


def calculate_sentence_similarity(model, compared_sentence, group_of_sentences):
    # Encode the compared sentence
    compared_sentence_embedding = model.encode([compared_sentence])[0]

    # Calculate cosine similarity for each sentence in the group
    similarities = []
    for sentence in group_of_sentences:
        sentence_embedding = model.encode([sentence])[0]

        # Normalize the vectors
        compared_sentence_embedding_normalized = compared_sentence_embedding / np.linalg.norm(compared_sentence_embedding)
        sentence_embedding_normalized = sentence_embedding / np.linalg.norm(sentence_embedding)

        # Calculate cosine similarity
        similarity = np.dot(compared_sentence_embedding_normalized, sentence_embedding_normalized)
        similarities.append((sentence, similarity))

    return similarities

# Load the Sentence-Transformers model
model = SentenceTransformer('nickmuchi/setfit-finetuned-financial-text-classification')



def calculate_similarity(model, compared_sentence, group_of_sentences):
    # Calculate cosine similarity for each sentence in the group
    similarities = []
    compared_sentence_embedding = model.encode([compared_sentence])[0]
    for sentence in group_of_sentences:
        sentence_embedding = model.encode([sentence])[0]
        
        # Normalize the vectors
        compared_sentence_embedding_normalized = compared_sentence_embedding / np.linalg.norm(compared_sentence_embedding)
        sentence_embedding_normalized = sentence_embedding / np.linalg.norm(sentence_embedding)
        
        # Calculate cosine similarity
        similarity = np.dot(compared_sentence_embedding_normalized, sentence_embedding_normalized)
        similarities.append((sentence, similarity))
    return similarities

similarity = []
def cv_evaluation(request):
    

    if request.method == 'POST':
        model = SentenceTransformer('nickmuchi/setfit-finetuned-financial-text-classification')

        # Calculate similarity for education
        

        # Calculate similarity for work experiences
        jobs_data  = job.objects.values_list('workexperience', flat=True)
        jobs_string = "\n".join(str(workexperience) for workexperience in jobs_data)
        compared_sentence = jobs_string
        
        work_experience_data = request.user.applicant.workexperience_set.all()
        
        Workexperience_string = ""
        for work_experience in work_experience_data:
            Workexperience_string = "\n".join(f"companyworked: {work_experience.companyworked}, jobworked: {work_experience.jobworked}, describtion: {work_experience.describtion}" for work_experience in work_experience_data)

        group_of_sentences = Workexperience_string.split('\n')
        similarity.extend(calculate_sentence_similarity(model, compared_sentence, group_of_sentences))

        # Calculate similarity for skills
        jobs_data  = job.objects.values_list('technicalskills', flat=True)
        jobs_string = "\n".join(str(skils) for skills in jobs_data)
        compared_sentence = jobs_string
        education_data = request.user.applicant.skils_set.all()
        education_string = "\n".join(f"Skill Name: {education.name}" for education in education_data)
        group_of_sentences = education_string.split('\n')
        similarity.extend(calculate_sentence_similarity(model, compared_sentence, group_of_sentences))

        # Calculate similarity for certificates
        jobs_data  = job.objects.values_list('achievements', flat=True)
        jobs_string = "\n".join(str(certificate) for certificate in jobs_data)
        compared_sentence = jobs_string
        certificate_data = request.user.applicant.certificate_set.all()
        certificatestring = "\n".join(f"Place: {certificate.place},Major: {certificate.major},About: {certificate.about}" for certificate in certificate_data)
        group_of_sentences = certificatestring.split('\n')
        similarity.extend(calculate_sentence_similarity(model, compared_sentence, group_of_sentences))

    return render(request, 'RMS/similarity_form.html', {'similarities':similarity})


from datetime import datetime





@login_required(login_url='login')
def apply_job(request, job_id):
    similarity = []  # Initialize an empty list
    job_instance = None  # Initialize job_instance variable outside the if block

    try:
        job_instance = job.objects.get(id=job_id)
    except job.DoesNotExist:
        # Handle the case where the job ID doesn't exist
        pass
    
    
     # Check if the applicant has already applied for this job
    if jobstatus.objects.filter(job_id=job_id, applicant=request.user.applicant).exists():
        context = {
            'already_applied': True,
            'job_id': job_id
        }
        return render(request, 'RMS/already_applied.html', context)
    
    if job_instance:
        number_of_applicants = job_instance.number_of_positions
        workexperience = job_instance.workexperience
        education_instance=job_instance.education
        education="\n".join(f"Degree: {education.degree}, title: {education.title},  Date: {education.fromto}, major: {education.major}" for education in request.user.applicant.education_set.all())
        work_experience = "\n".join(f"companyworked: {work_experience.companyworked}, jobworked: {work_experience.jobworked}, describtion: {work_experience.describtion}" for work_experience in request.user.applicant.workexperience_set.all())
        
        achievements = "\n".join(f"Place: {certificate.place}, Major: {certificate.major}, About: {certificate.about}" for certificate in request.user.applicant.certificate_set.all())


        technical_skills = job_instance.technicalskills
        applicant_skills = "\n".join(f"Skill Name: {skils.name}" for skils in request.user.applicant.skils_set.all())

        # Convert both strings to uppercase
        technical_skills = technical_skills.upper()
        applicant_skills = applicant_skills.upper()

        # Split the first string into words
        words1 = technical_skills.split()

        # Split the second string into words
        words2 = applicant_skills.split()

        # Find common words
        common_words = [word for word in words1 if word in words2]

        # Join common words into a string
       # result = ", ".join(common_words) if common_words else ""
        #if result!="":
        # result = result.split('/n')

         #similarity.extend(calculate_sentence_similarity(model, technical_skills, result))
        #common_words = [word for word in words1 if word in words2]

# Calculate the ratio of common words to the total number of words in words2
        if words1:
           common_ratio = len(common_words) / len(words1)
        else:
           common_ratio = 0
        
        print("Common Ratio:", common_ratio)


        # Calculate similarity for work experiences
        model = SentenceTransformer('nickmuchi/setfit-finetuned-financial-text-classification')
        compared_sentence = work_experience
        group_of_sentences = workexperience.split('\n')

        similarity.extend(calculate_sentence_similarity(model, compared_sentence, group_of_sentences))


        # Calculate similarity for certificates
        compared_sentence = achievements
        group_of_sentences = job_instance.achievements.split('\n')
        similarity.extend(calculate_sentence_similarity(model, compared_sentence, group_of_sentences))


        # Calculate similarity for education
       
        compared_sentence = education
        group_of_sentences = education_instance.split('\n')

        similarity.extend(calculate_sentence_similarity(model, compared_sentence, group_of_sentences))


        job_sections = {
            'workexperience': job_instance.workexperience,
            'education': job_instance.education,
            'technicalskills': job_instance.technicalskills,
            'achievements': job_instance.achievements
        }
        
        additional_sections = request.user.applicant.othersection_set.all()
        # Calculate similarity between each job section and each additional applicant section
        for section in additional_sections:
            applicant_section_content = "\n".join(f"{section.name}: {content}" for content in request.user.applicant.othersection_set.filter(name=section.name))

            max_similarity = 0
            best_match = None

            for job_section_name, job_section_content in job_sections.items():
                compared_sentence = job_section_content
                group_of_sentences = applicant_section_content.split('\n')
                section_similarities = calculate_similarity(model, compared_sentence, group_of_sentences)

                # Find the highest similarity in this section
                for sentence, sim in section_similarities:
                    if sim > max_similarity:
                        max_similarity = sim
                        best_match = (sentence, sim)

            # Append the best match similarity for this section
            if best_match:
                similarity.append(best_match) 
# Calculate the average similarity
        if similarity:
            total_similarity = sum(sim for _, sim in similarity)
            average_similarity = total_similarity / len(similarity)

             # Get the first associated company
            company = job_instance.companies.first()

            # Save to JobStatus table
            jobstate= jobstatus.objects.create(
                company=company,
                job=job_instance,
                applicant=request.user.applicant,
                percentage=average_similarity
            )

            top_applicants = jobstatus.objects.filter(job=job_instance).order_by('-percentage')[:number_of_applicants]
            
            # Check if the applicant is one of the top applicants
            if jobstate in top_applicants:
                jobstate.is_top_applicant = True
                jobstate.save()
        
        context = {'already_applied': False}
        return render(request, 'RMS/already_applied.html', context)         



@login_required(login_url='login')
def check_apply(request, job_id):
    # Check if the applicant has already applied for this job
    already_applied = jobstatus.objects.filter(job_id=job_id, applicant=request.user.applicant).exists()
    return JsonResponse({'alreadyApplied': already_applied})

