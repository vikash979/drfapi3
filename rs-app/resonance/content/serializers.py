from .models import (
    Lecture, LectureTOCMapping, StudyMaterialFile, StudyMaterial
)
from users.models import (
    User
)
from institute.models import (Classs, Subject, Batch, Program, Phase, Sessions)
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination, _positive_int
from subject.models import TOC
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound


def dummyDict():
    d = dict()
    d['subject_lectures'] = {"information": {
                                "value": "70 %",
                                "message": "Your attendance record is good at",
                                "background_color": "#5454ff"}}
    return d


class TocSerializer(serializers.ModelSerializer):
    class Meta:
        model = TOC
        fields = ['id', 'level', 'label', 'parent_id']


class LectureTocMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureTOCMapping
        fields = '__all__'


class LecturePageNumberPagination(PageNumberPagination):

    page_size = 10
    def get_page_size(self, request):
        print(self.page_size_query_param, "page size query params")
        if self.page_size_query_param:
            print(request.data)
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size


    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        
        if request.method == "POST":
            page_number = request.data.get(self.page_query_param, 1)
        else:    
            page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)
    
    def get_paginated_response(self, data):
        d = dummyDict()
        d['pagination'] = OrderedDict([
             ('current_page', self.page.number),
             ('total_pages', self.page.paginator.num_pages),
        ])
        d['subject_lectures']['lectures'] = data
        return d


class BatchSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(BatchSerializer, self).to_representation(obj)
        return data['label']

    class Meta:
        model = Batch
        fields = ['label',]
        read_only_fields = ('label',)

class PhaseSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(PhaseSerializer, self).to_representation(obj)
        return data['label']

    class Meta:
        model = Phase
        fields = ['label',]


class ProgramSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(ProgramSerializer, self).to_representation(obj)
        return data['label']

    class Meta:
        model = Program
        fields = ['label',]


class SessionsSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(SessionsSerializer, self).to_representation(obj)
        return data['label']

    class Meta:
        model = Sessions
        fields = ['label',]


class SubjectSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(SubjectSerializer, self).to_representation(obj)
        return data['label']

    class Meta:
        model = Subject
        fields = ['label',]


class ClassSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(ClassSerializer, self).to_representation(obj)
        return data['label']

    class Meta:
        model = Classs
        fields = ['label',]


class UserModelSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        data = super(UserModelSerializer, self).to_representation(obj)
        return data['name']

    class Meta:
        model = User
        fields = ['name',]


class LectureSerializer(serializers.ModelSerializer):
    faculty = UserModelSerializer()
    classs = ClassSerializer()
    subject = SubjectSerializer()
    session = SessionsSerializer()
    program = ProgramSerializer()
    phase = PhaseSerializer()
    batch = BatchSerializer()
    # chapter_id = serializers.IntegerField(source='chapter')
    # chapter_title = serializers.CharField()
    important_label = serializers.SerializerMethodField(read_only=True)
    is_attended = serializers.SerializerMethodField(read_only=True)
    status_color = serializers.SerializerMethodField(read_only=True)
    nps_score = serializers.SerializerMethodField(read_only=True)
    batch_attendance = serializers.SerializerMethodField(read_only=True)
    batch_strength = serializers.SerializerMethodField(read_only=True)
    
    def get_nps_score(self, obj):
        return "8.1"

    def get_batch_attendance(self,obj):
        return "100%"

    def get_batch_strength(self,obj):
        return "100"

    class Meta:
        model = Lecture
        exclude = ['created_by', 'added_on', 'updated_on', 'object_status',]
        # read_only_fields = ('chapter_id',)
        depth = 1

    def get_important_label(self, obj):
        return "30 mins. left"

    def get_is_attended(self, obj):
        return 0

    def get_status_color(self, obj):
        return "#FFF00"
