
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import BackupStudent, Billing, BillingDetail, Employer, Student, Teacher, User


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


@receiver(post_save, sender=Billing)
def create_billing_details(sender, instance,created,*args,**kwargs):
    if created:
        BillingDetail.objects.create(billing=instance,course_fee = instance.schedule.fee if instance.schedule.program_type == 'Onsite' else instance.schedule.fee_dollar )
        instance.save()


@receiver(pre_save, sender=Student)
def create_backup_student(sender, instance, *args, **kwargs):

   
    BackupStudent.objects.create(student=instance, just_for_jobs=instance.just_for_jobs, full_name=instance.full_name, student_idcard_id=instance.student_idcard_id, date_of_birth=instance.date_of_birth, mobile_numbers=instance.mobile_numbers, profile_pic=instance.profile_pic, cv_upload=instance.cv_upload,residential_address=instance.residential_address, contact_address=instance.contact_address, next_of_kin_fullname=instance.next_of_kin_fullname, next_of_kin_contact_address=instance.next_of_kin_contact_address, next_of_kin_mobile_number=instance.next_of_kin_mobile_number, relationship_with_next_kin=instance.next_of_kin_mobile_number)

    instance.save()
