import django_filters

from .models import * 





class companyFilter(django_filters.FilterSet):
    class Meta:
        model = company
        fields = ['name'] 






class jobFilter(django_filters.FilterSet):
    class Meta:
        model = job
        fields = ['title']         




class applicantFilter(django_filters.FilterSet):
    class Meta:
        model = Applicant
        fields = ['name']                 