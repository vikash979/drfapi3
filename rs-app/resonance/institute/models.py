from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date, datetime

from common.models import BaseTOCModel,TOCMapping,BaseResonanceModel
from subject.models import Subject
from django.contrib.auth import get_user_model
from common.choices import CscType

#User = get_user_model()


class Classs(BaseResonanceModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=200,unique=True)
    order = models.IntegerField()
    description = models.TextField()
    short_code  = models.CharField(max_length=200,unique=True)

    ordering = ['id']

    def __str__(self):
        return self.label


class Target(BaseResonanceModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    short_code  = models.CharField(max_length=200,unique=True)
    label = models.CharField(max_length=200,unique=True)


class Program(BaseTOCModel):
    subject_choice = (
        (1, "Online"),
        (2, "Distance Program"),
        (3, "Offline"),
    )
    short_code = models.CharField(max_length=200,unique=True)
    label = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    type = models.IntegerField(choices=subject_choice, default=1)

    target = models.ForeignKey(Target, related_name='target_name', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.label

class ProgramClass(BaseResonanceModel):
    classs = models.ForeignKey(Classs, related_name='programs',  on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name='classes',  on_delete=models.CASCADE)


class ProgramClassSubject(BaseResonanceModel):

    program_has_class = models.ForeignKey(ProgramClass, related_name='program_class', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,null=True,on_delete=models.SET_NULL)


class Sessions(BaseResonanceModel):
    #YEAR_CHOICES = [(r, r) for r in range(2000, date.today().year + 1)]

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    # year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
    start_date = models.DateField()
    end_date = models.DateField()
    short_code  = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.label

class SessionProgram(BaseResonanceModel):

    session = models.ForeignKey(Sessions,related_name='sessions',  on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name='sessionprogram', on_delete=models.CASCADE)

    def __str__(self):
        return self.session.label

class Phase(BaseResonanceModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=200,unique=True)
    short_code  = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    session_program = models.ForeignKey(SessionProgram, related_name='phases', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.session_program.program.label+", "+str(self.session_program.session)

class Batch(BaseResonanceModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    phase = models.ForeignKey(Phase, related_name='batches',  on_delete=models.CASCADE)
    times_slot = models.TimeField(auto_now=False, auto_now_add=False)
    short_code  = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.label

class StudentClassPath(BaseResonanceModel):
    current_choice = (
        (0, "Zero"),
        (1, "One"),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    classes = models.ForeignKey(Classs, related_name='students', on_delete=models.CASCADE)
    current = models.IntegerField(choices=current_choice, default='0')
    status = models.BooleanField(default=True, blank=True)

class CscDetails(BaseResonanceModel):
    label = models.CharField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey('self',blank=True,null=True,on_delete=models.SET_NULL)
    csc_type = models.IntegerField(choices=CscType.CHOICES, blank=True, null=True)

    def __str__(self):
        return self.label


class Center(BaseResonanceModel):
    name = models.CharField("Center name", max_length=120)
    country = models.ForeignKey(CscDetails, related_name='country',on_delete=models.SET_NULL,null=True)
    state = models.ForeignKey(CscDetails, related_name="state",on_delete=models.SET_NULL,null=True)
    city = models.ForeignKey(CscDetails,related_name="city" ,on_delete=models.SET_NULL,null=True)
    status = models.BooleanField("Center status", default=True)

    def __str__(self):
        return self.name
