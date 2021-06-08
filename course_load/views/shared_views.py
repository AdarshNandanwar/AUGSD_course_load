import csv
import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from course_load.models import Course, Instructor, CourseInstructor, CourseAccessRequested
from course_load.utils import get_equivalent_course_info

@login_required
def download_course_wise(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Course Load course-wise.csv"'
    writer = csv.writer(response)

    writer.writerow(['Course number', 'Course title', 'Max strength per section: ', 'L', 'T', 'P'])
    writer.writerow(['PSRN/ID', 'Instructor name','', 'L', 'T', 'P', 'Role'])
    printed_set = set()
    current_month = datetime.datetime.now().month
    current_sem = 'sem2' if (current_month >= 11 or current_month < 4) else 'sem1'
    course_list = Course.objects.filter(enable = True).filter(Q(sem = 'sem12')|Q(sem = current_sem)).values('code').distinct().order_by('code')
    for course in course_list:
        course = Course.objects.get(code = course['code'])
        if request.user.is_superuser or course.department == request.user.userprofile.department or CourseAccessRequested.objects.filter(course = course, department = request.user.userprofile.department).exists():
            if course.code in printed_set:
                continue
            equivalent_course_list = get_equivalent_course_info(course.code)
            for i in equivalent_course_list:
                printed_set.add(i['code'])
            writer.writerow([])
            writer.writerow([])
            if len(equivalent_course_list) == 1:
                writer.writerow([course.code, course.name, '', course.max_strength_per_l, course.max_strength_per_t, course.max_strength_per_p])
            else:
                equivalent_course_list = sorted(equivalent_course_list, key = lambda i: i['code'])
                combined_code = equivalent_course_list[0]['code']
                for i in range(1, len(equivalent_course_list)):
                    combined_code = combined_code+' / '+equivalent_course_list[i]['code']
                writer.writerow([combined_code, course.name, '', course.max_strength_per_l, course.max_strength_per_t, course.max_strength_per_p])
            writer.writerow([])
            ic = course.ic
            l_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'L').count()
            t_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'T').count()
            p_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'P').count()
            writer.writerow([ic.psrn_or_id, ic.name, '', l_count, t_count, p_count, 'IC'])
            instructor_list = CourseInstructor.objects.filter(course = course).values('instructor').distinct().order_by('instructor__instructor_type', 'instructor')
            for instructor in instructor_list:
                if instructor['instructor'] == ic.psrn_or_id:
                    continue
                instructor = Instructor.objects.get(psrn_or_id = instructor['instructor'])
                l_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'L').count()
                t_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'T').count()
                p_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'P').count()
                writer.writerow([instructor.psrn_or_id, instructor.name, '', l_count, t_count, p_count, 'I'])    
    return response

@login_required
def download_instructor_wise(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Course Load instructor-wise.csv"'
    writer = csv.writer(response)

    writer.writerow(['PSRN/ID', 'Instructor name', 'Deptartment'])
    writer.writerow(['Course number', 'Course title', '', 'L', 'T', 'P', 'Role'])
    current_month = datetime.datetime.now().month
    current_sem = 'sem2' if (current_month >= 11 or current_month < 4) else 'sem1'
    instructor_list = None
    if request.user.is_superuser:
        instructor_list_1 = list(CourseInstructor.objects.filter(course__enable = True).filter(Q(course__sem = 'sem12')|Q(course__sem = current_sem)).values_list('instructor', flat=True).distinct())
        instructor_list_2 = list(Course.objects.filter(enable = True).filter(Q(sem = 'sem12')|Q(sem = current_sem)).values_list('ic', flat=True).distinct())
        instructor_list = instructor_list_1 + instructor_list_2
        instructor_list = list(set(instructor_list))
    else:
        instructor_list_1 = list(CourseInstructor.objects.filter(course__enable = True, instructor__department = request.user.userprofile.department).filter(Q(course__sem = 'sem12')|Q(course__sem = current_sem)).values_list('instructor', flat=True).distinct())
        instructor_list_2 = list(Course.objects.filter(enable = True, ic__department = request.user.userprofile.department).filter(Q(sem = 'sem12')|Q(sem = current_sem)).values_list('ic', flat=True).distinct())
        instructor_list = instructor_list_1 + instructor_list_2
        instructor_list = list(set(instructor_list))
    instructor_list = Instructor.objects.filter(psrn_or_id__in = instructor_list).order_by('department', 'instructor_type', 'psrn_or_id')
    for instructor in instructor_list:
        writer.writerow([])
        writer.writerow([])
        writer.writerow([instructor.psrn_or_id, instructor.name, instructor.department])
        writer.writerow([])
        course_list_1 = list(CourseInstructor.objects.filter(course__enable = True, instructor = instructor).filter(Q(course__sem = 'sem12')|Q(course__sem = current_sem)).values_list('course', flat=True).distinct())
        course_list_2 = list(Course.objects.filter(enable = True, ic = instructor).filter(Q(sem = 'sem12')|Q(sem = current_sem)).values_list('code', flat=True).distinct())
        course_list = course_list_1 + course_list_2
        course_list = list(set(course_list))
        printed_set = set()
        for course in course_list:
            course = Course.objects.get(code = course)
            if course.code in printed_set:
                continue
            equivalent_course_list = get_equivalent_course_info(course.code)
            for i in equivalent_course_list:
                printed_set.add(i['code'])
            l_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'L').count()
            t_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'T').count()
            p_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'P').count()
            role = 'I'
            if course.ic == instructor:
                role = 'IC'
            if len(equivalent_course_list) == 1:
                writer.writerow([course.code, course.name, '', l_count, t_count, p_count, role])
            else:
                combined_code = equivalent_course_list[0]['code']
                for i in range(1, len(equivalent_course_list)):
                    combined_code = combined_code+' / '+equivalent_course_list[i]['code']
                writer.writerow([combined_code, course.name, '', l_count, t_count, p_count, role])
    return response