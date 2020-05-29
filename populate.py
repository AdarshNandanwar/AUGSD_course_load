import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AUGSD_time_table_project.settings')

import django

django.setup()
from course_load.models import *
from course_load.utils import get_department_list, get_department_cdc_list, get_department_elective_list, get_department_instructor_list, get_department_phd_student_list

from django.contrib.auth.models import User

def create_super_user():
    print("Creating superuser")
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

def create_user_profile(file):
    print("Creating departments and users")

    print("Creating admin user profile")
    UserProfile.objects.create(user = User.objects.filter(is_superuser=True).first())

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

def create_instructor(file):
    print("Creating instructors")
    try:
        dept_list = get_department_list()
        for i in dept_list:
            dept = Department.objects.get(code = i)

            department_instructor_list = get_department_instructor_list(i, file)
            for instructor in department_instructor_list:
                try:
                    Instructor.objects.create(psrn_or_id = instructor[1], name = instructor[0], instructor_type = 'F', department = dept)
                    # print('ADDED: ', instructor[1], ' [', instructor[0], ']')
                except Exception as e:
                    print('SKIPPED: ', instructor[1], ' [', instructor[0], "] instructor is already in db.")
                    pass
                
            department_phd_student_list = get_department_phd_student_list(i, file)
            for phd_student in department_phd_student_list:
                try:
                    Instructor.objects.create(psrn_or_id = phd_student[1], name = phd_student[0], instructor_type = 'S', department = dept)
                    # print('ADDED: ', phd_student[1], ' [', phd_student[0], ']')
                except Exception as e:
                    print('SKIPPED: ', phd_student[1], ' [', phd_student[0], "] phd scholar is already in db.")
                    pass

    except Exception as e:
        print(str(e))
        print("Error creating instructors")

def create_course(file):
    print("Creating courses")
    try:
        dept_list = get_department_list()
        for i in dept_list:
            dept = Department.objects.get(code = i)
            department_cdc_list = get_department_cdc_list(i, file)
            for cdc in department_cdc_list:
                parent_course = None
                if cdc[6] is not None:
                    parent_course = Course.objects.filter(code=cdc[6]).first()
                try:
                    Course.objects.create(
                        code = cdc[0], 
                        name = cdc[1], 
                        course_type = 'C', 
                        department = dept, 
                        l_count = cdc[2], 
                        t_count = cdc[3], 
                        p_count = cdc[4], 
                        comcode = cdc[5], 
                        merge_with = parent_course,
                    )
                    if cdc[6] is not None:
                        if parent_course is None:
                            print('NOTFOUND: ', 'Parent course ['+cdc[6]+'] of '+cdc[1]+' ['+cdc[0]+']')
                        else:
                            # print('FOUND: ', 'Parent course ['+cdc[6]+'] of '+cdc[1]+' ['+cdc[0]+']')
                            pass
                    # print('ADDED: ', cdc[0], ' [', cdc[1], ']')
                except Exception as e:
                    print('SKIPPED: ', cdc[0], ' [', cdc[1], "] cdc is already in db ("+str(e)+")")
                    pass
            department_elective_list = get_department_elective_list(i, file)
            for elective in department_elective_list:
                parent_course = None
                if elective[3] is not None:
                    parent_course = Course.objects.filter(code=elective[3]).first()
                try:
                    Course.objects.create(
                        code = elective[0], 
                        name = elective[1], 
                        course_type = 'E', 
                        department = dept, 
                        comcode = elective[2],
                        merge_with = parent_course,
                    )
                    if elective[3] is not None:
                        if parent_course is None:
                            print('NOTFOUND: ', 'Parent course ['+elective[3]+'] of '+elective[1]+' ['+elective[0]+']')
                        else:
                            # print('FOUND: ', 'Parent course ['+elective[3]+'] of '+elective[1]+' ['+elective[0]+']')
                            pass
                    # print('ADDED: ', elective[0], ' [', elective[1], ']')
                except Exception as e:
                    print('SKIPPED: ', elective[0], ' [', elective[1], "] elective is already in db. ("+str(e)+")")
                    pass

    except Exception as e:
        print(str(e))
        print("Error creating courses")

if __name__ == '__main__':

    print("Clearing database")
    
    AdminSettings.objects.all().delete()
    User.objects.all().delete()
    Department.objects.all().delete()
    UserProfile.objects.all().delete()
    Instructor.objects.all().delete()
    Course.objects.all().delete()
    CourseInstructor.objects.all().delete()
    CourseAccessRequested.objects.all().delete()

    file = 'data.xlsx'
    AdminSettings.objects.create()
    create_super_user()
    create_user_profile(file)
    create_instructor(file)
    create_course(file)

    print("Done!")

def populate_from_admin_data(file):
    print("Clearing database")
    Instructor.objects.all().delete()
    Course.objects.all().delete()
    CourseInstructor.objects.all().delete()
    CourseAccessRequested.objects.all().delete()
    create_instructor(file)
    create_course(file)
    print("Done!")