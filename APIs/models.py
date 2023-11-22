import uuid

from django.db import models


# Create your models here.
class Instructor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructors = models.ManyToManyField(Instructor, related_name='instructors')


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course, related_name='students')


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
