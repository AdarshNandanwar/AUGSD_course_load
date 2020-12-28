from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from course_load.views import (admin_views)

urlpatterns = [
    path('', lambda request: redirect('course-load/dashboard', permanent=False)),
    path('admin/', admin.site.urls),
    path('course-load/', include('course_load.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add-course/', admin_views.AddCourse.as_view()),
    path('add-instructor/', admin_views.AddInstructor.as_view()),
    path('update-course/', admin_views.UpdateCourse.as_view()),
    path('update-instructor/', admin_views.UpdateInstructor.as_view()),
    path('delete-course/', admin_views.DeleteCourse.as_view()),
    path('delete-instructor/', admin_views.DeleteInstructor.as_view()),
    path('get-course-preview/', admin_views.get_course_preview),
    path('get-instructor-preview/', admin_views.get_instructor_preview),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)