from celery import shared_task 
from django.core.mail import send_mail
from time import sleep


@shared_task
def send_email_task():
    send_mail(
        'Celery Task Worked!',
        'This is proof the task worked with CELERY using delay func!',
        'mostafa9102vahdani@outlook.com',
        [
            'vahdanim77@gmail.com',
        ])

    return None
