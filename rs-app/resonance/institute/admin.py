from django.contrib import admin
from .models import (
    Classs, Target, Program, ProgramClass,ProgramClassSubject, Sessions,SessionProgram,Phase,Batch,StudentClassPath, CscDetails, Center

)

admin.site.register(Classs)
admin.site.register(Target)
admin.site.register(Program)
admin.site.register(ProgramClass)
admin.site.register(ProgramClassSubject)
admin.site.register(Sessions)
admin.site.register(SessionProgram)
admin.site.register(Phase)
admin.site.register(Batch)
admin.site.register(StudentClassPath)
admin.site.register(CscDetails)
admin.site.register(Center)
