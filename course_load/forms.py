from django import forms
from .models import Department, Course, Instructor, UserProfile

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

class AddCourseForm(forms.ModelForm):
    class Meta:  
        model = Course  
        fields = ['code', 'name', 'comcode', 'department', 'course_type']
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
        fields = ['code', 'name', 'comcode', 'department', 'course_type']
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