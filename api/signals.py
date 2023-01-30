from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Teacher,Student


@receiver(post_save, sender=User)
def create_teacher_profile(sender, created, instance, *args, **kwargs):
    if created:
        if instance.user_type =='teacher':
            Teacher.objects.create(user=instance,when_joined='2022-01-01')
            instance.save()
        elif instance.user_type == 'student':
            Student.objects.create(user=instance)
            instance.save()    
