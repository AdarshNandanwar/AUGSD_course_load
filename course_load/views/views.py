import json
import os
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
 
from course_load.utils import get_department_list, get_department_cdc_list, get_department_elective_list, get_department_instructor_list, get_instructor_list, get_department_phd_student_list
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from course_load.models import Course, Instructor, CourseInstructor, CourseAccessRequested
from django.conf import settings

from django.shortcuts import get_object_or_404

import csv
from django.http import HttpResponse

from django.views import View
from course_load.forms import *

# Only for testing
from django.views.decorators.csrf import csrf_exempt

@method_decorator(login_required, name='dispatch')
class DashboardView(generic.TemplateView):
    template_name = 'admin/admin-page.html'
    index_file_path = os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            context = {
                'comment_files': []
            }
            department_list = get_department_list()
            for dept in department_list:
                department = Department.objects.get(code = dept)
                context['comment_files'].append({
                    'name': department.name,
                    'comment_file': department.comment_file
                })
            return render(request, self.template_name, context)
        else:
            try:
                with open(self.index_file_path) as f:
                    return HttpResponse(f.read())
            except FileNotFoundError:
                logging.exception('Production build of app not found')
                return HttpResponse(
                    """
                    This URL is only used when you have built the production
                    version of the app. Visit http://localhost:3000/ instead after
                    running `yarn start` on the frontend/ directory
                    """,
                    status=501,
                )

@method_decorator(login_required, name='dispatch')
class AddCourse(View):
    form_class = AddCourseForm
    initial = {'key': 'value'}
    template_name = 'admin/add-course.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                form = self.form_class(request.POST)
                if form.is_valid():
                    course, created = Course.objects.get_or_create(
                        code = form.cleaned_data['code'], 
                        name = form.cleaned_data['name'], 
                        department = form.cleaned_data['department'], 
                        course_type = form.cleaned_data['course_type'], 
                    )
                    return HttpResponseRedirect('/course-load/dashboard')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class AddInstructor(View):
    form_class = AddInstructorForm
    initial = {'key': 'value'}
    template_name = 'admin/add-instructor.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                form = self.form_class(request.POST)
                if form.is_valid():
                    instructor, created = Instructor.objects.get_or_create(
                        psrn_or_id = form.cleaned_data['psrn_or_id'], 
                        name = form.cleaned_data['name'], 
                        department = form.cleaned_data['department'], 
                        instructor_type = form.cleaned_data['instructor_type'], 
                    )
                    return HttpResponseRedirect('/course-load/dashboard')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class UpdateCourse(View):
    form_class = UpdateCourseForm
    initial = {'key': 'value'}
    template_name = 'admin/update-course.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                course = Course.objects.get(code = request.POST['old_code'])
            except Instructor.DoesNotExist:
                form = self.form_class(initial=self.initial)
                return render(request, self.template_name, {'form': form})
            course_original = Course.objects.get(code = request.POST['old_code'])
            form = self.form_class(request.POST, instance = course)
            course.delete()
            try:
                if form.is_valid():
                    form.code = form.cleaned_data['code'], 
                    form.name = form.cleaned_data['name'], 
                    form.department = Department.objects.get(code = form.cleaned_data['department']), 
                    form.course_type = form.cleaned_data['course_type'], 
                    form.save()
                    return HttpResponseRedirect('/course-load/dashboard')
            except Exception as e:
                course_original.save()
                print(e)
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class UpdateInstructor(View):
    form_class = UpdateInstructorForm
    initial = {'key': 'value'}
    template_name = 'admin/update-instructor.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                instructor = Instructor.objects.get(psrn_or_id = request.POST['old_psrn_or_id'])
            except Instructor.DoesNotExist:
                form = self.form_class(initial=self.initial)
                return render(request, self.template_name, {'form': form})
            instructor_original = Instructor.objects.get(psrn_or_id = request.POST['old_psrn_or_id'])
            form = self.form_class(request.POST, instance = instructor)
            instructor.delete()
            try:
                if form.is_valid():
                    form.psrn_or_id = form.cleaned_data['psrn_or_id'], 
                    form.name = form.cleaned_data['name'], 
                    form.department = Department.objects.get(code = form.cleaned_data['department']), 
                    form.instructor_type = form.cleaned_data['instructor_type'], 
                    form.save()
                    return HttpResponseRedirect('/course-load/dashboard')
            except Exception as e:
                instructor_original.save()
                print(e)
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@login_required
def get_data(request, *args, **kwargs):
    response = {}
    dept = request.user.userprofile.department
    try:
        requested_cdc_list = Course.objects.filter(
            code__in = CourseAccessRequested.objects.filter(department = dept, course__course_type = 'C').values('course'),
            course_type = 'C'
        )
        requested_elective_list = Course.objects.filter(
            code__in = CourseAccessRequested.objects.filter(department = dept, course__course_type = 'E').values('course'),
            course_type = 'E'
        )
        department_cdc_list = Course.objects.filter(department = dept, course_type = 'C')
        department_elective_list = Course.objects.filter(department = dept, course_type = 'E')
        other_cdc_list = Course.objects.filter(course_type = 'C').difference(department_cdc_list).difference(requested_cdc_list)
        other_elective_list = Course.objects.filter(course_type = 'E').difference(department_elective_list).difference(requested_elective_list)
        faculty_list = Instructor.objects.filter(instructor_type = 'F') | Instructor.objects.filter(department = dept, instructor_type = 'S')
        response['data'] = {
            'department_cdc_list': list(department_cdc_list.values('name', 'code')),
            'department_elective_list': list(department_elective_list.values('name', 'code')),
            'requested_cdc_list': list(requested_cdc_list.values('name', 'code')),
            'requested_elective_list': list(requested_elective_list.values('name', 'code')),
            'other_cdc_list': list(other_cdc_list.values('name', 'code')),
            'other_elective_list': list(other_elective_list.values('name', 'code')),
            'faculty_list': list(faculty_list.values('name', 'psrn_or_id')),
        }
        response['error'] = False
        response['message'] = 'success'
    except Exception as e:
        response['data'] = {}
        response['error'] = True
        response['message'] = str(e)
    return JsonResponse(response, safe=False)

@login_required
# @csrf_exempt
def get_course_data(request, *args, **kwargs):
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        course = Course.objects.get(code = data['course_code'], course_type = data['course_type'])
        l_entry_list = CourseInstructor.objects.filter(section_type = 'L', course = course).values('instructor')
        l_instructor_list = []
        for entry in l_entry_list:
            instructor = Instructor.objects.get(psrn_or_id = entry['instructor'])
            l_instructor_list.append({
                'name': instructor.name,
                'psrn_or_id': instructor.psrn_or_id,
            })
        t_entry_list = CourseInstructor.objects.filter(section_type = 'T', course = course).values('instructor')
        t_instructor_list = []
        for entry in t_entry_list:
            instructor = Instructor.objects.get(psrn_or_id = entry['instructor'])
            t_instructor_list.append({
                'name': instructor.name,
                'psrn_or_id': instructor.psrn_or_id,
            })
        p_entry_list = CourseInstructor.objects.filter(section_type = 'P', course = course).values('instructor')
        p_instructor_list = []
        for entry in p_entry_list:
            instructor = Instructor.objects.get(psrn_or_id = entry['instructor'])
            p_instructor_list.append({
                'name': instructor.name,
                'psrn_or_id': instructor.psrn_or_id,
            })
        response['data'] = {
            'course_code': course.code,
            'course_type': course.course_type,
            'l_section_count': course.l_section_count,
            't_section_count': course.t_section_count,
            'p_section_count': course.p_section_count,
            'l_count': course.l_count,
            't_count': course.t_count,
            'p_count': course.p_count,
            'student_count': course.student_count,
            'max_strength': course.max_strength,
            'l': l_instructor_list,
            't': t_instructor_list,
            'p': p_instructor_list,
        }
        if course.ic:
            response['data']['ic'] = {
                'name': course.ic.name,
                'psrn_or_id': course.ic.psrn_or_id,
            }
        else:
            response['data']['ic'] = {
                'name': '',
                'psrn_or_id': '',
            }
            
        response['error'] = False
        response['message'] = 'success'
    except Exception as e:
        print(e)
        response['error'] = True
        response['message'] = str(e)
    return JsonResponse(response, safe=False)

@login_required
# @csrf_exempt
def request_course_access(request, *args, **kwargs):
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        course = Course.objects.get(code = data['course_code'], course_type = data['course_type'])
        course, created = CourseAccessRequested.objects.get_or_create(course = course, department = request.user.userprofile.department)
        
        response['error'] = False
        response['message'] = 'success'
    except Exception as e:
        print(e)
        response['error'] = True
        response['message'] = str(e)
    return JsonResponse(response, safe=False)

@login_required
# @csrf_exempt
def submit_data(request, *args, **kwargs):
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        course = Course.objects.filter(code = data['course_code'], course_type = data['course_type'])
        course.update(
            l_section_count = data['l_section_count'],
            t_section_count = data['t_section_count'],
            p_section_count = data['p_section_count'],
            l_count = data['l_count'],
            t_count = data['t_count'],
            p_count = data['p_count'],
            student_count = data['student_count'],
            max_strength = data['max_strength'],
            ic = Instructor.objects.get(psrn_or_id = data['ic']),
        )

        CourseInstructor.objects.filter(course = course.first()).delete()
        l = data['l']
        t = data['t']
        p = data['p']
        for psrn_or_id in l:
            instructor = Instructor.objects.get(psrn_or_id = psrn_or_id)
            CourseInstructor.objects.create(
                section_type = 'L',
                course = course.first(),
                instructor = instructor
            )
        for psrn_or_id in t:
            instructor = Instructor.objects.get(psrn_or_id = psrn_or_id)
            CourseInstructor.objects.create(
                section_type = 'T',
                course = course.first(),
                instructor = instructor
            )
        for psrn_or_id in p:
            instructor = Instructor.objects.get(psrn_or_id = psrn_or_id)
            CourseInstructor.objects.create(
                section_type = 'P',
                course = course.first(),
                instructor = instructor
            )

        response['error'] = False
        response['message'] = 'success'
    except Exception as e:
        print(e)
        response['error'] = True
        response['message'] = str(e)
    return JsonResponse(response, safe=False)

@method_decorator(login_required, name='dispatch')
class AddComment(View):
    form_class = CommentFileForm
    initial = {'key': 'value'}
    template_name = 'course_load/add-comment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=request.user.userprofile.department.__dict__)
        return render(request, self.template_name, {
            'form': form,
            'uploaded_file': request.user.userprofile.department.comment_file})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            request.user.userprofile.department.comment_file = request.FILES['comment_file']
            request.user.userprofile.department.save()
            return HttpResponseRedirect('/course-load/dashboard')
        return render(request, self.template_name, {'form': form})

@login_required
def download_course_wise(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Course Load course-wise.csv"'
    writer = csv.writer(response)

    writer.writerow(['Course Code', 'Course Name', 'IC'])
    writer.writerow(['Instructor Name', 'L', 'T', 'P'])
    course_list = CourseInstructor.objects.filter().values('course').distinct()
    for course in course_list:
        course = Course.objects.get(code = course['course'])
        if request.user.is_superuser or course.department == request.user.userprofile.department:
            writer.writerow([])
            writer.writerow([])
            writer.writerow([course.code, course.name, course.ic])
            writer.writerow([])
            instructor_list = CourseInstructor.objects.filter(course = course).values('instructor').distinct()
            for instructor in instructor_list:
                instructor = Instructor.objects.get(psrn_or_id = instructor['instructor'])
                l_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'L').count()
                t_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'T').count()
                p_count = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'P').count()
                writer.writerow([instructor.name, l_count, t_count, p_count])    
    return response

@login_required
def download_instructor_wise(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Course Load instructor-wise.csv"'
    writer = csv.writer(response)

    writer.writerow(['Instructor Name', 'Deptartment'])
    writer.writerow(['Course Code', 'Course Name', 'L', 'T', 'P', 'Role'])
    instructor_list = None
    if request.user.is_superuser:
        instructor_list = CourseInstructor.objects.filter().values('instructor').distinct()
    else:
        instructor_list = CourseInstructor.objects.filter(course__department = request.user.userprofile.department).values('instructor').distinct()
    for instructor in instructor_list:
        writer.writerow([])
        writer.writerow([])
        instructor = Instructor.objects.get(psrn_or_id = instructor['instructor'])
        writer.writerow([instructor.name, instructor.department])
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
            writer.writerow([course.code, course.name, l_count, t_count, p_count, role])
    return response