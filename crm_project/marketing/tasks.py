from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from celery import shared_task
from marketing import my_statics
import smtplib


@shared_task
def send_email_task(
    user_pk, from_email, email_to, subject, 
    normal_message_content, html_message_content):

    user_obj = get_user_model().objects.get(pk=user_pk)
    try:
        send_mail(
            subject=subject,
            message=normal_message_content,
            html_message=html_message_content,
            from_email=from_email,
            recipient_list=[
                email_to,
            ],
            fail_silently=False)

        my_statics.save_email_status_delivery(
            receiver_email=email_to, 
            sender=user_obj, 
            was_successfull=True)

        return True
    except smtplib.SMTPException as exc:
        my_statics.save_email_status_delivery(
            receiver_email=email_to, 
            sender=user_obj, 
            was_successfull=False)

        return False
