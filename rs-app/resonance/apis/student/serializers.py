from rest_framework import serializers

from users.models import Student, User
from institute.models import Batch, Program, Phase
from subject.models import TOC
from content.models import Content, ContentTOCMapping


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile']


class PhaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phase
        fields = ['description', 'start_date', 'end_date']


class BatchSerializer(serializers.ModelSerializer):
    phase = PhaseSerializer()
    class Meta:
        model = User
        fields = ['description', 'time_slot', 'phase']


class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ['label', 'description', 'type']


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    program = ProgramSerializer()
    batch = BatchSerializer()
    class Meta:
        model = Student
        fields = [
            'user', 'roll_no', 'profile_picture', 'Unread_notice_count', 'date_of_birth',
            'gender', 'father_name', 'father_email', 'father_mobile', 'mother_name',
            'mother_email', 'mother_mobile', 'status', 'program', 'batch']


{
    "data": {
        "name": "mahesh",
        "role_number": 75354,
        "profile_picture": "image_url",
        "Unread_notice_count": 123,
        "student_program": {
            "id": 2,
            "name": "MyProgram"
        },
        "phase": {
            "id": 1,
            "name": "phase1"
        },
        "current_batch": {
            "id": 5,
            "name": "pythonasdf"
        }
    },
    "error": [],
    "status": 1
}

class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = [
            'description', 'faculty_releasable', 'faculty_only', 'title',  'unique_code',
            'content_type', 'content_subtype',
        ]


class ContentTOCMappingSerializer(serializers.ModelSerializer):
    # content = ContentSerializer()
    description = serializers.CharField(source="content.description")
    faculty_releasable = serializers.BooleanField(source="content.faculty_releasable")
    faculty_only =  serializers.BooleanField(source="content.faculty_only")

    unique_code = serializers.CharField(source="content.unique_code")
    content_type = serializers.IntegerField(source="content.content_type")
    content_subtype = serializers.IntegerField(source="content.content_subtype")
    id = serializers.SerializerMethodField()
    is_released = serializers.SerializerMethodField()
    status_color = serializers.SerializerMethodField()
    

    def get_status_color(self,obj):
        return "#000000"

    def get_id(self,obj):
        return obj.content_id
    
    def get_is_released(self,obj):
        return False
    

    class Meta:
        model = ContentTOCMapping
        fields = ['id','description','faculty_only', 'faculty_releasable','unique_code',
            'title', 'content_type', 'content_subtype', 'level', 'ref_id','is_released',
            'status_color','content_id'
        ]



class TOCSerializerSmall(serializers.ModelSerializer):
    level_name = serializers.CharField(source="get_level_display")
    content = serializers.SerializerMethodField()
    status_color = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    
    def get_content(self, obj):
        return ContentTOCMappingSerializer(ContentTOCMapping.objects.filter(ref_id=obj.id).exclude(level__in=[10,20]), many=True).data

    

    class Meta:
        model = TOC
        fields = ['id','label', 'order', 'level', 'level_name','subject', 'content','status_color', 'content']

    def get_content(self, obj):
        return ContentTOCMappingSerializer(ContentTOCMapping.objects.filter(ref_id=obj.id).exclude(level__in=[10,20]), many=True).data

    def get_status_color(self,obj):
        return "#000000"

class TOCSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()
    level_name = serializers.CharField(source="get_level_display")
    content = serializers.SerializerMethodField()
    
    def get_content(self, obj):
        return ContentTOCMappingSerializer(ContentTOCMapping.objects.filter(ref_id=obj.id).exclude(level__in=[10,20]), many=True).data

    class Meta:
        model = TOC
        fields = [
            'id','label', 'order', 'level', 'level_name','parent', 'subject', 'created_by', 'chapters',
            'content'
            ]


    def get_chapters(self, obj):
        if obj.level == 0:
            return self.get_chapter(obj)
        elif obj.level == 1:
            return self.get_topics(obj)
        elif obj.level == 2:
            return self.get_sub_topics(obj)

    def get_chapter(self, obj):
        chapters = []

        for chapter in TOC.objects.filter(parent=obj):
            data = TOCSerializerSmall(chapter).data
            data['topics'] = self.get_topics(chapter)
            chapters.append(data)
        return chapters

    def get_topics(self, obj):
        topics = []
        for topic in TOC.objects.filter(parent=obj):
            data = TOCSerializerSmall(topic).data
            data['subtopics'] = self.get_sub_topics(topic)
            topics.append(data)
        return topics

    def get_sub_topics(self, obj):
        sub_topics = []
        for subtopic in TOC.objects.filter(parent=obj):
            sub_topics.append(TOCSerializerSmall(subtopic).data)
        return sub_topics


class BaseTOCSerializer(serializers.Serializer):

    units = serializers.SerializerMethodField()

    def get_toc_detail(self, obj):
        if obj.level == 0:
            return self.get_chapters(obj)
        elif obj.level == 1:
            return self.get_topics(obj)
        elif obj.level == 2:
            return self.get_sub_topics(obj)

    def get_chapters(self, obj):
        chapters = []

        for chapter in TOC.objects.filter(parent=obj):
            data = TOCSerializerSmall(chapter).data
            data['topics'] = self.get_topics(chapter)
            chapters.append(data)
        return chapters

    def get_topics(self, obj):
        topics = []
        for topic in TOC.objects.filter(parent=obj):
            data = TOCSerializerSmall(topic).data
            data['subtopics'] = self.get_sub_topics(topic)
            topics.append(data)
        return topics

    def get_sub_topics(self, obj):
        sub_topics = []
        for subtopic in TOC.objects.filter(parent=obj):
            sub_topics.append(TOCSerializerSmall(subtopic).data)
        return sub_topics

    def get_units(self, obj):
        units = []
        for unit in TOC.objects.filter(parent__isnull=True):
            unit_data = TOCSerializerSmall(unit).data
            unit_data['chapters'] = self.get_toc_detail(unit)
            units.append(unit_data)
        return units
        # return unit_data


class DashboardSerializer(serializers.ModelSerializer):
    completed_items = serializers.SerializerMethodField()
    
    def get_completed_items(self,obj):
        return obj.user.name


    # def get_batch(self,obj):

    class Meta:
        model=Student
        fields = ["completed_items"]
        related_fields = ['user']
