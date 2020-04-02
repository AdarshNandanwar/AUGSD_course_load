import json
import os
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic, View

from course_load.forms import CommentFileForm
from course_load.models import Department, Course, Instructor, CourseInstructor, CourseAccessRequested
from course_load.utils import get_department_list

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
        faculty_list = Instructor.objects.filter(department = dept)
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
            'max_strength_per_l': course.max_strength_per_l,
            'max_strength_per_t': course.max_strength_per_t,
            'max_strength_per_p': course.max_strength_per_p,
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
            max_strength_per_l = data['max_strength_per_l'],
            max_strength_per_t = data['max_strength_per_t'],
            max_strength_per_p = data['max_strength_per_p'],
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