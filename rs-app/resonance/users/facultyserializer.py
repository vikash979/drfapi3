from rest_framework import serializers
from .models import Student, Division, Subject,Faculty,FacultyPhase,EmploymentType,Designation,Department,FacultyBatch,FacultySubject,FacultyProgram,FacultyPhase,User
from institute.models import (
    Batch, Phase, Program, Sessions, Classs,Center,SessionProgram,ProgramClass,ProgramClassSubject
)
from subject.models import Subject, MasterSubject

from users.serializer import BatchDetailsSerializer,SubjectSerialiser,DivisionSerializer

class ClasssFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Classs
        fields = [ 'label',]

class ProgramClassFacultySerializer(serializers.ModelSerializer):
    classs = ClasssFacultySerializer(many=False)
    class Meta:
        model = ProgramClass
        fields = ['classs']

class SessionsFacultySerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        print(obj.id)
    class Meta:
        model = Sessions
        fields = ['id', 'label',]

class BatchFacultySerializer(serializers.ModelSerializer):
    #phase = PhaseSerializer(many=False)
    class Meta:
        model = Batch
        fields = ['id', 'label',]

class PhaseFacultySerializer(serializers.ModelSerializer):
    #batches = BatchFacultySerializer(many=True)
   
    class Meta:
        model = Phase
        fields = [ 'id','label']


class ProgramFacultySerializer(serializers.ModelSerializer):
    #classes = ProgramClassSerializer(many=True)
    #sessionprogram = SessionProgramFacultySerializer(many=True)

    class Meta:
        model = Program
        fields = [ 'id','label']

class SessionProgramFacultySerializer(serializers.ModelSerializer):
    session = SessionsFacultySerializer(many=False)
    #phases = PhaseFacultySerializer(many=True)
    program = ProgramFacultySerializer(many=False)

    class Meta:
        model = SessionProgram
        fields = ['id','session','program']




class MasterSubjectFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSubject
        fields = ['url', 'background_code']

class SubjectFacultySerializer(serializers.ModelSerializer):
    master_subject = MasterSubjectFacultySerializer()
    class Meta:
        model = Subject
        fields = ['master_subject',]



class FacultyBatchFacultySerializer(serializers.ModelSerializer):
    batch = BatchFacultySerializer(many=False)

    def to_representation(self, obj):
        session_id =obj.batch.phase.session_program.session_id
        session_o = Sessions.objects.filter(id=session_id)
        session_data = SessionsFacultySerializer(session_o,many=True).data
        phase_data = PhaseFacultySerializer(Phase.objects.filter(id=obj.batch.phase.id),many=True).data
        program_ob = ProgramFacultySerializer(Program.objects.filter(id=obj.batch.phase.session_program.program_id),many=True).data
        if len(phase_data)>0:
            phase_data =phase_data[0]
        else:
            phase_data = phase_data
        if len(session_data) > 0:
            session_data = session_data[0]
        else:
            session_data = None
        if len(program_ob) > 0:
            program_ob = program_ob[0]
        else:
            program_ob = None



        # session_program = SessionProgram.objects.filter(id=phase_id)
        # session_ob = SessionProgramFacultySerializer(session_program,many=True)
        
       

        data = {
            "id": obj.batch.id,
            "label": obj.batch.label,
            "phase":phase_data,
            #"session":SessionsFacultySerializer(Sessions.objects.filter(id=obj.batch.phase.session_program.session_id)).data
            "sessions":session_data,
           "program":program_ob
            #"session_program": SessionProgramFacultySerializer(SessionProgram.objects.filter(id=obj.batch.phase.session_program.id),many=True).data


        }
        return data

    class Meta:
        model = FacultyBatch
        fields = ['batch']



class FacultySubjectFacultySerializer(serializers.ModelSerializer):
    subject = SubjectFacultySerializer(many=False)

    class Meta:
        model = FacultySubject
        fields = ['subject']


class FacultyPhaseFacultySerializer(serializers.ModelSerializer):
    phase = PhaseFacultySerializer(many=False)

    class Meta:
        model = FacultyPhase
        fields = ['phase']


class FacultyProgramFacultySerializer(serializers.ModelSerializer):
    Program = ProgramFacultySerializer(many=False)


    class Meta:
        model = FacultyProgram
        fields = ['Program']


class EmploymentTypeFacultySerializer(serializers.ModelSerializer):

    def to_representation(self,obj):
        return obj.name

    class Meta:
        model = EmploymentType
        fields =['name']


class DivisionFacultySerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return obj.name

    class Meta:
        model = Division
        fields =['name']

class CenterFacultySerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        return obj.name

    class Meta:
        model = Center
        fields =['name']

class DesignationFacultySerializer(serializers.ModelSerializer):

    def to_representation(self,obj):
        return obj.name


    class Meta:
        model = Designation
        fields =['name']

class DepartmentFacultySerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        return obj.name

    class Meta:
        model = Department
        fields =['name']

class FacultyFacultySerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    division = DivisionSerializer()
    employment_type = EmploymentTypeFacultySerializer()
    gender = serializers.SerializerMethodField()
    center = CenterFacultySerializer()
    designation = DesignationFacultySerializer()
    department = DepartmentFacultySerializer()
    #programs =  FacultyProgramFacultySerializer(many=True)
    name = serializers.SerializerMethodField()
    date_of_birth =  serializers.SerializerMethodField()
    
    batches = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    
        

    def get_subjects(self,obj):
        subjects = Subject.objects.filter(id__in=FacultySubject.objects.filter(faculty=obj).values_list('subject_id'))
        return SubjectSerialiser(subjects,many=True).data
    
    class Meta:
            model = Faculty

            fields =('id','name','profile_picture','gender','date_of_birth','short_name',
                'department','designation','employment_type','division','center','employee_code',
                'subjects','reporting_manager','batches','date_of_joining')


    def get_name(self,obj):
        return obj.user.name
    
    def get_profile_picture(self,obj):
        return obj.user.profile_picture.url if obj.user.profile_picture else ''
    
    def get_gender(self,obj):
        return obj.user.get_gender_display()

    def get_date_of_birth(self,obj):
        return obj.user.date_of_birth

    def get_batches(self,obj):
        batches  = Batch.objects.filter(id__in=FacultyBatch.objects.filter(faculty = obj.id).values_list('batch_id'))
        return BatchDetailsSerializer(batches,many=True).data
