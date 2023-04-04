# user model
USER_TYPE_CHOICES = (
    ("teacher", "Teacher"),
    ("student", "Student"),
    ("employer", "Employer"),
)

# Schedule
PROGRAM_TYPE_CHOICES = (
    ("Physical/Onsite Class", "Physical/Onsite Class"),
    ("Virtual/Online Class", "Virtual/Online Class"),
)

# Student Attendance
ABSENT = "Absent"
PRESENT = "Present"
ATTENDANCE_CHOICES = (
    (ABSENT, "Absent"),
    (PRESENT, "Present"),
)

# Kids Model
AGE_BRACKET_CHOICES = (
        ("6-9", "6-9"),
        ("10-14", "10-14")
      )


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
COMMUNITY_TYPE = (
        ("Webinars", "Webinars"),
        ("Meetups", "Meetups")
    )


# HowItWork Models
HOW_IT_WORK_CLASS_TYPE = (
        ("Physical Class", "Physical Class"),
        ("Virtual Class", "Virtual Class"),
    )


# JobCategory Model
EXPERIENCE_LEVEL = (
        ("Experienced", "Experienced"),
        ("Intermediate", "Intermediate"),
        ("Internship", "Internship"),
    )

JOB_TYPE = (
    ("Full-time", "Full-time"),
    ("Part-time", "Part-time"),
    ("Contractor", "Contractor"),
)

JOB_LOCATION = (("On-site", "On-site"), ("Hybrid", "Hybrid"), ("Remote", "Remote"))


# Job Model
STATUS = (
        ("Draft", "Draft"), 
        ("Published", "Published")
    )


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
PROGRAM_TYPE_CHOICES = (
    ("Onsite", "Onsite"), 
    ("Virtual", "Virtual")
    )

# Blog Model
OPTIONS = (("published", "Published"), ("draft", "Draft"))