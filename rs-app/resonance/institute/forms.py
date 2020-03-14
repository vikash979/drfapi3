from django import forms
from institute.models import Classs ,Program, ProgramClassSubject, Sessions, Phase, Batch
from content.models import Lecture, Assessment

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'duration_hrs', 'faculty', 'room', 'start_date_time']

class ClasssForm(forms.ModelForm):
    class Meta:
        model = Classs
        fields = ('label','order','description')



class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('label', 'description', 'target')


class ProgramClassSubjectForm(forms.ModelForm):
    class Meta:
        model = ProgramClassSubject
        fields = ('program_has_class', 'subject')



# class SessionsForm(forms.ModelForm):
#     class Meta:
#         model = Sessions
#         fields = ['subject']




class PhaseForm(forms.ModelForm):
    start_date = forms.DateField() 
    end_date = forms.DateField()

    class Meta:
        model = Phase
        fields = ('label', 'description', 'session_program', 'start_date', 'end_date')

class BatchForm(forms.ModelForm):
    
    times_slot = forms.TimeField()
    class Meta:
        model = Batch
        fields = ('label', 'description', 'phase', 'times_slot')




