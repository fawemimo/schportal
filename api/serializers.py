from rest_framework import serializers
from .models import *


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title']


class AddCourseSerializer(serializers.ModelSerializer):
    coursecategory_id = serializers.IntegerField()

    class Meta:
        model = Course
        fields = ['id', 'card_title', 'title', 'description', 'course_code',
                  'tech_subs', 'audience', 'coursecategory_id']

    def validate_coursecategory_id(self, value):
        if not CourseCategory.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'Invalid Course Category ID supplied')
        return value

    def create(self, validated_data):
        course = Course(**validated_data)
        course.save()
        return course


class CourseSerializer(serializers.ModelSerializer):
    coursecategory = CourseCategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'card_title', 'title', 'description', 'course_code',
                  'tech_subs', 'audience', 'coursecategory']


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
        fields = ['id', 'course', 'teacher', 'fee', 'discounted_fee',
                  'startdate', 'duration', 'timing']


class AddScheduleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()

    class Meta:
        model = Schedule
        fields = ['id', 'course_id', 'teacher_id', 'fee', 'discounted_fee',
                  'startdate', 'duration', 'timing']


class TopBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBar
        fields = ['id', 'title', 'bar_src']


class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainBanner
        fields = ['id', 'title', 'banner_src']


class SectionBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionBanner
        fields = ['id', 'title', 'banner_src']


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
