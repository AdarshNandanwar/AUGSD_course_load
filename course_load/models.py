from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length = 100, null = False)
    comment_file = models.FileField(null = True, blank = False)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    psrn_or_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length = 100, null = False)
    department = models.ForeignKey(Department, default=None, on_delete=models.CASCADE)
    INSTRUCTOR_TYPES = (
        ('F', 'Faculty'),
        ('S', 'PHD Student')
    )
    instructor_type = models.CharField(max_length=1, choices=INSTRUCTOR_TYPES, null = False)

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=10, primary_key = True)
    # code = models.CharField(max_length=10, null = False)
    name = models.CharField(max_length = 100, null = False)
    l_section_count = models.IntegerField(default=0)
    t_section_count = models.IntegerField(default=0)
    p_section_count = models.IntegerField(default=0)
    l_count = models.IntegerField(default=0)
    t_count = models.IntegerField(default=0)
    p_count = models.IntegerField(default=0)
    max_strength_per_l = models.IntegerField(default=0)
    max_strength_per_t = models.IntegerField(default=0)
    max_strength_per_p = models.IntegerField(default=0)
    ic = models.ForeignKey(Instructor, default=None, on_delete=models.CASCADE, null = True)
    department = models.ForeignKey(Department, default=None, on_delete=models.CASCADE)
    COURSE_TYPES = (
        ('C', 'CDC'),
        ('E', 'Elective')
    )
    course_type = models.CharField(max_length=1, choices=COURSE_TYPES, null = False)

    # class Meta:
    #     unique_together = ['code', 'course_type']]

    def __str__(self):
        return self.name

class CourseInstructor(models.Model):
    SECTION_TYPES = (
        ('L', 'Lecture'),
        ('T', 'Tutorial'),
        ('P', 'Practical'),
        ('I', 'Independent'),
    )
    section_type = models.CharField(max_length=1, choices=SECTION_TYPES, null = False)
    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, default=None, on_delete=models.CASCADE)

class CourseAccessRequested(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=False, default=None, on_delete=models.CASCADE)
