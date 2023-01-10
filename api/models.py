from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from datetime import datetime

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)


# region core models - mainsite


class CourseCategory(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    coursecategory = models.ForeignKey(
        CourseCategory, on_delete=models.DO_NOTHING)
    ordering = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=300)
    frontpage_featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    delisted = models.BooleanField(default=False)
    slug = models.CharField(max_length=150, null=True, blank=True)
    extra_note = models.TextField(null=True, blank=True)
    course_code = models.CharField(max_length=20, null=True, blank=True)
    location_state = models.CharField(
        max_length=50, null=True, blank=True)  # Lagos, Abuja etc
    location_state_area = models.CharField(
        max_length=50, null=True, blank=True)  # Lekki, ikeja etc
    card_title = models.CharField(max_length=100, null=True, blank=True)
    tech_subs = models.CharField(max_length=100, null=True, blank=True)
    audience = models.CharField(max_length=100, null=True, blank=True)
    audience_description = models.TextField(null=True, blank=True)
    description = models.TextField()
    course_outline = models.TextField(null=True, blank=True)
    what_you_will_learn = models.TextField(null=True, blank=True)
    requirements = models.CharField(max_length=450, null=True, blank=True)
    prerequisites = models.CharField(max_length=450, null=True, blank=True)
    card_thumb = models.ImageField(
        null=True, blank=True, upload_to='courseimg')
    pic1 = models.ImageField(null=True, blank=True, upload_to='courseimg')
    pic2 = models.ImageField(null=True, blank=True, upload_to='courseimg')
    pic3 = models.ImageField(null=True, blank=True, upload_to='courseimg')

    seo_pagetitle = models.CharField(max_length=200, null=True, blank=True)
    seo_metabulk = models.TextField(null=True, blank=True)

    def snippet(self):
        return self.description[:120] + ' ...'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(args, kwargs)

    def __str__(self):
        return f'{self.course_code} - {self.title}'

    def get_absolute_url(self):
        return f'/{self.location_state}/{self.location_state_area}/{self.slug}/'


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    courses_taking = models.ManyToManyField(Course)
    when_joined = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    student_id = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_numbers = models.CharField(max_length=250)
    email_addresses = models.CharField(max_length=250)
    profile_pic = models.ImageField(upload_to='students_profilepix/')
    residential_address = models.CharField(max_length=250)
    contact_address = models.CharField(max_length=250)
    next_of_kin_fullname = models.CharField(max_length=150)
    next_of_kin_contact_address = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Schedule(models.Model):
    active = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True)
    startdate = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=50)
    timing = models.CharField(max_length=450, blank=True)

    fee = models.IntegerField(null=True, blank=True)
    discounted_fee = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.teacher} - {self.course}'


class Batch(models.Model):
    title = models.CharField(max_length=150)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f'{self.title} - {self.start_date}'


class TopBar(models.Model):
    title = models.CharField(max_length=150)
    published = models.BooleanField(default=False)
    bar_src = models.TextField()

    def __str__(self):
        return self.title


class MainBanner(models.Model):
    title = models.CharField(max_length=150)
    published = models.BooleanField(default=False)
    banner_src = models.TextField()

    def __str__(self):
        return self.title


class SectionBanner(models.Model):
    title = models.CharField(max_length=150)
    published = models.BooleanField(default=False)
    banner_src = models.TextField()

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    student_name = models.CharField(max_length=250)
    student_pic = models.ImageField(upload_to='testimonial_pic/')
    batch = models.DateField()
    course_taken = models.CharField(max_length=150)
    published = models.BooleanField(default=False)
    body = models.TextField()

    def __str__(self):
        return self.student_name


class TechIcon(models.Model):
    tech_name = models.CharField(max_length=150)
    icon_img_src = models.TextField(null=True)
    popup_src = models.TextField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.tech_name


class FeaturedProject(models.Model):
    title = models.CharField(max_length=350)
    student_name = models.CharField(max_length=150)
    student_pic = models.ImageField(
        upload_to='studentprojectpic/', null=True, blank=True)
    course_taken = models.CharField(max_length=150)
    batch = models.DateField()
    project_img = models.ImageField()
    body = models.TextField()
    published = models.BooleanField(default=False)
    project_url = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class NavLink(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class NavLinkItem(models.Model):
    navlink = models.ForeignKey(NavLink, on_delete=models.CASCADE)
    item = models.CharField(max_length=250)
    item_url = models.CharField(max_length=150)

    def __str__(self):
        return self.item

# For any section that just requires a content dump
# like the footer etc


class ComponentDump(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return self.title


class ShortQuiz(models.Model):
    fullname = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=50)
    tartiary_education = models.CharField(max_length=50)
    tartiary_studied = models.CharField(max_length=150)
    secondary_sch = models.CharField(max_length=150)
    secondary_studied = models.CharField(max_length=150)
    tech_interest = models.CharField(max_length=150)
    more_about_you = models.TextField()


class Inquiry(models.Model):
    fullname = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=50)
    message = models.TextField()

# endregion


# region student portal


# endregion
