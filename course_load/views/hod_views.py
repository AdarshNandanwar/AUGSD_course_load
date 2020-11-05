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
from course_load.models import Department, Course, Instructor, CourseInstructor, CourseAccessRequested, CourseHistory, PortalSettings
from course_load.utils import get_department_list, get_equivalent_course_info

# Only for testing
from django.views.decorators.csrf import csrf_exempt

@method_decorator(login_required, name='dispatch')
class DashboardView(generic.TemplateView):
    template_name = 'admin/admin-page.html'
    closed_template_name = 'admin/closed.html'
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
                    'comment_file': department.comment_file,
                    'comment_file_url': department.comment_file.url if department.comment_file else '',
                })
            return render(request, self.template_name, context)
        else:

            if not PortalSettings.objects.filter().first().is_portal_active:
                return render(request, self.closed_template_name)

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
        faculty_list_1 = Instructor.objects.filter(department = dept, instructor_type = 'F')
        faculty_list_2 = Instructor.objects.filter(department = dept, instructor_type = 'S')
        faculty_list_3 = Instructor.objects.filter(department = dept, instructor_type = 'M')
        faculty_list_4 = Instructor.objects.filter(instructor_type = 'F').exclude(department = dept)

        department_cdc_list = list(department_cdc_list.values('name', 'code', 'enable', 'sem'))
        department_elective_list = list(department_elective_list.values('name', 'code', 'enable', 'sem'))
        requested_cdc_list = list(requested_cdc_list.values('name', 'code', 'enable', 'sem'))
        requested_elective_list = list(requested_elective_list.values('name', 'code', 'enable', 'sem'))

        other_cdc_list = list(other_cdc_list.values('name', 'code', 'sem'))
        other_elective_list = list(other_elective_list.values('name', 'code', 'sem'))
        faculty_list_1 = list(faculty_list_1.values('name', 'psrn_or_id'))
        faculty_list_2 = list(faculty_list_2.values('name', 'psrn_or_id'))
        faculty_list_3 = list(faculty_list_3.values('name', 'psrn_or_id'))
        faculty_list_4 = list(faculty_list_4.values('name', 'psrn_or_id'))
        faculty_list = faculty_list_1 + faculty_list_2 + faculty_list_3 + faculty_list_4
        response['data'] = {
            'department_cdc_list': department_cdc_list,
            'department_elective_list': department_elective_list,
            'requested_cdc_list': requested_cdc_list,
            'requested_elective_list': requested_elective_list,
            'other_cdc_list': other_cdc_list,
            'other_elective_list': other_elective_list,
            'faculty_list': faculty_list,
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
        l_entry_list = CourseInstructor.objects.filter(section_type = 'L', course = course).values('instructor', 'section_number')
        l_instructor_list = []
        for entry in l_entry_list:
            instructor = Instructor.objects.get(psrn_or_id = entry['instructor'])
            l_instructor_list.append({
                'name': instructor.name,
                'psrn_or_id': instructor.psrn_or_id,
                'section_number': entry['section_number'],
            })
        t_entry_list = CourseInstructor.objects.filter(section_type = 'T', course = course).values('instructor', 'section_number')
        t_instructor_list = []
        for entry in t_entry_list:
            instructor = Instructor.objects.get(psrn_or_id = entry['instructor'])
            t_instructor_list.append({
                'name': instructor.name,
                'psrn_or_id': instructor.psrn_or_id,
                'section_number': entry['section_number'],
            })
        p_entry_list = CourseInstructor.objects.filter(section_type = 'P', course = course).values('instructor', 'section_number')
        p_instructor_list = []
        for entry in p_entry_list:
            instructor = Instructor.objects.get(psrn_or_id = entry['instructor'])
            p_instructor_list.append({
                'name': instructor.name,
                'psrn_or_id': instructor.psrn_or_id,
                'section_number': entry['section_number'],
            })
        equivalent_course_list = get_equivalent_course_info(data['course_code'])
        response['data'] = {
            'enable': course.enable,
            'past_course_strength': course.past_course_strength,
            'course_code': course.code,
            'course_type': course.course_type,
            'l_count': course.l_count,
            't_count': course.t_count,
            'p_count': course.p_count,
            'max_strength_per_l': course.max_strength_per_l,
            'max_strength_per_t': course.max_strength_per_t,
            'max_strength_per_p': course.max_strength_per_p,
            'l': l_instructor_list,
            't': t_instructor_list,
            'p': p_instructor_list,
            'equivalent_course_list': equivalent_course_list,
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

        course_list = get_equivalent_course_info(data['course_code'])
        for course in course_list:
            course = Course.objects.filter(code = course['code']).first()
            course.enable = data['enable']
            course.past_course_strength = data['past_course_strength']
            course.l_count = data['l_count']
            course.t_count = data['t_count']
            course.p_count = data['p_count']
            course.max_strength_per_l = data['max_strength_per_l']
            course.max_strength_per_t = data['max_strength_per_t']
            course.max_strength_per_p = data['max_strength_per_p']
            course.ic = Instructor.objects.get(psrn_or_id = data['ic'])
            course.save(update_fields=['enable', 'past_course_strength', 'l_count', 't_count', 'p_count', 'max_strength_per_l', 'max_strength_per_t', 'max_strength_per_p', 'ic'])
            CourseHistory.objects.create(course = course, l_count = data['l_count'], t_count = data['t_count'], p_count = data['p_count'], max_strength_per_l = data['max_strength_per_l'], max_strength_per_t = data['max_strength_per_t'], max_strength_per_p = data['max_strength_per_p'], ic = course.ic, enable = data['enable'])

            CourseInstructor.objects.filter(course = course).delete()
            l = data['l']
            t = data['t']
            p = data['p']
            for entry in l:
                instructor = Instructor.objects.get(psrn_or_id = entry['psrn_or_id'])
                CourseInstructor.objects.create(
                    section_type = 'L',
                    course = course,
                    instructor = instructor,
                    section_number = entry['section_number']
                )
            for entry in t:
                instructor = Instructor.objects.get(psrn_or_id = entry['psrn_or_id'])
                CourseInstructor.objects.create(
                    section_type = 'T',
                    course = course,
                    instructor = instructor,
                    section_number = entry['section_number']
                )
            for entry in p:
                instructor = Instructor.objects.get(psrn_or_id = entry['psrn_or_id'])
                CourseInstructor.objects.create(
                    section_type = 'P',
                    course = course,
                    instructor = instructor,
                    section_number = entry['section_number']
                )

        response['error'] = False
        response['message'] = 'success'
    except Exception as e:
        print(e)
        response['error'] = True
        response['message'] = str(e)
    return JsonResponse(response, safe=False)

@login_required
# @csrf_exempt
def clear_course(request, *args, **kwargs):
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        course_list = get_equivalent_course_info(data['course_code'])
        for course in course_list:
            course = Course.objects.filter(code = course['code']).first()
            course.max_strength_per_l = 0
            course.max_strength_per_t = 0
            course.max_strength_per_p = 0
            course.ic = None
            course.save(update_fields=['max_strength_per_l', 'max_strength_per_t', 'max_strength_per_p', 'ic'])
            CourseInstructor.objects.filter(course = course).delete()
            CourseHistory.objects.create(course = course, l_count = 0, t_count = 0, p_count = 0, max_strength_per_l = 0, max_strength_per_t = 0, max_strength_per_p = 0, ic = None, enable = course.enable)

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