import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from tinymce import models as tinymce_models

from api.choices import *
from api.validate import validate_file_size


class User(AbstractUser):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_numbers = models.CharField(max_length=50, blank=True, null=True)
    user_type = models.CharField(
        max_length=8, choices=USER_TYPE_CHOICES, blank=True, null=True
    )


# region core models - mainsite


class CourseCategory(models.Model):
    title = models.CharField(max_length=150)
    child_1 = models.CharField(max_length=250, blank=True, null=True)
    child_2 = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    coursecategory = models.ForeignKey(CourseCategory, on_delete=models.DO_NOTHING)
    ordering = models.IntegerField(null=True, blank=True)
    kids_coding = models.BooleanField(default=False)
    is_virtual_class = models.BooleanField(default=False)
    title = models.CharField(max_length=300)
    frontpage_featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    delisted = models.BooleanField(default=False)
    slug = models.CharField(max_length=150, null=True, blank=True)
    course_code = models.CharField(max_length=20, null=True, blank=True)
    location_state = models.CharField(
        max_length=50, null=True, blank=True, default="Lagos"
    )  # Lagos, Abuja etc
    location_state_area = models.CharField(
        max_length=50, null=True, blank=True, default="Ikeja"
    )  # Lekki, ikeja etc
    card_title = models.CharField(max_length=100, null=True, blank=True)
    tech_subs = models.CharField(max_length=100, null=True, blank=True)
    audience = models.CharField(max_length=100, null=True, blank=True)
    audience_description = models.TextField(null=True, blank=True)
    description = models.TextField()
    course_outline_pdf = models.FileField(
        blank=True, null=True, upload_to="courseoutline/files"
    )
    what_you_will_learn = models.TextField(null=True, blank=True)
    prerequisites = models.TextField(null=True, blank=True)
    card_thumb = models.ImageField(null=True, blank=True, upload_to="courseimg")
    pic1_detailpage_banner = models.ImageField(
        null=True, blank=True, upload_to="courseimg"
    )
    pic2_detailpage_main = models.ImageField(
        null=True, blank=True, upload_to="courseimg"
    )
    pic3 = models.ImageField(null=True, blank=True, upload_to="courseimg")

    seo_pagetitle = models.CharField(max_length=200, null=True, blank=True)
    seo_metabulk = models.TextField(null=True, blank=True)

    def snippet(self):
        return self.description[:120] + " ..."

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(args, kwargs)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return f"/{self.location_state}/{self.location_state_area}/{self.slug}/"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    # billings = models.OneToOneField("Billing", on_delete=models.CASCADE, blank=True, null=True, related_name = '+')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    student_idcard_id = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    mobile_numbers = models.CharField(max_length=250, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to="students_profilepix/",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"]),
        ],
    )
    residential_address = models.CharField(max_length=250, blank=True, null=True)
    contact_address = models.CharField(max_length=250, blank=True, null=True)
    next_of_kin_fullname = models.CharField(max_length=150, blank=True, null=True)
    next_of_kin_contact_address = models.CharField(
        max_length=250, blank=True, null=True
    )
    next_of_kin_mobile_number = models.CharField(max_length=250, blank=True, null=True)
    relationship_with_next_kin = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    teacher_idcard_id = models.CharField(max_length=50, blank=True, null=True)
    courses_taking = models.ManyToManyField(Course)
    when_joined = models.DateField()

    def __str__(self):
        return f"{self.user}"


class Schedule(models.Model):
    program_type = models.CharField(
        max_length=50, choices=PROGRAM_TYPE_CHOICES, blank=True, null=True
    )
    active = models.BooleanField(default=False)
    registration_status = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True
    )
    startdate = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=50)
    timing = models.CharField(max_length=450, blank=True)

    fee = models.IntegerField(null=True, blank=True)
    discounted_fee = models.IntegerField(null=True, blank=True)

    fee_dollar = models.IntegerField(blank=True, null=True)
    discounted_fee_dollar = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.teacher} - {self.course}"


class Batch(models.Model):
    title = models.CharField(max_length=150)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return f"{self.title}"


class TopBar(models.Model):
    title = models.CharField(max_length=150)
    published = models.BooleanField(default=False)
    bar_src = models.TextField()

    def __str__(self):
        return self.title


class MainBanner(models.Model):
    ordering = models.CharField(max_length=50, blank=True, null=True)
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
    student_pic = models.ImageField(upload_to="testimonial_pic/")
    batch = models.CharField(max_length=255)
    course_taken = models.CharField(max_length=150)
    published = models.BooleanField(default=False)
    body = models.TextField()

    def __str__(self):
        return self.student_name


class TechIcon(models.Model):
    tech_name = models.CharField(max_length=150)
    icon_img = models.ImageField(upload_to="techicons/", null=True)
    popup_src = models.TextField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.tech_name


class FeaturedProject(models.Model):
    title = models.CharField(max_length=350)
    student_name = models.CharField(max_length=150)
    student_pic = models.ImageField(
        upload_to="studentprojectpic/", null=True, blank=True
    )
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


class AboutUsSection(models.Model):
    about_intro = models.TextField()
    our_mission = models.TextField()
    our_mission_item = models.TextField()
    why_anchorsoft = models.TextField()
    ordering = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)


class StudentLoanSection(models.Model):
    is_published = models.BooleanField(default=False)
    loan_intro = models.TextField()
    eligibility = models.TextField()

    def __str__(self):
        return str(self.id)


class CareerSection(models.Model):
    is_published = models.BooleanField(default=False)
    intro_banner = models.TextField()
    our_story = models.TextField()
    mission_values = models.TextField()
    team_description = models.TextField()

    def __str__(self):
        return str(self.id)


class AlbumSection(models.Model):
    is_published = models.BooleanField(default=False)
    album_photo = models.TextField()

    def __str__(self):
        return str(self.id)


class AlumiConnectSection(models.Model):
    is_published = models.BooleanField(default=False)
    intro = models.TextField()
    content = models.TextField()

    def __str__(self):
        return str(self.id)


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
    tartiary_education = models.CharField(max_length=50, blank=True, null=True)
    tartiary_studied = models.CharField(max_length=150, blank=True, null=True)
    secondary_sch = models.CharField(max_length=150, blank=True, null=True)
    secondary_studied = models.CharField(max_length=150, blank=True, null=True)
    tech_interest = models.CharField(max_length=150, blank=True, null=True)
    more_about_you = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname


class Inquiry(models.Model):
    fullname = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.fullname


class OurTeam(models.Model):
    image = models.ImageField()
    full_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    social_dump = models.TextField()

    def __str__(self):
        return str(self.id)


class Sponsorship(models.Model):
    choices_type = (
        ("Individual", "Individual"),
        ("Organization", "Organization"),
    )
    name_of_sponsor = models.CharField(max_length=255)
    selection = models.CharField(max_length=50, choices=choices_type)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    number_of_student = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    remarks = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str(self):
        return self.name_of_sponsor


class Announcement(models.Model):
    # cookie_id = models.UUIDField(default=uuid.uuid4, unique=True, blank=True,null=True)
    title = models.CharField(max_length=255)
    announcement = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        now = datetime.now()
        if self.expiration_date == now:
            self.is_published = False

        super(Announcement, self).save(args, kwargs)


class ScholarshipSection(models.Model):
    scholarship_intro = models.TextField()
    access_text = models.TextField()
    wings = models.TextField()

    def __str__(self):
        return str(self.id)


# endregion


# region student portal


class InterestedForm(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=155)
    email = models.EmailField(max_length=155)
    mobile = models.CharField(max_length=50)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course.title}"


class Assignment(models.Model):
    name = models.CharField(max_length=255)
    assignment_file = models.FileField(upload_to="assignment/%Y%M%d")
    assignment_given = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class AssignmentAllocation(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_date = models.DateField()
    deadline = models.DateField()

    def __str__(self):
        return f"{self.batch}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    project_docs = models.FileField(upload_to="project/%Y%M%d")
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
        return f"{self.student.user}"


class CourseManual(models.Model):
    title = models.CharField(max_length=350, blank=True, null=True)
    course = models.ManyToManyField(Course)
    manual = models.FileField(upload_to="coursemanual/")
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseManualAllocation(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=True, null=True)
    course_manual = models.ForeignKey(CourseManual, on_delete=models.CASCADE)
    released_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    when_released = models.DateField()

    def __str__(self):
        return f"{self.batch}"


class ResourceType(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    short_description = models.TextField(blank=True, null=True)
    primer = models.FileField(upload_to="free/primer", blank=True, null=True)
    cheat_sheat = models.FileField(upload_to="free/cheat_sheat", blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.resource_type.name}"


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    attendance_status = models.CharField(
        max_length=50, choices=ATTENDANCE_CHOICES, default=ABSENT
    )
    timestamp = models.DateTimeField(blank=True, null=True)
    attendance_comment = models.CharField(max_length=255)
    raise_warning = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user}"


class VirtualClass(models.Model):
    country_of_residence = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class KidsCoding(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    age_bracket = models.CharField(max_length=150, choices=AGE_BRACKET_CHOICES)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class InternationalModel(models.Model):
    ordering = models.CharField(max_length=25, blank=True, null=True, unique=True)
    country_name = models.CharField(max_length=255)
    flag = models.ImageField(
        upload_to="international/flags",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    country_code = models.CharField(max_length=255)
    topbar_src = models.TextField()
    why_choose_virtual = models.TextField()

    def __str__(self):
        return self.country_name

    def save(self, *args, **kwargs):
        self.country_name = self.country_name.lower()
        super(InternationalModel, self).save(*args, **kwargs)


class FinancialAid(models.Model):
    aid_type = models.CharField(max_length=50, choices=AID_TYPE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=50)
    residential_address = models.CharField(max_length=255, blank=True, null=True)
    guarantor_full_name = models.CharField(max_length=255, blank=True, null=True)
    guarantor_residential_contact_address = models.CharField(
        max_length=255, blank=True, null=True
    )
    relationship_with_guarantor = models.CharField(
        max_length=255, blank=True, null=True
    )
    guarantor_mobile = models.CharField(max_length=255, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CommunityConnect(models.Model):
    completed = models.BooleanField(default=False)
    ordering = models.CharField(max_length=5, blank=True, null=True)
    community = models.CharField(max_length=50, choices=COMMUNITY_TYPE)
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    image = models.ImageField(
        upload_to="community/banners",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )
    start_date = models.DateTimeField()

    def __str__(self):
        return self.title


class AlumiConnect(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TermsOfService(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VirtualVsOther(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.TextField()

    def __str__(self):
        return self.title


class HowItWork(models.Model):

    how_it_work_class = models.CharField(
        max_length=50, choices=HOW_IT_WORK_CLASS_TYPE, blank=True, null=True
    )
    content = models.TextField()

    def __str__(self):
        return str(self.id)


# endregion


# job portal region


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    tagline = models.TextField()
    company_logo = models.ImageField(
        upload_to="JobPortal/Company",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["svg", "jpg", "png", "jpeg"]),
        ],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class JobCategory(models.Model):

    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    experience = models.CharField(
        max_length=50, choices=EXPERIENCE_LEVEL, blank=True, null=True
    )
    job_type = models.CharField(max_length=50, choices=JOB_TYPE, blank=True, null=True)
    job_location = models.CharField(
        max_length=50, choices=JOB_LOCATION, blank=True, null=True
    )
    job_title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    save_as = models.CharField(max_length=50, choices=STATUS, default="Draft")
    job_summary = models.TextField()
    job_responsibilities = tinymce_models.HTMLField()
    close_job = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employer}:- {self.job_title}"


class JobApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cv_upload = models.FileField(
        upload_to="JobPortal/cv_upload",
        validators=[
            FileExtensionValidator(allowed_extensions=("pdf", "jpg", "jpeg", "png"))
        ],
    )
    years_of_experience = models.CharField(max_length=50)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student)


# endportal region


# Billing information region


class Billing(models.Model):
    transaction_ref = models.UUIDField(default=uuid.uuid4)
    squad_transaction_ref = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, blank=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    total_amount_paid = models.PositiveBigIntegerField(blank=True, null=True)
    total_amount = models.PositiveBigIntegerField(blank=True, null=True)
    payment_completion_status = models.CharField(
        default=PENDING,
        choices=PAYMENT_COMPLETION_STATUS,
        max_length=50,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)

    @property
    def get_grand_outstanding(self):

        try:
            billings = self.billingdetail_set.filter(billing_id=self.id).aggregate(
                amount_paid=Sum("amount_paid")
            )
            total_amount_paid = 0

            if billings:
                if total_amount_paid != None:
                    total_amount_paid = billings["amount_paid"]
                    cal = self.total_amount - total_amount_paid
                    return cal
                elif total_amount_paid == None:
                    total_amount_paid = 0
                    cal = self.total_amount - total_amount_paid

                    return cal
        except Exception as e:
            return None

    def save(self, *args, **kwargs):
        try:

            if self.total_amount == self.total_amount_paid:
                self.payment_completion_status = True

        except Exception as e:
            pass
        super(Billing, self).save(*args, **kwargs)


class BillingDetail(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
    program_type = models.CharField(
        max_length=50, choices=PROGRAM_TYPE_CHOICES, blank=True, null=True
    )
    amount_paid = models.PositiveBigIntegerField()
    outstanding_amount = models.PositiveBigIntegerField(null=True, blank=True)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def cal_sum_ofamount(self):
        try:
            # aggreagate amount paid wrt billing
            billings = self.billing.billingdetail_set.filter(billing_id=self.billing.id)
            sum_of_amount_paid = sum([x.amount_paid for x in billings])
            # amount of the course from amount paid
            if billings:
                amount_of_the_course = self.billing.total_amount
                sum_of_amount_paid = sum_of_amount_paid
                cal = self.billing.total_amount - sum_of_amount_paid
                return cal
        except Exception as e:
            pass

    def save(self, *args, **kwargs):
        try:

            self.outstanding_amount = self.cal_sum_ofamount()
        except Exception as e:
            pass

        super(BillingDetail, self).save(*args, **kwargs)


# End Billing Information region


# BLOG MODEL REGION


class BlogBaseModel(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    seo_keywords = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_created"]
        abstract = True

    def __str__(self):
        return self.title


class BlogCategory(BlogBaseModel):
    pass


class BlogPost(BlogBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    content = tinymce_models.HTMLField()
    image_1 = models.ImageField(upload_to="blog", blank=True, null=True)
    image_2 = models.ImageField(upload_to="blog", blank=True, null=True)
    image_3 = models.ImageField(upload_to="blog", blank=True, null=True)
    status = models.CharField(max_length=50, choices=OPTIONS)

    @property
    def short_content(self):
        return f"{self.content[:200]}...."


# END BLOG MODEL REGION
