import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from course_load.models import Course, Instructor, CourseInstructor, CourseAccessRequested

@login_required
def download_course_wise(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Course Load course-wise.csv"'
    writer = csv.writer(response)

    writer.writerow(['Course Code', 'Course Name', 'Max strength per section: ', 'L', 'T', 'P'])
    writer.writerow(['PSRN/ID', 'Instructor Name','', 'L', 'T', 'P', 'Status'])
    course_list = CourseInstructor.objects.filter().values('course').distinct()
    for course in course_list:
        course = Course.objects.get(code = course['course'])
        if request.user.is_superuser or course.department == request.user.userprofile.department or CourseAccessRequested.objects.filter(course = course, department = request.user.userprofile.department).exists():
            writer.writerow([])
            writer.writerow([])
            writer.writerow([course.code, course.name, '', course.max_strength_per_l, course.max_strength_per_t, course.max_strength_per_p])
            writer.writerow([])
            ic = course.ic
            l_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'L').count()
            t_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'T').count()
            p_count = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'P').count()
            writer.writerow([ic.name, '', l_count, t_count, p_count, 'IC'])
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

    writer.writerow(['PSRN/ID', 'Instructor Name', 'Deptartment'])
    writer.writerow(['Course Code', 'Course Name', '', 'L', 'T', 'P', 'Status'])
    instructor_list = None
    if request.user.is_superuser:
        instructor_list = CourseInstructor.objects.filter().values('instructor').distinct()
    else:
        instructor_list = CourseInstructor.objects.filter(course__department = request.user.userprofile.department).values('instructor').distinct()
    for instructor in instructor_list:
        writer.writerow([])
        writer.writerow([])
        instructor = Instructor.objects.get(psrn_or_id = instructor['instructor'])
        writer.writerow([instructor.psrn_or_id, instructor.name, instructor.department])
        writer.writerow([])
        course_list = None
        if request.user.is_superuser:
            course_list = CourseInstructor.objects.filter(instructor = instructor).values('course').distinct()
        else:
            course_list = CourseInstructor.objects.filter(instructor = instructor, course__department = request.user.userprofile.department).values('course').distinct()
        for course in course_list:
            course = Course.objects.get(code = course['course'])
            l_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'L').count()
            t_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'T').count()
            p_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'P').count()
            role = 'I'
            if course.ic == instructor:
                role = 'IC'
            writer.writerow([course.code, course.name, '', l_count, t_count, p_count, role])
    return response