from django import forms
from .models import Department, Course, Instructor, UserProfile
from .models import PortalSettings

class TogglePortalForm(forms.ModelForm):
    class Meta:  
        model = PortalSettings  
        fields = ['is_portal_active', 'disable_all_courses']
        labels = {
            "is_portal_active": "Activate portal",
            "disable_all_courses": "Disable all courses"
        }

class CommentFileForm(forms.ModelForm):
    class Meta:  
        model = Department  
        fields = ['comment_file']
        labels = {
            "comment_file": "Comment file",
        }

class InitialDataFileForm(forms.ModelForm):
    class Meta:  
        model = UserProfile  
        fields = ['initial_data_file']
        labels = {
            "initial_data_file": "Data file",
        }

class PastCourseStrengthFileForm(forms.ModelForm):
    class Meta:  
        model = UserProfile  
        fields = ['past_course_strength_data_file']
        labels = {
            "past_course_strength_data_file": "Data File (in correct format)",
        }

class AddCourseForm(forms.ModelForm):
    merge_with = forms.ModelChoiceField(queryset=Course.objects.order_by('code'), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.order_by('name'), required=True)
    class Meta:  
        model = Course  
        fields = ['code', 'name', 'comcode', 'department', 'course_type', 'merge_with', 'past_course_strength', 'sem', 'lpu']
        labels = {
            'code': 'Course number',
            'name': 'Course title',
            'sem': 'Semesters',
            'lpu': 'LPU'
        }

class AddCourseBulkForm(forms.ModelForm):
    class Meta:  
        model = UserProfile  
        fields = ['course_file']
        labels = {
            "course_file": "Data file",
        }

class AddInstructorForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.order_by('name'), required=True)
    class Meta:  
        model = Instructor  
        fields = ['psrn_or_id', 'name', 'department', 'instructor_type']
        labels = {
            'psrn_or_id': 'PSRN/ID'
        }

class AddInstructorBulkForm(forms.ModelForm):
    class Meta:  
        model = UserProfile  
        fields = ['instructor_file']
        labels = {
            "instructor_file": "Data file",
        }

class UpdateCourseForm(forms.ModelForm):
    merge_with = forms.ModelChoiceField(queryset=Course.objects.order_by('code'), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.order_by('name'), required=True)
    class Meta:  
        model = Course  
        fields = ['code', 'name', 'comcode', 'department', 'course_type', 'merge_with', 'past_course_strength', 'sem', 'lpu']
        labels = {
            'code': 'Course number',
            'name': 'Course title',
            'sem': 'Semesters',
            'lpu': 'LPU'
        }

class UpdateInstructorForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.order_by('name'), required=True)
    class Meta:  
        model = Instructor  
        fields = ['psrn_or_id', 'name', 'department', 'instructor_type']
        labels = {
            'psrn_or_id': 'PSRN/ID'
        }

class DeleteCourseForm(forms.ModelForm):
    class Meta:  
        model = Course  
        fields = ['code']
        labels = {
            'code': 'Course number',
        }

class DeleteInstructorForm(forms.ModelForm):
    class Meta:  
        model = Instructor  
        fields = ['psrn_or_id']
        labels = {
            'psrn_or_id': 'PSRN/ID'
        }