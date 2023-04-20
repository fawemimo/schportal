from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (Billing, BillingDetail, Employer, Student, StudentBackup,
                     Teacher, User)


@receiver(post_save, sender=User)
def create_teacher_profile(sender, created, instance, *args, **kwargs):
    try:
        if created:
            if instance.user_type == "teacher":
                f_name = instance.first_name
                l_name = instance.last_name
                Teacher.objects.create(
                    user=instance,
                    when_joined="2022-01-01",
                    full_name=f"{f_name} {l_name}",
                )
                instance.save()

            elif instance.user_type == "student":
                f_name = instance.first_name
                l_name = instance.last_name
                mobile_numbers = instance.mobile_numbers
                Student.objects.create(
                    user=instance,
                    full_name=f"{f_name} {l_name}",
                    mobile_numbers=mobile_numbers,
                )

                instance.save()

    except Exception as e:
        print(e)


@receiver(post_save, sender=Billing)
def create_billing_details(sender, instance, created, *args, **kwargs):
    if created:
        BillingDetail.objects.create(
            billing=instance,
            course_fee=instance.course_fee
        )
        instance.save()

