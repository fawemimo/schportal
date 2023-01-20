from templated_mail.mail import BaseEmailMessage
from django.conf import settings


def send_inquiries_email(fullname,email,mobile,message):
    try:
        message = BaseEmailMessage(template_name='emails/iniquiries.html',
        context = {
            'fullname' : fullname,
            'email' :email,
            'mobile' : mobile,
            'message': message
        }
        
        )
        message.send([email,settings.EMAIL_HOST_USER])
    except Exception as e:
            print(e)