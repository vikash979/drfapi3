from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users.models import (
    Student, StudentSubject, Faculty, User, FacultySubject, FacultyBatch
)
from users.facultyserializer import SubjectSerialiser, BatchDetailsSerializer
from subject.models import Subject
from institute.models import Program
from institute.models import (
    Batch, Phase, Program, Sessions, Classs,Center,SessionProgram,ProgramClass,ProgramClassSubject
)

class ClasssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classs
        fields = [ 'label',]

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
    #phase = PhaseSerializer(many=False)
    class Meta:
        model = Batch
        fields = ['id', 'label',]

class PhaseSerializer(serializers.ModelSerializer):
    batches = BatchSerializer(many=True)

    class Meta:
        model = Phase
        fields = [ 'id','label','batches']

class SessionProgramSerializer(serializers.ModelSerializer):
    session = SessionsSerializer(many=False)
    phases = PhaseSerializer(many=True)
    #program = ProgramSerializer(many=False)

    class Meta:
        model = SessionProgram
        fields = ['id','phases','session']

class ProgramSerializer(serializers.ModelSerializer):
    #classes = ProgramClassSerializer(many=True)
    sessionprogram = SessionProgramSerializer(many=True)
    class Meta:
        model = Program
        fields = [ 'id','label','sessionprogram']


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    username = serializers.CharField()

    class Meta:
        fields = ['username', 'password']

    # def validate_email(self, value):
    #     if not User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("Please Enter a valid email")
    #     return value

# class SubjectSerialiser(serializers.ModelSerializer):
#     url = serializers.CharField(source="master_subject.url")
#     background_code = serializers.CharField(source="master_subject.background_code")
#     class Meta:
#         model = Subject
#         fields = ['id','label','url','background_code']

class UserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()
    is_faculty = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    batches = serializers.SerializerMethodField()
    # faculty = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'mobile', 'auth_token','is_faculty','subjects', 'batches']

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
        #StudentSubject

    def get_is_faculty(self,obj):
        if obj.role==3:
            status = True
        else:
            status= False


        return status

    # def get_batches(self, obj):
    #     get_faculty_obj = Faculty.objects.filter(user_id=obj.id)
    #     if get_faculty_obj.exists():
    #         subjects = Subject.objects.filter(id__in=FacultySubject.objects.filter(faculty=get_faculty_obj[0]).values_list('subject_id'))
    #         return SubjectSerialiser(subjects,many=True).data

    def get_batches(self, obj):
        get_faculty_obj = Faculty.objects.filter(user_id=obj.id)
        if get_faculty_obj.exists():
            batches  = Batch.objects.filter(id__in=FacultyBatch.objects.filter(faculty = get_faculty_obj[0]).values_list('batch_id'))
            return BatchDetailsSerializer(batches,many=True).data
        
        student = Student.objects.filter(user_id=obj.id)
        if student.exists():
            return BatchDetailsSerializer([student.first().batch],many=True).data

        return None

    def get_subjects(self, obj):

        get_faculty_obj = Faculty.objects.filter(user_id=obj.id)
        if get_faculty_obj.exists():
            subjects = Subject.objects.filter(id__in=FacultySubject.objects.filter(faculty=get_faculty_obj.first()).values_list('subject_id'))
            return SubjectSerialiser(subjects,many=True).data
        
        student = Student.objects.filter(user_id=obj.id)
        if student.exists():
            subjects = Subject.objects.filter(id__in=StudentSubject.objects.filter(student=student.first()).values_list('subject_id'))
            return SubjectSerialiser(subjects,many=True).data
        

        return None
