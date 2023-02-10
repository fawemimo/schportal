from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator, MinValueValidator
import math
from decimal import Decimal

class User(AbstractUser):
    user_type_choices = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=7,choices=user_type_choices,blank=True,null=True)


# region core models - mainsite


class CourseCategory(models.Model):
    title = models.CharField(max_length=150)
    child_1 = models.CharField(max_length=250, blank=True, null=True)
    child_2 = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    coursecategory = models.ForeignKey(
        CourseCategory, on_delete=models.DO_NOTHING)
    ordering = models.IntegerField(null=True, blank=True)
    kids_coding = models.BooleanField(default=False)
    is_virtual_class = models.BooleanField(default=False)
    title = models.CharField(max_length=300)
    frontpage_featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    delisted = models.BooleanField(default=False)
    slug = models.CharField(max_length=150, null=True, blank=True)
    extra_note = models.TextField(null=True, blank=True)
    course_code = models.CharField(max_length=20, null=True, blank=True)
    location_state = models.CharField(
        max_length=50, null=True, blank=True, default='Lagos')  # Lagos, Abuja etc
    location_state_area = models.CharField(
        max_length=50, null=True, blank=True, default='Ikeja')  # Lekki, ikeja etc
    card_title = models.CharField(max_length=100, null=True, blank=True)
    tech_subs = models.CharField(max_length=100, null=True, blank=True)
    audience = models.CharField(max_length=100, null=True, blank=True)
    audience_description = models.TextField(null=True, blank=True)
    description = models.TextField()
    course_outline = models.TextField(null=True, blank=True)
    course_outline_pdf = models.FileField(blank=True,null=True, upload_to='courseoutline/files')
    what_you_will_learn = models.TextField(null=True, blank=True)
    requirements = models.CharField(max_length=450, null=True, blank=True)
    prerequisites = models.TextField(null=True, blank=True)
    card_thumb = models.ImageField(
        null=True, blank=True, upload_to='courseimg')
    pic1_detailpage_banner = models.ImageField(
        null=True, blank=True, upload_to='courseimg')
    pic2_detailpage_main = models.ImageField(
        null=True, blank=True, upload_to='courseimg')
    pic3 = models.ImageField(null=True, blank=True, upload_to='courseimg')

    seo_pagetitle = models.CharField(max_length=200, null=True, blank=True)
    seo_metabulk = models.TextField(null=True, blank=True)

    def snippet(self):
        return self.description[:120] + ' ...'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(args, kwargs)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/{self.location_state}/{self.location_state_area}/{self.slug}/'


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    student_idcard_id = models.CharField(max_length=50, null=True, blank=True)
    mobile_numbers = models.CharField(max_length=250)
    profile_pic = models.ImageField(upload_to='students_profilepix/')
    residential_address = models.CharField(max_length=250)
    contact_address = models.CharField(max_length=250)
    next_of_kin_fullname = models.CharField(max_length=150)
    next_of_kin_contact_address = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.user} - {self.student_idcard_id}'


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    teacher_idcard_id = models.CharField(max_length=50, blank=True, null=True)
    courses_taking = models.ManyToManyField(Course)
    when_joined = models.DateField()

    def __str__(self):
        return f'{self.user}'


class Schedule(models.Model):
    program_type_choices = (
        ('Physical/Onsite Class', 'Physical/Onsite Class'),
        ('Virtual/Online Class', 'Virtual/Online Class'),
    )

    program_type = models.CharField(max_length=50, choices = program_type_choices,blank=True,null=True)
    active = models.BooleanField(default=False)
    registration_status = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True)
    startdate = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=50)
    timing = models.CharField(max_length=450, blank=True)
    
    fee = models.IntegerField(null=True, blank=True)    
    discounted_fee = models.IntegerField(null=True, blank=True)

    discounted_fee_dollar = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    naira_to_dollar_rate = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True, validators=[MinValueValidator(1)])
    fee_dollar = models.IntegerField(editable=False, default=0)

    # overriding the save method to input the dollar fee
    def save(self, *args, **kwargs):
        half_fee = 0
        if self.fee is not None:
            half_fee = self.fee / 2
        fee_dollar = 0
        if self.naira_to_dollar_rate is not None:
            fee_dollar = Decimal(half_fee) / self.naira_to_dollar_rate 

        round_up = math.ceil(fee_dollar)
        self.fee_dollar = round_up
        super(Schedule, self).save(args, kwargs)

    def __str__(self):
        return f'{self.teacher} - {self.course}'


class Batch(models.Model):
    title = models.CharField(max_length=150)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f'{self.title}'


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
    batch = models.CharField(max_length=255)
    course_taken = models.CharField(max_length=150)
    published = models.BooleanField(default=False)
    body = models.TextField()

    def __str__(self):
        return self.student_name


class TechIcon(models.Model):
    tech_name = models.CharField(max_length=150)
    icon_img = models.ImageField(upload_to='techicons/', null=True)
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
    tartiary_education = models.CharField(max_length=50,blank=True,null=True)
    tartiary_studied = models.CharField(max_length=150,blank=True,null=True)
    secondary_sch = models.CharField(max_length=150,blank=True,null=True)
    secondary_studied = models.CharField(max_length=150,blank=True,null=True)
    tech_interest = models.CharField(max_length=150,blank=True,null=True)
    more_about_you = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.fullname


class Inquiry(models.Model):
    fullname = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.fullname

# endregion


# region student portal


class InterestedForm(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=155)
    email = models.EmailField(max_length=155)
    mobile = models.CharField(max_length=50)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} - {self.course.title}'


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    enrolled = models.BooleanField(default=True)
    training_date = models.DateTimeField()

    def __str__(self):
        return f'{self.student} - {self.course}'


class Assignment(models.Model):
    batch = models.ForeignKey(
        Batch, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    assignment_file = models.FileField(upload_to='assignment/%Y%M%d')
    assignment_given = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class AssignmentAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_date = models.DateField()
    deadline = models.DateField()

    def __str__(self):
        return f'{self.student.user}'


class Project(models.Model):
    name = models.CharField(max_length=255)
    project_docs = models.FileField(upload_to='project/%Y%M%d')
    project_assigned = models.BooleanField(default=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    supervisor = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    delivery_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.user}'


class CourseManual(models.Model):
    title = models.CharField(max_length=350, blank=True, null=True)
    course = models.ManyToManyField(Course)
    manual = models.FileField(upload_to='coursemanual/')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseManualAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_manual = models.ForeignKey(CourseManual, on_delete=models.CASCADE)
    released_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    when_released = models.DateField()

    def __str__(self):
        return f'{self.student.user}'


class ResourceType(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    short_description = models.TextField(blank=True, null=True)
    primer = models.FileField(upload_to='free/primer', blank=True, null=True)
    cheat_sheat = models.FileField(
        upload_to='free/cheat_sheat', blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.resource_type.name}'


class StudentAttendance(models.Model):

    ABSENT = 'Absent'
    PRESENT = 'Present'
    attendance_choices = (
        (ABSENT, 'Absent'),
        (PRESENT, 'Present'),
    )

    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    attendance_status = models.CharField(
        max_length=50, choices=attendance_choices, default=ABSENT)
    timestamp = models.DateTimeField(blank=True, null=True)
    attendance_comment = models.CharField(max_length=255)
    raise_warning = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student.user}'


class VirtualClass(models.Model):
    country_of_residence = models.CharField(max_length=255,blank=True,null=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class KidsCoding(models.Model):
    age_bracket_choices = (
        ('1', '6-9'),
        ('2', '10-14')
    )
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    age_bracket = models.CharField(max_length=150, choices=age_bracket_choices)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class InternationalModel(models.Model):
    ordering = models.CharField(max_length=25, blank=True, null=True)
    country_name = models.CharField(max_length=255)
    flag = models.ImageField(upload_to='international/flags',validators=[FileExtensionValidator(allowed_extensions = ['jpg','jpeg','png'])])
    country_code = models.CharField(max_length=255)
    topbar_src = models.TextField()
    intro_txt = models.TextField()

    def __str__(self):
        return self.country_name


# endregion
