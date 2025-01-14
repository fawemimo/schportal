import random
import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from tinymce import models as tinymce_models

from api.choices import *
from api.utils import *
from api.validate import validate_file_size


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_numbers = models.CharField(max_length=50, blank=True, null=True)
    user_type = models.CharField(
        max_length=8, choices=USER_TYPE_CHOICES, blank=True, null=True
    )


# region core models - mainsite


class SEO(models.Model):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    page_name = models.CharField(max_length=255)
    meta_content = models.TextField()

    def __str__(self):
        return self.page_name


class LoanPartner(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    descriptions = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class CourseCategory(models.Model):
    title = models.CharField(max_length=150)
    child_1 = models.CharField(max_length=250, blank=True, null=True)
    child_2 = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return f"/{self.title}/"


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
        self.location_state = self.location_state.lower()
        self.location_state_area = self.location_state_area.lower()
        super(Course, self).save(args, kwargs)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return f"/courses/{self.location_state}/{self.location_state_area}/{self.slug}/"


class CorporateCourseSection(models.Model):
    intro_text = models.TextField()

    def __str__(self):
        return str(self.id)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    job_ready = models.BooleanField(
        default=False, help_text="to control student for job applications"
    )
    just_for_jobs = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    mobile_numbers = models.CharField(max_length=250, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to="students_profilepix/",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"]),
        ],
        blank=True,
        null=True,
    )
    cv_upload = models.FileField(
        upload_to="JobPortal/cv_upload",
        validators=[FileExtensionValidator(allowed_extensions=("pdf",))],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{str(self.id)}:{self.full_name}"


class Student_Matriculation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    matric_number = models.CharField(max_length=50, unique=True)
    expel = models.BooleanField(default=False, verbose_name="Expelled")
    matric_date = models.DateField()
    graduation_date = models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    residential_address = models.CharField(max_length=250)
    contact_address = models.CharField(max_length=250)
    next_of_kin_fullname = models.CharField(max_length=150)
    next_of_kin_contact_address = models.CharField(max_length=250)
    next_of_kin_mobile_number = models.CharField(max_length=250)
    relationship_with_next_kin = models.CharField(max_length=255)

    def __str__(self):
        return self.student.full_name


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
        return f"{self.teacher} - {self.course}: {self.program_type}"


class CourseWaitingList(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=255)

    def __str__(self):
        return f"{first_name} {last_name}"


class Batch(models.Model):
    program_type = models.CharField(
        max_length=50, blank=True, null=True, choices=PROGRAM_TYPE_CHOICES
    )
    title = models.CharField(max_length=150)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    course_manuals = models.ManyToManyField("CourseManual", blank=True)
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

    class Meta:
        ordering = ["ordering"]


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
    course_taken = models.ForeignKey(
        Course, on_delete=models.DO_NOTHING, blank=True, null=True
    )
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
    join_our_team = models.TextField(blank=True, null=True)
    ordering = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return f"/about/"


class StudentLoanSection(models.Model):
    is_published = models.BooleanField(default=False)
    loan_intro = models.TextField()
    eligibility = models.TextField()

    def __str__(self):
        return str(self.id)


class CareerSection(models.Model):
    our_culture = models.TextField()
    how_we_hire = models.TextField()
    what_we_offer = models.TextField()
    find_your_role = models.TextField()

    def __str__(self):
        return str(self.id)


class CareerCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.title}/"


class CareerOpening(models.Model):
    is_published = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_location = models.ForeignKey("JobLocation", on_delete=models.CASCADE)
    employment_type = models.ForeignKey("JobType", on_delete=models.CASCADE)
    career_category = models.ForeignKey(CareerCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CareerApplicant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=255)
    course_study = models.CharField(max_length=255, blank=True, null=True)
    highest_qualification = models.CharField(
        max_length=255, choices=QUALIFICATION_CHOICES, blank=True, null=True
    )
    degree = models.CharField(
        max_length=50, choices=DEGREE_CHOICES, blank=True, null=True
    )
    career_opening = models.ForeignKey(CareerOpening, on_delete=models.CASCADE)
    current_salary = models.CharField(max_length=255, blank=True, null=True)
    salary_expectation = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(
        upload_to="career/applicant/",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["pdf"]),
        ],
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return f"/{self.career_opening.title}/"


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

    def get_absolute_url(self):
        return f"/alumni/"


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


class Sponsor(models.Model):
    choices_type = (
        ("Individual", "Individual"),
        ("Organization", "Organization"),
    )
    active = models.BooleanField(default=False)
    name_of_sponsor = models.CharField(max_length=255)
    selection = models.CharField(max_length=50, choices=choices_type)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    number_of_student = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    remarks = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_of_sponsor


class Announcement(models.Model):
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
    eligibility = models.TextField(blank=True, null=True)
    wings = models.TextField()
    terms_and_conditions = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return f"/scholarship/"


class Album(models.Model):
    ordering = models.PositiveIntegerField()
    main_title = models.CharField(max_length=255)
    main_description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    image_cover = models.ImageField(
        upload_to="album/cover/",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "svg"]),
        ],
        blank=True,
        null=True,
    )
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.main_title

    class Meta:
        ordering = ["-ordering"]


class AlbumDetail(models.Model):
    ordering = models.PositiveIntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    image = models.ImageField(
        upload_to="album/details/",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "svg"]),
        ],
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-ordering"]


# endregion


# region student portal


class ScholarshipAward(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    award_date = models.DateTimeField()
    total_amount = models.CharField(max_length=255)
    amount_received = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(auto_now=True)
    number_of_students = models.PositiveIntegerField()
    beneficiaries = models.ManyToManyField(Student)
    remarks = models.TextField()

    def __str__(self):
        return f"{self.sponsor.name_of_sponsor}- {self.award_date}"


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, blank=True, null=True
    )
    program_type = models.CharField(max_length=50, blank=True, null=True)
    fee = models.CharField(max_length=250, blank=True, null=True)
    fee_dollar = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.CharField(max_length=50, blank=True, null=True)
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

    def get_absolute_url(self):
        return f"/resources/{self.resource_type.slug}/"


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
    identify_our_virutal_courses = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.country_name

    def save(self, *args, **kwargs):
        self.country_name = self.country_name.lower()
        super(InternationalModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/international/"


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

    def get_absolute_url(self):
        return f"/events/"


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

    def get_absolute_url(self):
        return f"/terms/"


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
    profile_approval = models.BooleanField(default=False)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_person_mobile = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    company_url = models.CharField(blank=True, null=True, max_length=255)
    tagline = models.TextField(blank=True, null=True)
    company_logo = models.ImageField(
        upload_to="JobPortal/Company",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["svg", "jpg", "png", "jpeg"]),
        ],
        blank=True,
        null=True,
    )
    kyc_document = models.FileField(
        upload_to="JobPortal/Company",
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=["pdf"]),
        ],
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"


class JobCategory(models.Model):
    title = models.CharField(max_length=255)
    ordering = models.PositiveIntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.title}/"

    class Meta:
        ordering = ["ordering"]


class JobExperience(models.Model):
    title = models.CharField(max_length=255)
    ordering = models.PositiveIntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.title}/"

    class Meta:
        ordering = ["-ordering"]


class BaseJobSelection(models.Model):
    title = models.CharField(max_length=255)
    ordering = models.PositiveIntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.title}/"

    class Meta:
        ordering = ["-ordering"]


class JobType(BaseJobSelection):
    pass


class JobLocation(BaseJobSelection):
    pass


class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_category = models.ManyToManyField(JobCategory)
    experience = models.ManyToManyField(JobExperience)
    job_type = models.ForeignKey(
        JobType, on_delete=models.CASCADE, blank=True, null=True
    )
    job_location = models.ForeignKey(
        JobLocation, on_delete=models.CASCADE, blank=True, null=True
    )
    job_title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    posting_approval = models.BooleanField(default=False)
    job_summary = tinymce_models.HTMLField()
    job_responsibilities = tinymce_models.HTMLField()
    close_job = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    seo_meta_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employer}:- {self.job_title}"

    def save(self, *args, **kwargs):
        num = range(100, 1000)
        ran = random.choice(num)
        self.slug = f"{(slugify(self.job_title))}-{ran}"
        super(Job, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{JOB_BASE_URL}/{self.slug}/{self.id}/"

    class Meta:
        ordering = ["-date_posted"]


class JobApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied = models.BooleanField(default=False)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student)

    class Meta:
        ordering = ["-date_applied"]
        unique_together = [("student", "job")]


# endportal region


# Billing information region


class Billing(models.Model):
    got_scholarship = models.BooleanField(default=False)
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    got_loan = models.BooleanField(default=False)
    loanpartner = models.ForeignKey(
        LoanPartner, on_delete=models.CASCADE, blank=True, null=True
    )
    course_name = models.ForeignKey(
        Course, blank=True, null=True, on_delete=models.PROTECT
    )
    program_type = models.CharField(
        max_length=50, choices=PROGRAM_TYPE_CHOICES, blank=True, null=True
    )
    course_fee = models.PositiveBigIntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, null=True, blank=True
    )
    total_amount = models.PositiveBigIntegerField(blank=True, null=True)
    total_amount_text = tinymce_models.HTMLField(blank=True, null=True)
    payment_completion_status = models.CharField(
        default=PENDING,
        choices=PAYMENT_COMPLETION_STATUS,
        max_length=50,
        blank=True,
        null=True,
    )
    receipt_no = models.CharField(
        max_length=255, unique=True, editable=False, blank=True, null=True
    )
    date_posted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{str(self.student.full_name)}-{str(self.id)}"

    def save(self, *args, **kwargs):
        try:
            batch_id = self.student.batch_set.values("id")
            if not self.pk:
                batch_id = [x["id"] for x in batch_id]
                self.receipt_no = generate_receipt_num(batch_id[0])
            super(Billing, self).save(*args, **kwargs)
        except Exception as e:
            print(e)


class BillingDetail(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
    amount_paid = models.PositiveBigIntegerField(blank=True, null=True)
    payment_descriptions = models.CharField(max_length=250, blank=True, null=True)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


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

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"


# END BLOG MODEL REGION


# FORUM API MODELS


class Topic(models.Model):
    title = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,blank=True,null=True)
    topics = models.ManyToManyField(Topic)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    likes = models.PositiveIntegerField(null=True, blank=True)
    dislikes = models.PositiveIntegerField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        num = range(100, 1000)
        ran = random.choice(num)
        self.slug = f"{(slugify(self.title))}-{ran}"
        super(Question, self).save(*args, **kwargs)


class QuestionComment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(null=True, blank=True)
    dislikes = models.PositiveIntegerField(null=True, blank=True)
    date_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student}"


# END FORUM API MODELS
