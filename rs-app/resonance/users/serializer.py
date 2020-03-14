from rest_framework import serializers
from .models import Student, Division, StudentSubject,Faculty,FacultyPhase,EmploymentType,Designation,Department,FacultyBatch,FacultySubject,FacultyProgram,FacultyPhase
from institute.models import (
    Batch, Phase, Program, Sessions, Classs,Center,ProgramClass
)
from subject.models import Subject, MasterSubject


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'name',]


class ClasssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classs
        fields = [ 'id','label',]

class ProgramClassSerializer(serializers.ModelSerializer):
    classs = ClasssSerializer(many=False)
    class Meta:
        model = ProgramClass
        fields = ['classs']

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = ['id', 'label',]


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'label',]

class BatchDetailsSerializer(serializers.ModelSerializer):
    phase = serializers.SerializerMethodField()
    program = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()
    
    class Meta:
        model = Batch
        fields = ['id', 'label','phase','program','session']

    def get_phase(self,obj):
        return {"id":obj.phase.id,"label":obj.phase.label}

    def get_program(self,obj):
        return {"id":obj.phase.session_program.program.id,"label":obj.phase.session_program.program.label}

    def get_session(self,obj):
        return {"id":obj.phase.session_program.session.id,"label":obj.phase.session_program.session.label}


class PhaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Phase
        fields = ['id', 'label',]

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'label',]

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = ['id', 'label',]

class ClasssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classs
        fields = ['id', 'label',]

class MasterSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSubject
        fields = ['url', 'background_code']

class SubjectSerializer(serializers.ModelSerializer):
    master_subject = MasterSubjectSerializer()
    class Meta:
        model = Subject
        fields = ['master_subject',]

class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = ['subject']
        depth = 2

class SubjectSerialiser(serializers.ModelSerializer):
    url = serializers.CharField(source="master_subject.url")
    background_code = serializers.CharField(source="master_subject.background_code")
    class Meta:
        model = Subject
        fields = ['id','label','url','background_code']


# class SubjectSerialiser(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()
    batches = serializers.SerializerMethodField()
    classs = ClasssSerializer()
    division = DivisionSerializer()
    unread_notice_count = serializers.SerializerMethodField()
    name = serializers.CharField()
    center_name = serializers.CharField()
    city_name = serializers.CharField()
    is_faculty = serializers.SerializerMethodField()
    medium = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    
    def get_subjects(self,obj):
        subjects = Subject.objects.filter(id__in=StudentSubject.objects.filter(student=obj).values_list('subject_id'))
        
        return SubjectSerialiser(subjects,many=True).data

    def get_medium(self,obj):
        return obj.get_medium_display()

    def get_unread_notice_count(self,obj):
        return "123"

    def get_batches(self,obj):
        return BatchDetailsSerializer([obj.batch],many=True).data

    def get_is_faculty(self,obj):
        return obj.user.role == 3

    # def get_batch(self,obj):

    class Meta:
        model = Student
        exclude = ['user', 'center','status','batch','session','program','phase']






class FacultyBatchSerializer(serializers.ModelSerializer):
    batch = BatchSerializer(many=False)


    class Meta:
        model = FacultyBatch
        fields = ['batch']



class FacultySubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=False)

    class Meta:
        model = FacultySubject
        fields = ['subject']


class FacultyPhaseSerializer(serializers.ModelSerializer):
    phase = PhaseSerializer(many=False)

    class Meta:
        model = FacultyPhase
        fields = ['phase']


class FacultyProgramSerializer(serializers.ModelSerializer):
    #Program = ProgramSerializer(many=False)

    class Meta:
        model = FacultyProgram
        fields = ['Program']


class EmploymentTypeSerializer(serializers.ModelSerializer):

    def to_representation(self,obj):
        return obj.name

    class Meta:
        model = EmploymentType
        fields =['name']


# class DivisionSerializer(serializers.ModelSerializer):
#     def to_representation(self, obj):
#         return obj.name

#     class Meta:
#         model = Division
#         fields =['name']

class CenterSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        return obj.name

    class Meta:
        model = Center
        fields =['name']

class DesignationSerializer(serializers.ModelSerializer):

    def to_representation(self,obj):
        return obj.name


    class Meta:
        model = Designation
        fields =['name']

class DepartmentSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        return obj.name

    class Meta:
        model = Department
        fields =['name']

class FacultySerializer(serializers.ModelSerializer):
    division = DivisionSerializer()
    employment_type = EmploymentTypeSerializer()
    center = CenterSerializer()
    designation = DesignationSerializer()
    department = DepartmentSerializer()
    batch = FacultyBatchSerializer(many=True)
    subject = FacultySubjectSerializer(many=True)
    programs =  FacultyProgramSerializer(many=True)
    
    #phases = FacultyPhaseSerializer(many=True)

    class Meta:
            model = Faculty

            fields =['short_name','department','designation','employment_type','division','center','employee_code','reporting_manager','batch','subject','programs']

    # def get_reporting_manager(self,obj):
        
    #     return FacultySerializer(obj.reporting_manager).data
