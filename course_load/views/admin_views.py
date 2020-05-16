import csv
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from course_load.forms import *
from course_load.models import Course, Instructor, CourseInstructor

from AUGSD_time_table_project.settings import MEDIA_ROOT, BASE_DIR
from populate import populate_from_admin_data

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
                        comcode = form.cleaned_data['comcode'], 
                        department = form.cleaned_data['department'], 
                        course_type = form.cleaned_data['course_type'], 
                        merge_with = form.cleaned_data['merge_with'], 
                    )
                    messages.success(request, "Course added successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Course not added.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Course not added.", extra_tags='alert-danger')
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
                    messages.success(request, "Instructor added successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.error(request, "Error occured. Instructor not added.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Instructor not added.", extra_tags='alert-danger')
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
        }
    except Exception as e:
        print(e)
        data = {
            'name': '',
            'comcode': '',
            'departemnt': '',
            'course_type': '',
            'merge_with': '',
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
def download_erp(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Course Load ERP.csv"'
        writer = csv.writer(response)
        writer.writerow(['Comcode', 'Course number', 'Course title', 'Section type', 'Section number', 'Instructor name', 'PSRN/ID', 'Role'])
        course_list = Course.objects.filter(ic__isnull = False).values('code').distinct().order_by('code')
        for course in course_list:
            course = Course.objects.get(code = course['code'])

            ic = course.ic
            ic_printed = False
            l_entry_list = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'L')
            for entry in l_entry_list:
                if ic_printed:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id, 'I'])
                else:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id, 'IC'])
                ic_printed = True
            t_entry_list = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'T')
            for entry in t_entry_list:
                if ic_printed:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id, 'I'])
                else:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id, 'IC'])
                ic_printed = True
            p_entry_list = CourseInstructor.objects.filter(course = course, instructor = ic, section_type = 'P')
            for entry in p_entry_list:
                if ic_printed:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id, 'I'])
                else:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, ic.name, ic.psrn_or_id, 'IC'])
                ic_printed = True
            if not ic_printed:
                writer.writerow([course.comcode, course.code, course.name, 'R', '1', ic.name, ic.psrn_or_id, 'IC'])
              
            instructor_list = CourseInstructor.objects.filter(course = course).values('instructor').distinct().order_by('instructor__instructor_type', 'instructor')
            for instructor in instructor_list:
                if instructor['instructor'] == ic.psrn_or_id:
                    continue
                instructor = Instructor.objects.get(psrn_or_id = instructor['instructor'])
                l_entry_list = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'L').order_by('section_number')
                for entry in l_entry_list:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, instructor.name, instructor.psrn_or_id, 'I'])
                t_entry_list = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'T').order_by('section_number')
                for entry in t_entry_list:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, instructor.name, instructor.psrn_or_id, 'I'])
                p_entry_list = CourseInstructor.objects.filter(course = course, instructor = instructor, section_type = 'P').order_by('section_number')
                for entry in p_entry_list:
                    writer.writerow([course.comcode, course.code, course.name, entry.section_type, entry.section_number, instructor.name, instructor.psrn_or_id, 'I'])
        return response
    else:
        return HttpResponseRedirect('/course-load/dashboard')

@login_required
def download_time_table(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Course Load timetable.csv"'
        writer = csv.writer(response)
        writer.writerow(['Comcode', 'Course number', 'Course title', 'Section type', 'Section number', 'Instructor names'])
        course_list = Course.objects.filter(ic__isnull = False).values('code').distinct().order_by('code')
        for course in course_list:
            course = Course.objects.get(code = course['code'])

            ic_printed = False;
            ic = course.ic
            if CourseInstructor.objects.filter(course = course, instructor = ic).count() == 0:
                writer.writerow([course.comcode, course.code, course.name, 'R', '1', ic.name])

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
                writer.writerow([course.comcode, course.code, course.name, 'L', sec, instructor_str])
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
                writer.writerow([course.comcode, course.code, course.name, 'T', sec, instructor_str])
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
                writer.writerow([course.comcode, course.code, course.name, 'P', sec, instructor_str])
        return response
    else:
        return HttpResponseRedirect('/course-load/dashboard')

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
                    populate_from_admin_data(MEDIA_ROOT+'/'+str(request.user.userprofile.initial_data_file))
                    messages.success(request, "Data uploaded successfully.", extra_tags='alert-success')
                    return HttpResponseRedirect('/course-load/dashboard')
                messages.success(request, "Error occured. Data not updated.", extra_tags='alert-success')
                return render(request, self.template_name, {'form': form})
            except Exception as e:
                print(e)
                messages.error(request, "Error occured. Data not updated.", extra_tags='alert-danger')
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseRedirect('/course-load/dashboard')

@login_required
def download_data_template(request):
    if request.user.is_superuser:
        path = BASE_DIR+'/'+'data_template.xlsx'
        if os.path.exists(path):
            with open(path, 'rb') as excel:
                data = excel.read()

            response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=data_template.xlsx'
            return response
    else:
        return HttpResponseRedirect('/course-load/dashboard')