from django.contrib import admin

# Register your models here.
from .models import company
admin.site.register(company)
from .models import job
admin.site.register(job)
from .models import Applicant
admin.site.register(Applicant)
from .models import skils
admin.site.register(skils)
from .models import education
admin.site.register(education)
from .models import Department
admin.site.register(Department)
from .models import OtherSection
admin.site.register(OtherSection)

from .models import project
admin.site.register(project)
from .models import workexperience
admin.site.register(workexperience)
from .models import certificate
admin.site.register(certificate)

from .models import jobstatus
admin.site.register(jobstatus)


from .models import Notification
admin.site.register(Notification)