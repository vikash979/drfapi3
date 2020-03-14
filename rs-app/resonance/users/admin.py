from django.contrib import admin
from users.models import (
    User, Faculty, Student, Department, EmploymentType, Designation,
    Division, FacultySubject, FacultyBatch, StudentSubject,FacultyPhase,FacultyProgram,StudentBatch
)
# Register your models here.

admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Division)
admin.site.register(Department)
admin.site.register(EmploymentType)
admin.site.register(Designation)
admin.site.register(FacultySubject)
admin.site.register(StudentSubject)
admin.site.register(FacultyBatch)
admin.site.register(FacultyPhase)
admin.site.register(FacultyProgram)
admin.site.register(StudentBatch)

