import time
from django.utils import timezone
import django
import os
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv.settings')
django.setup()

from RMS.models import job, jobstatus, Notification, Applicant  # Import related models as needed
from RMS.utils import send_notification

def hide_expired_jobs():
    now_utc = timezone.now()
    
    egypt_tz = pytz.timezone('Africa/Cairo')
    now_local = now_utc.astimezone(egypt_tz)
    
    current_date = now_local.date()
    current_time = now_local.time()
    print(f"Running job cleanup at {current_time} on {current_date} (Egypt local time)")

    jobs_to_hide = job.objects.filter(end_date__lte=current_date, deletion_time__lte=current_time, is_active=True)
    hidden_count = jobs_to_hide.count()
    
    if hidden_count > 0:
        print(f"Found {hidden_count} jobs to hide")
        for job_instance in jobs_to_hide:
            print(f"Hiding job: {job_instance.title} with end_date: {job_instance.end_date} and deletion_time: {job_instance.deletion_time}")
            job_instance.is_active = False
            job_instance.save()

            # Notify top applicants
            top_applicants = jobstatus.objects.filter(job=job_instance, percentage__gt=0)  # Filter top applicants based on your criteria
            for top_applicant in top_applicants:
                applicant_user = top_applicant.applicant.user
                company = top_applicant.company  # Assuming this is how you get the company related to jobstatus
                send_notification(None, applicant_user, company, 'job_accepted', job_instance)

        print(f"Hidden {hidden_count} expired jobs")
    else:
        print("No expired jobs to hide")

if __name__ == "__main__":
    while True:
        hide_expired_jobs()
        time.sleep(1)  # Run the cleanup every hour
