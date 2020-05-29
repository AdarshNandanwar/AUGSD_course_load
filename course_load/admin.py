from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(CourseInstructor)
admin.site.register(CourseAccessRequested)
admin.site.register(PortalSettings)