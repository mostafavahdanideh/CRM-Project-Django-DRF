from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from celery import shared_task
from django.shortcuts import get_object_or_404
from django.conf import settings
from marketing import models as marketing_models
from django.template import loader


@shared_task
def send_email_task(quote_pk, user_pk):

    quote_obj = get_object_or_404(klass=marketing_models.Quote, pk=quote_pk)
    user_obj = get_object_or_404(klass=get_user_model(), pk=user_pk)
    email_from = settings.EMAIL_HOST_USER
    email_to = quote_obj.owner.owner_email
    subject = 'پیش فاکتور'
    normal_message_content = "پیش فاکتور شما ثبت شد"
    
    html_message_content = loader.render_to_string(
            template_name="quote_email_template.html",
            context={
                'quote_pk': quote_pk,
                'message': "پیش فاکتور شما ثبت شد", 
            })

    try:

        send_mail(
            subject=subject,
            message=normal_message_content,
            html_message=html_message_content,
            from_email=email_from,
            recipient_list=[
                email_to,
            ],
            fail_silently=False)

        was_successfull=True

    except Exception as error:
        print(error)
        was_successfull=False

    marketing_models.QuoteEmailHistory.objects.create(
        receiver_email_address=email_to,
        was_successfull=was_successfull,
        user_sender=user_obj
    ).save()

    return 'Done'
