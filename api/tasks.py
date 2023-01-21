from celery.utils.log import get_task_logger
from celery import shared_task
from django.db import transaction
from .emails import *

logger = get_task_logger(__name__)


@shared_task
def send_inquiries_email_task(fullname,email,mobile,message):
    with transaction.atomic():
        logger.info('Successful')
        return send_inquiries_email(fullname,email,mobile,message)


@shared_task
def send_virtualclass_email_task(course,full_name,email,mobile,remarks):
    with transaction.atomic():
        logger.info('Successful')
        return send_virtualclass_email(course,full_name,email,mobile,remarks)        


@shared_task
def send_kids_coding_email_task(age_bracket,full_name,email,mobile,remarks):
    with transaction.atomic():
        logger.info('Successful')
        return send_kids_coding_email(age_bracket,full_name,email,mobile,remarks)                


@shared_task
def send_short_quizze_email_task(fullname,email,mobile,tartiary_education,tartiary_studied,secondary_sch,secondary_studied,tech_interest,more_about_you):
    with transaction.atomic():
        logger.info('Successful')
        return send_short_quizze_email(fullname,email,mobile,tartiary_education,tartiary_studied,secondary_sch,secondary_studied,tech_interest,more_about_you)           


@shared_task
def send_interested_email_task(course_id,full_name,email,mobile):
    with transaction.atomic():
        logger.info('Successful')
        return send_interested_email(course_id,full_name,email,mobile)
