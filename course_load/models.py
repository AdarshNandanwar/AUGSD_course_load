from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PortalSettings(models.Model):
    is_portal_active = models.BooleanField(default=False)

    def __str__(self):
        return "settings"

class Department(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length = 100, null = False)
    comment_file = models.FileField(null = True, blank = False)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, default=None, on_delete=models.CASCADE, null=True)
    initial_data_file = models.FileField(null = True, blank = False)
    past_course_strength_data_file = models.FileField(null = True, blank = False)

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    psrn_or_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length = 100, null = False)
    department = models.ForeignKey(Department, default=None, on_delete=models.CASCADE)
    INSTRUCTOR_TYPES = (
        ('F', 'Faculty'),
        ('S', 'PHD Student'),
        ('M', 'ME Student')
    )
    instructor_type = models.CharField(max_length=1, choices=INSTRUCTOR_TYPES, null = False)
    system_id = models.CharField(max_length = 15, null = True, blank = True)

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=20, primary_key = True)
    comcode = models.IntegerField()
    name = models.CharField(max_length = 100, null = False)
    l_count = models.IntegerField(default=0)
    t_count = models.IntegerField(default=0)
    p_count = models.IntegerField(default=0)
    max_strength_per_l = models.IntegerField(default=0)
    max_strength_per_t = models.IntegerField(default=0)
    max_strength_per_p = models.IntegerField(default=0)
    ic = models.ForeignKey(Instructor, default=None, on_delete=models.SET_DEFAULT, null = True)
    department = models.ForeignKey(Department, default=None, on_delete=models.CASCADE)
    COURSE_TYPES = (
        ('C', 'CDC'),
        ('E', 'Elective')
    )
    course_type = models.CharField(max_length=1, choices=COURSE_TYPES, null = False)
    merge_with = models.ForeignKey('self', default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)
    past_course_strength = models.IntegerField(null = True, blank = True)
    enable = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    SEM_TYPES = (
        ('sem1', 'Odd'),
        ('sem2', 'Even'),
        ('sem12', 'Both')
    )
    sem = models.CharField(max_length = 5, choices=SEM_TYPES, null = False, blank = False, default='sem12')
    lpu = models.CharField(max_length = 20, null = False, blank = False, default='0 0 0')

    def __str__(self):
        return self.code+' ('+self.name+')'

class CourseHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    l_count = models.IntegerField(default=0)
    t_count = models.IntegerField(default=0)
    p_count = models.IntegerField(default=0)
    max_strength_per_l = models.IntegerField(default=0)
    max_strength_per_t = models.IntegerField(default=0)
    max_strength_per_p = models.IntegerField(default=0)
    ic = models.ForeignKey(Instructor, default=None, on_delete=models.SET_DEFAULT, null = True)
    enable = models.BooleanField(default=False)

    def __str__(self):
        return self.course

class CourseInstructor(models.Model):
    SECTION_TYPES = (
        ('L', 'Lecture'),
        ('T', 'Tutorial'),
        ('P', 'Practical'),
        ('I', 'Independent'),
    )
    section_type = models.CharField(max_length=1, choices=SECTION_TYPES, null = False)
    section_number = models.IntegerField(blank = False, null = False)
    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, default=None, on_delete=models.CASCADE)

class CourseAccessRequested(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=False, default=None, on_delete=models.CASCADE)
