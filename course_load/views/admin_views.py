import csv
import os
import pandas as pd
import numpy as np

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from course_load.forms import *
from course_load.models import Course, Instructor, CourseInstructor, CourseHistory, PortalSettings

from AUGSD_time_table_project.settings import MEDIA_ROOT, BASE_DIR
from populate import populate_from_admin_data
from course_load.utils import get_equivalent_course_info


@method_decorator(login_required, name='dispatch')
class TogglePortal(View):
    form_class = TogglePortalForm
    initial = {'key': 'value'}
    template_name = 'admin/toggle-portal.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            initial = {"is_portal_active": PortalSettings.objects.filter().first().is_portal_active}
            form = self.form_class(initial=initial)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                form = self.form_class(request.POST)
                if form.is_valid():
                    PortalSettings.objects.filter().update(is_portal_active=form.cleaned_data["is_portal_active"])
                    if form.cleaned_data["disable_all_courses"] is True:
                        Course.objects.filter().update(enable=False)
                    messages.success(request, "Portal toggled successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class AddCourse(View):
    form_class = AddCourseForm
    form_class_bulk = AddCourseBulkForm
    initial = {'key': 'value'}
    template_name = 'admin/add-course.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            form_bulk = self.form_class_bulk(initial=self.initial)
            return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                form = self.form_class(request.POST)
                form_bulk = self.form_class_bulk(initial=self.initial)
                if form.is_valid():
                    course, created = Course.objects.get_or_create(
                        code = form.cleaned_data['code'], 
                        name = form.cleaned_data['name'], 
                        comcode = form.cleaned_data['comcode'], 
                        department = form.cleaned_data['department'], 
                        course_type = form.cleaned_data['course_type'], 
                        merge_with = form.cleaned_data['merge_with'], 
                        past_course_strength = form.cleaned_data['past_course_strength'], 
                        sem = form.cleaned_data['sem'], 
                        lpu = form.cleaned_data['lpu'], 
                    )
                    messages.success(request, "Course added successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Course not added.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Course not added.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class AddCourseBulk(View):
    form_class = AddCourseForm
    form_class_bulk = AddCourseBulkForm
    initial = {'key': 'value'}
    template_name = 'admin/add-course.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            form_bulk = self.form_class_bulk(request.POST, request.FILES)
            try:
                if form_bulk.is_valid():
                    request.user.userprofile.course_file = request.FILES['course_file']
                    request.user.userprofile.save()
                    populate_from_admin_data(request.user.userprofile.course_file.url, clear_db = False, query = "course")
                    messages.success(request, "Data uploaded successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class AddInstructor(View):
    form_class = AddInstructorForm
    form_class_bulk = AddInstructorBulkForm
    initial = {'key': 'value'}
    template_name = 'admin/add-instructor.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            form_bulk = self.form_class_bulk(initial=self.initial)
            return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                form = self.form_class(request.POST)
                form_bulk = self.form_class_bulk(initial=self.initial)
                if form.is_valid():
                    instructor, created = Instructor.objects.get_or_create(
                        psrn_or_id = form.cleaned_data['psrn_or_id'], 
                        name = form.cleaned_data['name'], 
                        department = form.cleaned_data['department'], 
                        instructor_type = form.cleaned_data['instructor_type'], 
                    )
                    messages.success(request, "Instructor added successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Instructor not added.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Instructor not added.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class AddInstructorBulk(View):
    form_class = AddInstructorForm
    form_class_bulk = AddInstructorBulkForm
    initial = {'key': 'value'}
    template_name = 'admin/add-instructor.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            form_bulk = self.form_class_bulk(request.POST, request.FILES)
            try:
                if form_bulk.is_valid():
                    request.user.userprofile.instructor_file = request.FILES['instructor_file']
                    request.user.userprofile.save()
                    populate_from_admin_data(request.user.userprofile.instructor_file.url, clear_db = False, query = "instructor")
                    messages.success(request, "Data uploaded successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form, 'form_bulk': form_bulk})
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
                course_original = Course.objects.get(code = request.POST['old_code'])
                form = self.form_class(request.POST, instance = course)
            except Course.DoesNotExist:
                form = self.form_class(initial=self.initial)
                messages.error(request, "Course not found.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            course.delete()
            try:
                if form.is_valid():
                    form.code = form.cleaned_data['code'], 
                    form.name = form.cleaned_data['name'], 
                    form.department = Department.objects.get(code = form.cleaned_data['department']), 
                    form.course_type = form.cleaned_data['course_type'], 
                    form.save()
                    messages.success(request, "Course updated successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
            except Exception as e:
                course_original.save()
                print(e)
                messages.error(request, "Error occured. Course not updated.", extra_tags='alert-danger')
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
                instructor_original = Instructor.objects.get(psrn_or_id = request.POST['old_psrn_or_id'])
                form = self.form_class(request.POST, instance = instructor)
            except Instructor.DoesNotExist:
                form = self.form_class(initial=self.initial)
                messages.error(request, "Instructor not found.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            instructor.delete()
            try:
                if form.is_valid():
                    form.psrn_or_id = form.cleaned_data['psrn_or_id'], 
                    form.name = form.cleaned_data['name'], 
                    form.department = Department.objects.get(code = form.cleaned_data['department']), 
                    form.instructor_type = form.cleaned_data['instructor_type'], 
                    form.save()
                    messages.success(request, "Instructor updated successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
            except Exception as e:
                instructor_original.save()
                print(e)
                messages.error(request, "Error occured. Instructor not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class DeleteCourse(View):
    form_class = DeleteCourseForm
    initial = {'key': 'value'}
    template_name = 'admin/delete-course.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                course = Course.objects.get(code = request.POST['code'])
            except Course.DoesNotExist:
                form = self.form_class(initial=self.initial)
                messages.error(request, "Course not found.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            course.delete()
            messages.success(request, "Course deleted successfully.", extra_tags='alert-success')
            return HttpResponseRedirect('/course-load/dashboard')
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class DeleteInstructor(View):
    form_class = DeleteInstructorForm
    initial = {'key': 'value'}
    template_name = 'admin/delete-instructor.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            try:
                instructor = Instructor.objects.get(psrn_or_id = request.POST['psrn_or_id'])
            except Instructor.DoesNotExist:
                form = self.form_class(initial=self.initial)
                messages.error(request, "Instructor not found.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            instructor.delete()
            messages.success(request, "Instructor deleted successfully.", extra_tags='alert-success')
            return HttpResponseRedirect('/course-load/dashboard')
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@login_required
def get_course_preview(request):
    code = request.GET.get('course_code', None)
    try:
        course = Course.objects.get(code = code)
        data = {
            'name': course.name,
            'comcode': course.comcode,
            'department': course.department.name,
            'course_type': course.course_type,
            'merge_with': '-' if course.merge_with is None else course.merge_with.code,
            'past_course_strength': course.past_course_strength,
            'sem': course.sem,
            'lpu': course.lpu
        }
    except Exception as e:
        print(e)
        data = {
            'name': '',
            'comcode': '',
            'departemnt': '',
            'course_type': '',
            'merge_with': '',
            'past_course_strength': '',
            'sem': '',
            'lpu': ''
        }
    return JsonResponse(data)

@login_required
def get_instructor_preview(request):
    psrn_or_id = request.GET.get('psrn_or_id', None)
    try:
        instructor = Instructor.objects.get(psrn_or_id = psrn_or_id)
        data = {
            'name': instructor.name,
            'department': instructor.department.name,
            'instructor_type': instructor.instructor_type,
        }
    except Exception as e:
        print(e)
        data = {
            'name': '',
            'departemnt': '',
            'instructor_type': '',
        }
    return JsonResponse(data)

@login_required
def get_course_history(request):
    response = {
        'history': [],
        'error': False,
        'message': 'success'
    }
    if request.user.is_superuser:
        course_code = request.GET.get('course_code', None)
        try:
            course = Course.objects.get(code = course_code)
            course_history = CourseHistory.objects.filter(course = course)
            for entry in course_history:
                response['history'].append(
                    {
                        'time': entry.created,
                        'l_count': entry.l_count,
                        't_count': entry.t_count,
                        'p_count': entry.p_count,
                        'max_strength_per_l': entry.max_strength_per_l,
                        'max_strength_per_t': entry.max_strength_per_t,
                        'max_strength_per_p': entry.max_strength_per_p,
                        'enable': entry.enable
                    }
                )
        except Exception as e:
            response['history'] = []
            response['error'] = True
            response['message'] = str(e)
    else: 
        response['message'] = "superuser required"
    return JsonResponse(response)

@login_required
def download_erp(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Course Load ERP.csv"'
        writer = csv.writer(response)
        writer.writerow(['Comcode', 'Course number', 'Course title', 'Section type', 'Section number', 'Instructor name', 'PSRN/ID', 'Role'])
        course_list = Course.objects.filter(enable = True).values('code').distinct().order_by('code')
        for course in course_list:
            course = Course.objects.get(code = course['code'])
            ic = course.ic
            print(ic.instructor_type)
            ic_printed = False
            l_entry_list = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'L')
            for entry in l_entry_list:
                if ic_printed:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id if ic.instructor_type == 'F' else ic.system_id, 'I'])
                else:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id if ic.instructor_type == 'F' else ic.system_id, 'IC'])
                ic_printed = True
            t_entry_list = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'T')
            for entry in t_entry_list:
                if ic_printed:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id if ic.instructor_type == 'F' else ic.system_id, 'I'])
                else:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id if ic.instructor_type == 'F' else ic.system_id, 'IC'])
                ic_printed = True
            p_entry_list = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'P')
            for entry in p_entry_list:
                if ic_printed:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id if ic.instructor_type == 'F' else ic.system_id, 'I'])
                else:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id if ic.instructor_type == 'F' else ic.system_id, 'IC'])
                ic_printed = True
            if not ic_printed:
                writer.writerow([course.comcode, course.code, course.name, 'R', '1', ic.name, ic.psrn_or_id if ic.instructor_type == 'F' else ic.system_id, 'IC'])
              
            instructor_list = CourseInstructor.objects.filter(course = course).values('instructor').distinct().order_by('instructor__instructor_type', 'instructor')
            for instructor in instructor_list:
                if instructor['instructor'] == ic.psrn_or_id:
                    continue
                instructor = Instructor.objects.get(psrn_or_id = instructor['instructor'])
                l_entry_list = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'L').order_by('section_number')
                for entry in l_entry_list:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, instructor.name, instructor.psrn_or_id if instructor.instructor_type == 'F' else instructor.system_id, 'I'])
                t_entry_list = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'T').order_by('section_number')
                for entry in t_entry_list:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, instructor.name, instructor.psrn_or_id if instructor.instructor_type == 'F' else instructor.system_id, 'I'])
                p_entry_list = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'P').order_by('section_number')
                for entry in p_entry_list:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, instructor.name, instructor.psrn_or_id if instructor.instructor_type == 'F' else instructor.system_id, 'I'])
        return response
    else:
        return HttpResponseRedirect('/course-load/dashboard')

@login_required
def download_time_table(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Course Load timetable.csv"'
        writer = csv.writer(response)
        writer.writerow(['Comcode', 'Course number', 'Course title', 'L P U', 'Section type', 'Section number', 'Instructor names'])
        course_list = Course.objects.filter(enable = True).values('code').distinct().order_by('code')
        for course in course_list:
            course = Course.objects.get(code = course['code'])

            ic_printed = False;
            ic = course.ic
            if CourseInstructor.objects.filter(course = course, instructor = ic).count() == 0:
                writer.writerow([course.comcode, course.code, course.name, course.lpu, 'R', '1', ic.name])

            l_count = CourseInstructor.objects.filter(course = course, section_type = 'L').values('section_number').distinct().count()
            t_count = CourseInstructor.objects.filter(course = course, section_type = 'T').values('section_number').distinct().count()
            p_count = CourseInstructor.objects.filter(course = course, section_type = 'P').values('section_number').distinct().count()

            for sec in range(1, l_count+1):
                instructor_str = ""
                has_ic = CourseInstructor.objects.filter(course = course, section_type = 'L', section_number = sec, instructor = ic)
                for course_instructor in has_ic:
                    if not ic_printed:
                        instructor_str += (course_instructor.instructor.name.upper()+'/ ')
                        ic_printed = True
                    else:
                        instructor_str += (course_instructor.instructor.name.title()+'/ ')
                course_instructor_list = CourseInstructor.objects.filter(course = course, section_type = 'L', section_number = sec).exclude(instructor = ic)
                for course_instructor in course_instructor_list:
                    instructor_str += (course_instructor.instructor.name.title()+'/ ')
                instructor_str = instructor_str[:-2]
                writer.writerow([course.comcode, course.code, course.name, course.lpu, 'L', sec, instructor_str])
            for sec in range(1, t_count+1):
                instructor_str = ""
                has_ic = CourseInstructor.objects.filter(course = course, section_type = 'T', section_number = sec, instructor = ic)
                for course_instructor in has_ic:
                    if not ic_printed:
                        instructor_str += (course_instructor.instructor.name.upper()+'/ ')
                        ic_printed = True
                    else:
                        instructor_str += (course_instructor.instructor.name.title()+'/ ')
                course_instructor_list = CourseInstructor.objects.filter(course = course, section_type = 'T', section_number = sec).exclude(instructor = ic)
                for course_instructor in course_instructor_list:
                    instructor_str += (course_instructor.instructor.name.title()+'/ ')
                instructor_str = instructor_str[:-2]
                writer.writerow([course.comcode, course.code, course.name, course.lpu, 'T', sec, instructor_str])
            for sec in range(1, p_count+1):
                instructor_str = ""
                has_ic = CourseInstructor.objects.filter(course = course, section_type = 'P', section_number = sec, instructor = ic)
                for course_instructor in has_ic:
                    if not ic_printed:
                        instructor_str += (course_instructor.instructor.name.upper()+', ')
                        ic_printed = True
                    else:
                        instructor_str += (course_instructor.instructor.name.title()+', ')
                course_instructor_list = CourseInstructor.objects.filter(course = course, section_type = 'P', section_number = sec).exclude(instructor = ic)
                for course_instructor in course_instructor_list:
                    instructor_str += (course_instructor.instructor.name.title()+', ')
                instructor_str = instructor_str[:-2]
                writer.writerow([course.comcode, course.code, course.name, course.lpu, 'P', sec, instructor_str])
        return response
    else:
        return HttpResponseRedirect('/course-load/dashboard')

@login_required
def download_instructor_wise_compressed(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Course Load instructor-wise.csv"'
    writer = csv.writer(response)
    writer.writerow(['Deptartment', 'PSRN/ID', 'Instructor name', 'Course number', 'Course title', 'L', 'T', 'P', 'Role'])
    instructor_list = None
    if request.user.is_superuser:
        instructor_list_1 = list(CourseInstructor.objects.filter(course__enable = True).values_list('instructor', flat=True).distinct())
        instructor_list_2 = list(Course.objects.filter(enable = True).values_list('ic', flat=True).distinct())
        instructor_list = instructor_list_1 + instructor_list_2
        instructor_list = list(set(instructor_list))
    else:
        instructor_list_1 = list(CourseInstructor.objects.filter(course__enable = True, instructor__department = request.user.userprofile.department).values_list('instructor', flat=True).distinct())
        instructor_list_2 = list(Course.objects.filter(enable = True, ic__department = request.user.userprofile.department).values_list('ic', flat=True).distinct())
        instructor_list = instructor_list_1 + instructor_list_2
        instructor_list = list(set(instructor_list))
    instructor_list = Instructor.objects.filter(psrn_or_id__in = instructor_list).order_by('department', 'instructor_type', 'psrn_or_id')
    for instructor in instructor_list:
        course_list_1 = list(CourseInstructor.objects.filter(course__enable = True, instructor = instructor).values_list('course', flat=True).distinct())
        course_list_2 = list(Course.objects.filter(enable = True, ic = instructor).values_list('code', flat=True).distinct())
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
                writer.writerow([instructor.department, instructor.psrn_or_id, instructor.name, course.code, course.name, l_count, t_count, p_count, role])
            else:
                combined_code = equivalent_course_list[0]['code']
                for i in range(1, len(equivalent_course_list)):
                    combined_code = combined_code+' / '+equivalent_course_list[i]['code']
                writer.writerow([instructor.department, instructor.psrn_or_id, instructor.name, combined_code, course.name, l_count, t_count, p_count, role])
    return response

@method_decorator(login_required, name='dispatch')
class UploadInitialData(View):
    form_class = InitialDataFileForm
    initial = {'key': 'value'}
    template_name = 'admin/upload-initial-data.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=request.user.userprofile.__dict__)
            return render(request, self.template_name, {
                'form': form,
                'uploaded_file': request.user.userprofile.initial_data_file})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(request.POST, request.FILES)
            try:
                if form.is_valid():
                    request.user.userprofile.initial_data_file = request.FILES['initial_data_file']
                    request.user.userprofile.save()
                    populate_from_admin_data(request.user.userprofile.initial_data_file.url, clear_db = True)
                    messages.success(request, "Data uploaded successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@method_decorator(login_required, name='dispatch')
class UploadPastCourseStrengthData(View):
    form_class = PastCourseStrengthFileForm
    initial = {'key': 'value'}
    template_name = 'admin/upload-past-course-strength-data.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(initial=request.user.userprofile.__dict__)
            return render(request, self.template_name, {
                'form': form,
                'uploaded_file': request.user.userprofile.past_course_strength_data_file})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = self.form_class(request.POST, request.FILES)
            try:
                if form.is_valid():
                    request.user.userprofile.past_course_strength_data_file = request.FILES['past_course_strength_data_file']
                    request.user.userprofile.save()


                    print("Populating past course capacity")
                    try:
                        cap = pd.read_excel(request.user.userprofile.past_course_strength_data_file.url, 'sheet1', skiprows=1, usecols=['Subject', 'Catalog', 'Section', 'Tot Enrl'])
                        cap['Catalog'] = cap['Catalog'].str.strip()
                        cap['Section'] = cap['Section'].apply(lambda x: x[0])
                        df = pd.DataFrame()
                        cc = cap['Subject'] + " " + cap['Catalog'] + cap['Section']
                        df['course_code'] = cc.unique()
                        df['size'] = cap.groupby(['Subject', 'Catalog', 'Section'])['Tot Enrl'].sum().reset_index()['Tot Enrl']
                        df['course_code'] = df['course_code'].apply(lambda x: x[:-1])
                        df = df.drop_duplicates()
                        for ind in df.index:
                            Course.objects.filter(code = df['course_code'][ind].upper()).update(past_course_strength = df['size'][ind])
                    except Exception as e:
                        print("Error populating past course capacity")
                        raise Exception(e)


                    messages.success(request, "Data uploaded successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')


@method_decorator(login_required, name='dispatch')
class ViewCourseHistory(View):
    template_name = 'admin/view-course-history.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, self.template_name, {})
        else:
            return HttpResponseRedirect('/course-load/dashboard')


# DOWNLOAD API

@login_required
def download_course_data_template(request):
    return download_excel_file(request, 'course_data_template.xlsx')

@login_required
def download_instructor_data_template(request):
    return download_excel_file(request, 'instructor_data_template.xlsx')

@login_required
def download_data_template(request):
    return download_excel_file(request, 'data_template.xlsx')

@login_required
def download_past_course_strength_data_template(request):
    return download_excel_file(request, 'past_course_strength_data_template.xls')

@login_required
def download_excel_file(request, file_name):
    if request.user.is_superuser:
        path = os.path.join(BASE_DIR, 'sample_data', file_name)
        if os.path.exists(path):
            with open(path, 'rb') as excel:
                data = excel.read()

            response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename='+file_name
            return response
    else:
        return HttpResponseRedirect('/course-load/dashboard')