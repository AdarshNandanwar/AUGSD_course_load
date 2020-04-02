import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AUGSD_time_table_project.settings')

import django

django.setup()
from course_load.models import *
from course_load.utils import get_department_list, get_department_cdc_list, get_department_elective_list, get_department_instructor_list, get_department_phd_student_list

from django.contrib.auth.models import User

def create_super_user():
    try:
        (super_user, created) = User.objects.get_or_create(username="admin", is_superuser=True)
        super_user.set_password('adminpassword')
        super_user.is_staff = True
        super_user.is_admin = True
        super_user.is_superuser = True
        super_user.save()
    except Exception as e:
        print(str(e))
        print("Error occurred while creating super user")

def create_user_profile():
    try:
        dept_list = get_department_list()
        for i in dept_list:
            (mUser, created) = User.objects.get_or_create(username = 'hod_'+i)
            mUser.set_password('password_'+i)
            mUser.save()
            (dept, created) = Department.objects.get_or_create(code = i, name = i)
            dept.save()
            UserProfile.objects.create(user = mUser, department = dept)
            
    except Exception as e:
        print(str(e))
        print("Error creating user profiles")

def create_instructor():
    try:
        dept_list = get_department_list()
        for i in dept_list:
            dept = Department.objects.get(code = i)

            department_instructor_list = get_department_instructor_list(i)
            for instructor in department_instructor_list:
                print(instructor[0], ', ', instructor[1])
                try:
                    Instructor.objects.create(psrn_or_id = instructor[1], name = instructor[0], instructor_type = 'F', department = dept)
                except Exception as e:
                    print(instructor[0], ', ', instructor[1], " skipped as this instructor is already in db")
                
            # Error: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
            department_phd_student_list = get_department_phd_student_list(i)
            for phd_student in department_phd_student_list:
                print(phd_student[0], ', ', phd_student[1])
                try:
                    Instructor.objects.create(psrn_or_id = phd_student[1], name = phd_student[0], instructor_type = 'S', department = dept)
                except Exception as e:
                    print(instructor[0], ', ', instructor[1], " skipped as this phd scholar is already in db")

    except Exception as e:
        print(str(e))
        print("Error creating instructors")

def create_course():
    try:
        dept_list = get_department_list()
        for i in dept_list:
            dept = Department.objects.get(code = i)

            department_cdc_list = get_department_cdc_list(i)
            for cdc in department_cdc_list:
                print(cdc[0], ', ', cdc[1])
                try:
                    Course.objects.create(code = cdc[0], name = cdc[1], course_type = 'C', department = dept)
                except Exception as e:
                    print(cdc[0], ', ', cdc[1], " skipped as this cdc is already in db")
                
            department_elective_list = get_department_elective_list(i)
            for elective in department_elective_list:
                print(cdc[0], ', ', cdc[1])
                try:
                    Course.objects.create(code = elective[0], name = elective[1], course_type = 'E', department = dept)
                except Exception as e:
                    print(cdc[0], ', ', cdc[1], " skipped as this elective is already in db as a cdc")

    except Exception as e:
        print(str(e))
        print("Error creating courses")

if __name__ == '__main__':

    print("Clearing database")
    User.objects.all().delete()
    Department.objects.all().delete()
    UserProfile.objects.all().delete()
    Instructor.objects.all().delete()
    Course.objects.all().delete()
    CourseInstructor.objects.all().delete()
    CourseAccessRequested.objects.all().delete()

    print("Creating superuser")
    create_super_user()

    print("Creating departments and users")
    create_user_profile()

    print("Creating instructors")
    create_instructor()

    print("Creating courses")
    create_course()

    print("Done!")