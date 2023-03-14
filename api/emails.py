from templated_mail.mail import BaseEmailMessage
from django.conf import settings
from datetime import date
from api.models import Course


def send_inquiries_email(fullname,email,mobile,message):
    try:
        message = BaseEmailMessage(template_name='api/email_response/iniquiries.html',
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
        message = BaseEmailMessage(template_name='api/email_response/interested_emails.html',
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


def send_virtualclass_email(course_id,full_name,email,mobile,remarks,country_of_residence):
    course = Course.objects.get(id=course_id)
    try:
            message = BaseEmailMessage(template_name='api/email_response/virtual_class.html',
            context = {
                'course': course.title,
                'course_id':course_id,
                'full_name':full_name,
                'email':email,
                'mobile':mobile,
                'remarks': remarks,
                'country_of_residence':country_of_residence
            }
            
            )
            message.send([email, settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)


def send_kids_coding_email(age_bracket,full_name,email,mobile,remarks):
    try:
        message = BaseEmailMessage(template_name='api/email_response/kidscoding.html',
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
        message = BaseEmailMessage(template_name='api/email_response/career_choice.html',
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


def send_financial_aid_email(aid_type,first_name,last_name,email,mobile):
    
    try:
        message = BaseEmailMessage(template_name='api/email_response/financial_aid.html',
            context = {
                'aid_type':aid_type,
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'mobile':mobile
            }
        )

        message.send([email,settings.EMAIL_HOST_USER])
        
    except Exception as e:
        return e    
    

def send_sponsorship_email( name_of_sponsor, selection, number_of_student, email, phone_number, remarks):
    try:
        message = BaseEmailMessage(template_name='api/email_response/sponsorship.html',
            context = {
                'name_of_sponsor':name_of_sponsor,
                'selection':selection,
                'email':email,
                'phone_number':phone_number,
                'number_of_student':number_of_student,
                'remarks':remarks,
            }
        )

        message.send([email,settings.EMAIL_HOST_USER])

    except Exception as e:
        return e     