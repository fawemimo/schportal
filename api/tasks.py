from celery.utils.log import get_task_logger
from celery import shared_task
from django.db import transaction
from .emails import *

logger = get_task_logger(__name__)


@shared_task()
def send_inquiries_email_task(fullname,email,mobile,message):
    logger.info('Successful')
    return send_inquiries_email(fullname,email,mobile,message)