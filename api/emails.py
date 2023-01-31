from templated_mail.mail import BaseEmailMessage
from django.conf import settings
from datetime import date
from api.models import Course


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
    course = Course.objects.get(id=course_id)
    try:
        message = BaseEmailMessage(template_name='emails/interested_emails.html',
        context = {
            'course':course.title.upper(),
            'startdate':course.schedule_set.values('startdate'),
            'course_id':course_id,
            'full_name':full_name,
            'email':email,
            'mobile':mobile

        }
        
        )
        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        print(e)


def send_virtualclass_email(course_id,full_name,email,mobile,remarks):
    course = Course.objects.get(id=course_id)
    try:
            message = BaseEmailMessage(template_name='emails/virtual_class.html',
            context = {
                'course': course,
                'course_id':course_id,
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
    today_date = date.today()
    try:
        message = BaseEmailMessage(template_name='emails/career_choice.html',
        context = {
            'today_date':today_date,
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
        message.send([email,settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)




