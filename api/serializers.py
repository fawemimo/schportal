from rest_framework import serializers
from .models import *
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title']


class AddCourseSerializer(serializers.ModelSerializer):
    coursecategory_id = serializers.IntegerField()

    class Meta:
        model = Course
        fields = [
            'id',
            'card_title',
            'title',
            'description',
            'course_code',
            'tech_subs',
            'audience',
            'coursecategory_id',
        ]

    def validate_coursecategory_id(self, value):
        if not CourseCategory.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Invalid Course Category ID supplied')
        return value

    def create(self, validated_data):
        course = Course(**validated_data)
        course.save()
        return course


class CourseSerializer(serializers.ModelSerializer):
    coursecategory = CourseCategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        lookup_field = 'slug'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        fields = [
            'id',
            'course',
            'registration_status',
            'teacher',
            'fee',
            'discounted_fee',
            'startdate',
            'duration',
            'timing',
        ]


class AddScheduleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()

    class Meta:
        model = Schedule
        fields = [
            'id',
            'course_id',
            'teacher_id',
            'fee',
            'discounted_fee',
            'startdate',
            'duration',
            'timing',
        ]


class TopBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBar
        fields = '__all__'


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = '__all__'


class SectionBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionBanner
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class TechIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechIcon
        fields = '__all__'


class FeaturedProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedProject
        fields = '__all__'


class ComponentDumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentDump
        fields = '__all__'


class NavLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavLink
        fields = '__all__'


class NavLinkItemSerializer(serializers.ModelSerializer):
    navlink = NavLinkSerializer()

    class Meta:
        model = NavLinkItem
        fields = ['id', 'item', 'item_url', 'navlink']


class AddNavLinkItemSerializer(serializers.ModelSerializer):
    # navlink_id = serializers.IntegerField()

    class Meta:
        model = NavLinkItem
        fields = ['id', 'item', 'item_url']

    def create(self, validated_data):
        navlinkid = self.context['navlink_id']
        return NavLinkItem.objects.create(navlink_id=navlinkid, **validated_data)


class ShortQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuiz
        fields = '__all__'


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'


class InterestedFormSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    class Meta:
        model = InterestedForm
        fields = ['id','course_id','full_name','email','mobile']

    def validate_course_id(self, value):
        if not Course.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Course ID does not exist')
        return value

    def create(self, validated_data):
        interestedform = InterestedForm(**validated_data)      
        interestedform.save()
        return interestedform




class EnrollBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('id', 'title', 'start_date', 'end_date')


class EnrollStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'student_id',
            'first_name',
            'last_name',
            'mobile_numbers',
            'email_addresses',
            'profile_pic',
        )


class EnrollCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title')


class EnrollmentSerializer(serializers.ModelSerializer):
    student = EnrollStudentSerializer(read_only=True)
    course = EnrollCourseSerializer(read_only=True)
    batch = EnrollBatchSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'batch', 'enrolled', 'training_date']


class AssignmentSerializer(serializers.ModelSerializer):
    batch = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'batch', 'name', 'assignment_file', 'date_posted')


class ResourceSerializer(serializers.ModelSerializer):
    resource_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Resource
        fields = ('id', 'resource_type', 'primer', 'cheat_sheat', 'published')


class ProjectSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ['id', 'student', 'name', 'project_docs', 'date_posted']


class CourseManualSerializer(serializers.ModelSerializer):
    course = EnrollCourseSerializer(many=True)

    class Meta:
        model = CourseManual
        fields = ['id', 'course', 'manual', 'date_posted']


class AddCourseCardSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        coursecard = Course(**validated_data)      
        coursecard.save()
        return coursecard    


class CourseCardSerializer(serializers.ModelSerializer):
    the_url = serializers.SerializerMethodField(read_only=True)
    fee = serializers.SerializerMethodField(source='schedule_set')
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'card_title', 'course_code', 'the_url', 'fee','card_thumb','audience','audience_description','frontpage_featured','active','slug','location_state','location_state_area']
        lookup_field = 'slug'

    def get_the_url(self, obj):
        return f'{obj.location_state}/{obj.location_state_area}/{obj.slug}'

    def get_fee(self, obj):
        return obj.schedule_set.only('id').values('fee').first()


class StudentAttendanceSerializer(serializers.ModelSerializer):
    batch = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    class Meta:
        model = StudentAttendance
        fields = ['id','student','batch','attendance_status','timestamp','attendance_comment','raise_warning']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','email','password','first_name','last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']        