from http.client import HTTPResponse
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.urls import path



from . import views

urlpatterns = [
    
               path('',views.home, name="home" ),
               
               path('login',views.userLogin, name="login" ),
               
               path('logout',views.userLogout, name="logout" ),

               path('register',views.register, name="register" ),

               path('userprofile',views.userprofile, name="userprofile" ),
               
               path('companyprofile',views.companyprofile, name="companyprofile" ),
               
               path('department',views.department, name="department" ),

             
               path('noti',views.noti, name="noti" ),

               
               path('usercv',views.usercv, name="usercv" ),

                 
              path('companies',views.companies, name="companies" ),

              path('Editprof',views.Editprof, name="Editprof" ),

              path('EditJobReq/<int:job_id>/', views.EditJobReq, name='edit_job_req'),

              
              path('Editsection/<int:sec_id>/', views.Editsection, name='Editsection'),

              path('deletejob/<int:job_id>/', views.deletejob, name='deletejob'),

              path('deleteskill/<int:skill_id>/', views.deleteskill, name='deleteskill'),


              
              path('EditSkill/<int:skil_id>/', views.EditSkill, name='EditSkill'),


             path('deleteeducation/<int:edu_id>/', views.deleteeducation, name='deleteeducation'),

             
             path('Editeducation/<int:edu_id>/', views.Editeducation, name='Editeducation'),

              path('deleteexpeience/<int:exp_id>/', views.deleteexpeience, name='deleteexpeience'),


              path('Editedexperience/<int:exp_id>/', views.Editedexperience, name='Editedexperience'),


              
              path('deletesection/<int:sec_id>/', views.deletesection, name='deletesection'),

              
              path('deleteproject/<int:Project_id>/', views.deleteproject, name='deleteproject'),


              path('Editproject/<int:project_id>/', views.Editproject, name='Editproject'),

              
              path('deletecertificate/<int:certificate_id>/', views.deletecertificate, name='deletecertificate'),


              path('Editcertificate/<int:cer_id>/', views.Editcertificate, name='Editcertificate'),
              
               path('changepassword',views.changepassword, name="changepassword" ),

               path('Editcvinfo',views.Editcvinfo, name="Editcvinfo" ),

               path('usereducation',views.usereducation, name="usereducation" ),

                path('addusereducation',views.addusereducation, name="addusereducation" ),

                path('userexperience',views.userexperience, name="userexperience" ),

                path('adduserexperience',views.adduserexperience, name="adduserexperience" ),

                path('usercertificates',views.usercertificates, name="usercertificates" ),

                path('addusercertificates',views.addusercertificates, name="addusercertificates" ),

                path('userprojects',views.userprojects, name="userprojects" ),

                path('addproject',views.addproject, name="addproject" ),

                path('edituserbio',views.edituserbio, name="edituserbio" ),

                path('uservolant',views.uservolant, name="uservolant" ),

                path('editusercontact',views.editusercontact, name="editusercontact" ),

                path('userskills',views.userskills, name="userskills" ),

               path('addskills',views.addskills, name="addskills" ),

               
               path('addsection',views.addsection, name="addsection" ),
                
               path('JobRequirements/',views.JobRequirements, name="JobRequirements" ),

               path('NewJob/',views.NewJob, name="NewJob" ),

               path('Status/<int:job_id>/', views.Status, name='Status'),

               path('jobsStatus/', views.jobsStatus, name='jobsStatus'),

               path('JobsHistory/',views.JobsHistory, name="JobsHistory" ),
               

               path('EditCompanyProf',views.EditCompanyProf, name="EditCompanyProf" ),

               
               path('profileinfo',views.profileinfo, name="profileinfo" ),


               path('userinfo',views.userinfo, name="userinfo" ),

                path('welcome',views.welcome, name="welcome" ),
                path('similarity_form',views.similarity_form, name="similarity_form" ),
                path('similarity_result',views.similarity_result, name="similarity_result" ),

                

                path('companydepartment/<int:department_id>/', views.companydepartment, name='companydepartment'),

                path('applicantsdepartment', views.applicantsdepartment, name='applicantsdepartment'),

                path('companyPro/<int:company_id>/',views.companyPro, name="companyPro" ),

                path('companyPro/<int:company_id>/<int:job_id>/', views.companyPro, name='companyPro'),

                path('applicantprof/<int:applicant_id>/',views.applicantprof, name='applicantprof' ),
                
                path('applicantprof/<int:applicant_id>/<int:educations_id>/',views.applicantprof, name='applicantprof' ),

                
                path('usersections', views.usersections, name='usersections'),


                

               path('dashboard',views.dashboard, name="dashboard" ),

                path('deleteapplicant/', views.deleteapplicant, name='deleteapplicant'),
                path('delete_company/', views.delete_company, name='delete_company'),
                 path('delete_department/',views.delete_department, name='delete_department'),
                 path('addApplicantForAdmin/', views.addApplicantForAdmin, name='addApplicantForAdmin'),
                 path('addDepartmentForAdmin/', views.addDepartmentForAdmin, name='addDepartmentForAdmin'),
                   path('add_department/', views.add_department, name='add_department'),
                   path('companiesForAdmin/',views.companiesForAdmin, name='companiesForAdmin'),
                   path('applicantsForAdmin/',views.applicantsForAdmin, name='applicantsForAdmin'),
                   path('departmentForAdmin/',views.departmentForAdmin, name='departmentForAdmin'),
                   path('jobForAdmin/',views.jobForAdmin, name='jobForAdmin'),
                    path('editjobreqdash/<int:job_id>/',views.editjobreqdash, name='editjobreqdash'),
                     path('deletejobdash/<int:job_id>/', views.deletejobdash, name='deletejobdash'),
                     path('JobRequirementsdash/',views.JobRequirementsdash, name="JobRequirementsdash"),
                     path('cv_evaluation/', views.cv_evaluation, name='cv_evaluation'),                 
                     path('test/',views.education_data, name="test"),
                      path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),

                     path('home/', views.home, name='home'),

         path('company/<int:company_id>/follow_unfollow/', views.follow_unfollow_company, name='follow_unfollow_company'),
           path('followers/', views.followers, name='followers'),

] 


#urlpatterns += static[settings.MEDIA_URL , document_root =settings.MEDIA_ROOT]