from django import forms
from .models import Department, Course, Instructor, UserProfile
from .models import PortalSettings

class TogglePortalForm(forms.ModelForm):
    class Meta:  
        model = PortalSettings  
        fields = ['is_portal_active']
        labels = {
            "is_portal_active": "Activate portal",
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
            "initial_data_file": "Data File",
        }

class PastCourseStrengthFileForm(forms.ModelForm):
    class Meta:  
        model = UserProfile  
        fields = ['past_course_strength_data_file']
        labels = {
            "past_course_strength_data_file": "Data File (in correct format)",
        }

class AddCourseForm(forms.ModelForm):
    class Meta:  
        model = Course  
        fields = ['code', 'name', 'comcode', 'department', 'course_type', 'merge_with']
        labels = {
            'code': 'Course number',
            'name': 'Course title'
        }

class AddInstructorForm(forms.ModelForm):
    class Meta:  
        model = Instructor  
        fields = ['psrn_or_id', 'name', 'department', 'instructor_type']
        labels = {
            'psrn_or_id': 'PSRN/ID'
        }

class UpdateCourseForm(forms.ModelForm):
    class Meta:  
        model = Course  
        fields = ['code', 'name', 'comcode', 'department', 'course_type', 'merge_with']
        labels = {
            'code': 'Course number',
            'name': 'Course title'
        }

class UpdateInstructorForm(forms.ModelForm):
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