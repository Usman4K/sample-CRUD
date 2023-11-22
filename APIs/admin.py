from django.contrib import admin

from .models import Student, Instructor, Enrollment, Course

# Register your models here.
admin.register([Student, Instructor, Enrollment, Course])
