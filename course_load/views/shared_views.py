import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from course_load.models import Course, Instructor, CourseInstructor, CourseAccessRequested

@login_required
def download_course_wise(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Course Load course-wise.csv"'
    writer = csv.writer(response)

    writer.writerow(['Course number', 'Course title', 'Max strength per section: ', 'L', 'T', 'P'])
    writer.writerow(['PSRN/ID', 'Instructor name','', 'L', 'T', 'P', 'Status'])
    # course_list = CourseInstructor.objects.filter().values('course').distinct()
    course_list = Course.objects.filter(ic__isnull = False).values('code').distinct()
    for course in course_list:
        course = Course.objects.get(code = course['code'])
        if request.user.is_superuser or course.department == request.user.userprofile.department or CourseAccessRequested.objects.filter(course = course, department = request.user.userprofile.department).exists():
            writer.writerow([])
            writer.writerow([])
            writer.writerow([course.code, course.name, '', course.max_strength_per_l, course.max_strength_per_t, course.max_strength_per_p])
            writer.writerow([])
            ic = course.ic
            l_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'L').count()
            t_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'T').count()
            p_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'P').count()
            writer.writerow([ic.psrn_or_id, ic.name, '', l_count, t_count, p_count, 'IC'])
            instructor_list = CourseInstructor.objects.filter(course = course).values('instructor').distinct()
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
    writer.writerow(['Course number', 'Course title', '', 'L', 'T', 'P', 'Status'])
    instructor_list = None
    if request.user.is_superuser:
        instructor_list_1 = list(CourseInstructor.objects.filter().values_list('instructor', flat=True).distinct())
        instructor_list_2 = list(Course.objects.filter(ic__isnull = False).values_list('ic', flat=True).distinct())
        instructor_list = instructor_list_1 + instructor_list_2
        instructor_list = list(set(instructor_list))
    else:
        instructor_list_1 = list(CourseInstructor.objects.filter(instructor__department = request.user.userprofile.department).values_list('instructor', flat=True).distinct())
        instructor_list_2 = list(Course.objects.filter(ic__isnull = False, ic__department = request.user.userprofile.department).values_list('ic', flat=True).distinct())
        instructor_list = instructor_list_1 + instructor_list_2
        instructor_list = list(set(instructor_list))
    for instructor in instructor_list:
        writer.writerow([])
        writer.writerow([])
        instructor = Instructor.objects.get(psrn_or_id = instructor)
        writer.writerow([instructor.psrn_or_id, instructor.name, instructor.department])
        writer.writerow([])
        course_list_1 = list(CourseInstructor.objects.filter(instructor = instructor).values_list('course', flat=True).distinct())
        course_list_2 = list(Course.objects.filter(ic = instructor).values_list('code', flat=True).distinct())
        course_list = course_list_1 + course_list_2
        course_list = list(set(course_list))
        for course in course_list:
            course = Course.objects.get(code = course)
            l_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'L').count()
            t_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'T').count()
            p_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'P').count()
            role = 'I'
            if course.ic == instructor:
                role = 'IC'
            writer.writerow([course.code, course.name, '', l_count, t_count, p_count, role])
    return response