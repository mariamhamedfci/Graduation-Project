from .models import Notification

def send_notification(user_from, user_to, company, action, job=None):
    if action == 'follow':
        message_to_company = f'{user_from.username} starts to follow your company'
        message_to_applicant = f'You start following {company.name}'
    elif action == 'unfollow':
        message_to_company = f'{user_from.username} unfollows your company'
        message_to_applicant = f'You unfollow {company.name}'
    elif action == 'new_job':
        message_to_followers = f'The company {company.name} you followed added a new job: {job.title}. Check it out!'
        # Create a notification for each follower
        Notification.objects.create(user=user_to, message=message_to_followers)
        return
    elif action == 'job_accepted':
        message_to_applicant = f'Congratulations! You have been accepted for the job: {job.title} at {company.name}.'
        Notification.objects.create(user=user_to, message=message_to_applicant)
        return

    # Create notifications for both company and applicant (for follow/unfollow actions)
    Notification.objects.create(user=user_to, message=message_to_company)
    Notification.objects.create(user=user_from, message=message_to_applicant)
