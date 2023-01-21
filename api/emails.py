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


def send_interested_email(course_id,full_name,email,mobile):
    try:
        message = BaseEmailMessage(template_name='emails/interested_emails.html',
        context = {
            'course_id':course_id,
            'full_name':full_name,
            'email':email,
            'mobile':mobile

        }
        
        )
        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        print(e)


def send_virtualclass_email(course,full_name,email,mobile,remarks):
    try:
            message = BaseEmailMessage(template_name='emails/virtual_class.html',
            context = {
                'course':course,
                'full_name':full_name,
                'email':email,
                'mobile':mobile,
                'remarks': remarks
            }
            
            )
            message.send([email, settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)


def send_kids_coding_email(age_bracket,full_name,email,mobile,remarks):
    try:
        message = BaseEmailMessage(template_name='emails/kidscoding.html',
            context = {
            'age_bracket':age_bracket,
            'full_name':full_name,
            'email':email,
            'mobile':mobile,
            'remarks': remarks
        }
        
        )
        message.send([email, settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)


def send_short_quizze_email(fullname,email,mobile,tartiary_education,tartiary_studied,secondary_sch,secondary_studied,tech_interest,more_about_you):
    try:
        message = BaseEmailMessage(template_name='emails/short_quizzes.html',
        context = {
            'fullname' : fullname,
            'email' :email,
            'mobile' : mobile,
            'tartiary_education': tartiary_education,
            'tartiary_studied' : tartiary_studied,
            'secondary_sch' : secondary_sch,
            'secondary_studied' : secondary_studied,
            'tech_interest' : tech_interest,
            'more_about_you': more_about_you, 
        }
        
        )
        message.send([settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)




