
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Billing, BillingDetail, Employer, Student, Teacher, User


@receiver(post_save, sender=User)
def create_teacher_profile(sender, created, instance, *args, **kwargs):
    if created:
        if instance.user_type == "teacher":
            f_name = instance.first_name
            l_name = instance.last_name
            Teacher.objects.create(
                user=instance, when_joined="2022-01-01", full_name=f"{f_name} {l_name}"
            )
            instance.save()

        elif instance.user_type == "student":
            f_name = instance.first_name
            l_name = instance.last_name
            mobile_numbers = instance.mobile_numbers
            Student.objects.create(user=instance, full_name=f"{f_name} {l_name}", mobile_numbers=mobile_numbers)
            instance.save()

        # elif instance.user_type == "employer":
        #     # f_name = instance.first_name
        #     # l_name = instance.last_name
        #     Employer.objects.create(user=instance)
        #     instance.save()


@receiver(post_save, sender=Billing)
def create_billing_details(sender, instance,created,*args,**kwargs):
    if created:
        BillingDetail.objects.create(billing=instance,course_fee = instance.schedule.fee if instance.schedule.program_type == 'Onsite' else instance.schedule.fee_dollar )
        # , course_fee = instance.schedule.fee if instance.schedule.program_type == 'Onsite' else instance.schedule.program_type == 'Virtual'
        # if instance.schedule.program_type == 'Onsite':
        #     billingdetails.course_fee = instance.schedule.fee_dollar
        #     return instance.schedule.fee
        # elif instance.schedule.program_type == 'Virtual':
        #     billingdetails.course_fee = instance.schedule.fee_dollar 
        #     return instance.schedule.fee_dollar 
        # else:
        #     pass
        instance.save()

