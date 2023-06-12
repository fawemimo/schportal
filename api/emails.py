from datetime import date

from django.conf import settings
from templated_mail.mail import BaseEmailMessage

from api.models import Course, Schedule


def send_inquiries_email(fullname, email, mobile, message):
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/iniquiries.html",
            context={
                "fullname": fullname,
                "email": email,
                "mobile": mobile,
                "message": message,
            },
        )
        message.send([email, settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)


def send_interested_email(course_id, full_name, email, mobile, schedule_id):
    course = Course.objects.get(id=course_id)
    schedule = Schedule.objects.get(id=schedule_id)

    try:
        message = BaseEmailMessage(
            template_name="api/email_response/interested_emails.html",
            context={
                "course": course.title,
                "program_type": schedule.program_type,
                "startdate": schedule.startdate,
                "fee": schedule.fee,
                "discounted_fee": schedule.discounted_fee,
                "fee_dollar": schedule.fee_dollar,
                "discounted_fee_dollar": schedule.discounted_fee_dollar,
                "duration": schedule.duration,
                "course_id": course_id,
                "full_name": full_name,
                "email": email,
                "mobile": mobile,
            },
        )
        message.send([email, settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)


def send_virtualclass_email(
    course_id, full_name, email, mobile, remarks, country_of_residence
):
    course = Course.objects.get(id=course_id)
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/virtual_class.html",
            context={
                "course": course.title,
                "course_id": course_id,
                "full_name": full_name,
                "email": email,
                "mobile": mobile,
                "remarks": remarks,
                "country_of_residence": country_of_residence,
            },
        )
        message.send([email, settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)


def send_kids_coding_email(age_bracket, full_name, email, mobile, remarks):
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/kidscoding.html",
            context={
                "age_bracket": age_bracket,
                "full_name": full_name,
                "email": email,
                "mobile": mobile,
                "remarks": remarks,
            },
        )
        message.send([email, settings.EMAIL_HOST_USER])
    except Exception as e:
        print(e)


def send_short_quizze_email(
    fullname,
    email,
    mobile,
    tartiary_education,
    tartiary_studied,
    secondary_sch,
    secondary_studied,
    tech_interest,
    more_about_you,
):
    today_date = date.today()
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/career_choice.html",
            context={
                "today_date": today_date,
                "fullname": fullname,
                "email": email,
                "mobile": mobile,
                "tartiary_education": tartiary_education,
                "tartiary_studied": tartiary_studied,
                "secondary_sch": secondary_sch,
                "secondary_studied": secondary_studied,
                "tech_interest": tech_interest,
                "more_about_you": more_about_you,
            },
        )
        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        print(e)


def send_financial_aid_email(
    aid_type,
    course,
    first_name,
    last_name,
    email,
    mobile,
    relationship_with_guarantor,
    residential_address,
    guarantor_full_name,
    guarantor_residential_contact_address,
    guarantor_mobile,
):
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/financial_aid.html",
            context={
                "aid_type": aid_type,
                "course": course,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "mobile": mobile,
                "relationship_with_guarantor": relationship_with_guarantor,
                "residential_address": residential_address,
                "guarantor_full_name": guarantor_full_name,
                "guarantor_residential_contact_address": guarantor_residential_contact_address,
                "guarantor_mobile": guarantor_mobile,
            },
        )

        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        return e


def send_sponsorship_email(
    name_of_sponsor,
    selection,
    number_of_student,
    email,
    phone_number,
    remarks,
    organization_name,
):
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/sponsorship.html",
            context={
                "name_of_sponsor": name_of_sponsor,
                "selection": selection,
                "organization_name": organization_name,
                "email": email,
                "phone_number": phone_number,
                "number_of_student": number_of_student,
                "remarks": remarks,
            },
        )

        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        return e


def send_employer_sign_up_email(email, contact_person):
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/employer_sign_up.html",
            context={
                "contact_person": contact_person,
                "email": email,
            },
        )

        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        print(e)


def send_career_applicant_email(
    career_opening,
    first_name,
    last_name,
    email,
    mobile,
    highest_qualification,
    course_study,
    degree,
):
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/career_opening.html",
            context={
                "career_opening": career_opening,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "mobile": mobile,
                "course_study": course_study,
                "degree": degree,
                "highest_qualification": highest_qualification,
            },
        )

        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        print(e)


def send_loan_partner_email(email, contact_person, company_name, address, mobile,descriptions):
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/loan_partner.html",
            context={
                "email": email,
                "contact_person": contact_person,
                "company_name": company_name,
                "address": address,
                "mobile": mobile,
                "descriptions":descriptions
            },
        )
        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        print(e)

def send_course_waiting_list(course_id,first_name,last_name,email,mobile):
    course = Course.objects.get(id=course_id)
    try:
        message = BaseEmailMessage(
            template_name="api/email_response/course_waiting_list.html",
            context={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "mobile": mobile,
                "course":course.title
            },
        )
        message.send([email, settings.EMAIL_HOST_USER])

    except Exception as e:
        print(e)