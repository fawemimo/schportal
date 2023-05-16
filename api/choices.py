# user model
USER_TYPE_CHOICES = (
    ("teacher", "Teacher"),
    ("student", "Student"),
    ("employer", "Employer"),
)


# Student Attendance
ABSENT = "Absent"
PRESENT = "Present"
ATTENDANCE_CHOICES = (
    (ABSENT, "Absent"),
    (PRESENT, "Present"),
)

# Kids Model
AGE_BRACKET_CHOICES = (("6-9", "6-9"), ("10-14", "10-14"))


# Financial Aid Model
AID_TYPE_CHOICES = (
    ("Student Loan", "Student Loan"),
    (
        "Full Scholarship(Tuition + Laptop + Stipends)",
        "Full Scholarship(Tuition + Laptop + Stipends)",
    ),
    (
        "Scholarship Tier 1 (Tuition + Laptop)",
        "Scholarship Tier 1 (Tuition + Laptop)",
    ),
    ("Scholarship Tier 2 (Tuition)", "Scholarship Tier 2 (Tuition)"),
)


# Community Connect Models
COMMUNITY_TYPE = (("Webinars", "Webinars"), ("Meetups", "Meetups"))


# HowItWork Models
HOW_IT_WORK_CLASS_TYPE = (
    ("Physical Class", "Physical Class"),
    ("Virtual Class", "Virtual Class"),
)


# Job Model
STATUS = (("Draft", "Draft"), ("Published", "Published"))


# Billing Model
PENDING = "pending"
FAILED = "failed"
SUCCESS = "success"

PAYMENT_COMPLETION_STATUS = (
    (PENDING, "pending"),
    (FAILED, "failed"),
    (SUCCESS, "success"),
)


# Billing Detail Models
PROGRAM_TYPE_CHOICES = (("Onsite", "Onsite"), ("Virtual", "Virtual"))

# Blog Model
OPTIONS = (("published", "Published"), ("draft", "Draft"))

# CAREER OPENING
QUALIFICATION_CHOICES = (
    ("PhD", "PhD"),
    ("Msc", "Msc"),
    ("Bsc/B.Tech", "Bsc/B.Tech"),
    ("HND", "HND"),
    ("OND/NCE", "OND/NCE"),
    ("SSCE", "SSCE"),
)


DEGREE_CHOICES = (
    ("First Class", "First Class"),
    ("Second Class Upper", "Second Class Upper"),
    ("Second Class Lower", "Second Class Lower"),
)


# sitemaps
JOB_BASE_URL = '/jobs'