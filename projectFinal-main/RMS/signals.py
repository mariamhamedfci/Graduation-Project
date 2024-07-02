#from django.db.models.signals import post_save
#from django.contrib.auth.models import User ,Group
#from .models import *


#def company_create_profile(sender, instance,created ,**kwargs):
 #   if created:
         #registration_type = request.POST.get('registration_type', '')
         #if registration_type == 'company':
           
  #        group = Group.objects.get(name="company")
   #       instance.groups.add(group) 

    #      company.objects.create(
     #       user = instance,
      #      name= instance.username
       # )

   # print('company profile created! ') #  send Email to user
#post_save.connect(company_create_profile , sender=User)

