from django.db import models
from django.utils.text import slugify
from datetime import datetime

# Create your models here.


class Course(models.Model):

    COURSE_TYPE = [
        ('programming', 'Programming'),
        ('data analysis', 'Data Analysis'),
        ('ui/ux with figma', 'UI/UX with Figma'),
        ('kids coding', 'Kids Coding'),
    ]

    ordering = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=300)
    frontpage_featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    delisted = models.BooleanField(default=False)
    slug = models.CharField(max_length=150, null=True, blank=True)
    extra_note = models.TextField(null=True, blank=True)
    course_level_code = models.CharField(max_length=20, null=True, blank=True)
    location_state = models.CharField(
        max_length=50, null=True, blank=True)  # Lagos, Abuja etc
    location_state_area = models.CharField(
        max_length=50, null=True, blank=True)  # Lekki, ikeja etc
    card_title = models.CharField(max_length=100, null=True, blank=True)
    tech_subs = models.CharField(max_length=100, null=True)
    audience = models.CharField(max_length=100, null=True, blank=True)
    audience_description = models.TextField(null=True, blank=True)
    # programming, data science etc
    course_type = models.CharField(
        max_length=30, blank=True, choices=COURSE_TYPE)
    description = models.TextField()
    course_outline = models.TextField()
    what_you_will_learn = models.TextField()
    requirements = models.CharField(max_length=450)
    prerequisites = models.CharField(max_length=450)
    last_updated = models.DateTimeField()
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
        return f'{self.course_level_code} - {self.title}'

    def get_absolute_url(self):
        return f'/{self.location_state}/{self.location_state_area}/{self.slug}/'


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    courses_taking = models.ManyToManyField(Course)

    def __str__(self):
        return self.fullname


class Schedule(models.Model):
    teacher = models.OneToOneField(
        Teacher, on_delete=models.DO_NOTHING, null=True, blank=True)
    active = models.BooleanField()
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


class Enrollment(models.Model):
    fullname = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    date_enrolled = models.DateTimeField(default=datetime.now())
    course_startdate = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.fullname} - {self.mobile}'
