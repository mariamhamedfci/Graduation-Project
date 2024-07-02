from django.shortcuts import redirect 
from django.contrib.auth.models import User




def allowedUsers(allowedGroups={}):
    def decorators(view_fun):
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
               group= request.user.groups.all()[0].name
            if group in allowedGroups:
                    return view_fun(request,*args,**kwargs)
            else :
                    if request.user.groups.filter(name='company').exists():
                       return redirect('companyprofile')  # Replace 'company_home' with the desired company home URL
                    elif request.user.groups.filter(name='applicant').exists():
                       return redirect('userprofile')  # Replace 'applicant_home' with the desired applicant home URL
                    else:
                          return redirect('/')

        return wrapper_func
    return decorators