from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from content.models import StudyMaterial, Content, Question, AssessmentAttempt
from apis.student.serializers import TOCSerializer, BaseTOCSerializer
from .serializers import StudyMaterialSerializer, ContentSerializer, VideoSerializer, VideoDetailSerializer
from subject.models import TOC
from content.views import render_response
from content.models import Assessment, DPPPlanner, NotesAccessLog, VideoAccessLog, Language, QuestionOptions

from .serializers import (
    SolvedExamplesSerializer, AssessmentPreviewSerializer, AssesmentAttemptSerializer,
    AssesmentQuestionSaveSerializer, AssessmentAttemptSerializer, DPPPlannerSerializer,
    ExerciseSerializer, FacultyToDoSerializer, AssessmentScoreCardSerializer,
    LanguageSerializerFull
    )


class NotesAccessAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        content_id = request.data.get('content_id')
        file_id = request.data.get('file_id')
        checked_pages = request.data.get('checked_pages')
        last_page = request.data.get('last_page')
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')

        if content_id and file_id and checked_pages and last_page and start_date_time and end_date_time:
            NotesAccessLog.objects.create(content_id=content_id,file_id=file_id,checked_pages=checked_pages,last_page=last_page,
                start_date_time=start_date_time,end_date_time=end_date_time,user=request.user)
            return render_response(data="Logged successfully.", error=[], status=1)
        
        return render_response(data=[], error=["All fields are required : content_id, file_id, checked_pages, last_page, start_date_time, end_date_time "], status=0)

class NoteViewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        content_id_data = request.data.get('content_id', None)
        if content_id_data:
            content_obj = Content.objects.get(id=int(request.data.get('content_id')))
            return render_response(data=ContentSerializer(content_obj).data, status=1, error=[])
        return render_response(data=[], status=0, error=["content_id field required."])

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class VideoViewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        content_id_data = request.data.get('content_id', None)
        if content_id_data:
            content_obj = Content.objects.get(id=int(request.data.get('content_id')))
            return render_response(data=VideoDetailSerializer(content_obj).data, status=1, error=[])
        return render_response(data=[], status=0, error=["content_id field required."])

class VideoAccessAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        content_id = request.data.get('content_id', None)
        file_id = request.data.get('file_id', None)
        file_duration_viewed = request.data.get('file_duration_viewed', None)
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')

        if content_id and file_id and file_duration_viewed and start_date_time and end_date_time:
            VideoAccessLog.objects.create(content_id=content_id,file_id=file_id,file_duration_viewed=file_duration_viewed,
                start_date_time=start_date_time,end_date_time=end_date_time,user=request.user)
            return render_response(data="Logged successfully.", error=[], status=1)
        return render_response(data=[], error=["All fields are required : content_id, file_id, file_duration_viewed."], status=0)

class TOCListView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    serializer_class = TOCSerializer

    queryset = TOC.objects.filter(parent__isnull=True)

    def get_queryset(self):
        # print("data",self.request.data)
        return TOC.objects.filter(parent__isnull=True,subject_id=self.request.data.get('subject_id'))

    def post(self, request, *args, **kwargs):
        subject_id = request.data.get('subject_id', None)
        if subject_id:
            return self.get(self, request, *args, **kwargs)
        return render_response(data=[], status=0, error=["subject_id field required."])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            'data':{
                'toc_data': {"units" :serializer.data},

                "current_open_toc_id": 1,
                "information":{
                        "value": "70 %",
                        "message": "Batch is doing good with",
                        "background_color": "#bad53c"
                    }
            },
            "errors": [],
            "status": 1
        }
        return Response(data)

class VideoView(generics.RetrieveAPIView):

    queryset = StudyMaterial.objects.all()
    permission_classes = []
    serializer_class = VideoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {"data": serializer.data, "errors": [], "status": 1}
        return Response(data)


class SolvedExampleView(APIView):
    queryset = Assessment.objects.all()
    serializer_class = SolvedExamplesSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'content_id'	
    lookup_url_kwarg = "content_id" 

    def get_queryset(self):
        return self.queryset

    def post(self, request, *args, **kwargs):
        pk = request.data.get('content_id', 0)
        self.kwargs['content_id'] = pk
        return self.retrieve(request, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if 'language_id' in self.request.data:
            kwargs['context']['language_id'] = self.request.data['language_id']
        return serializer_class(*args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "data": serializer.data,
            "errors": [],
            "status": 1}
        return Response(data)

    def get_serializer_class(self):

        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


class AssesmentPreviewView(generics.RetrieveAPIView):
    serializer_class = AssessmentPreviewSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    lookup_url_kwarg = "content_id" 
    lookup_field="content_id"
    
    def get_queryset(self):
        return Assessment.objects.all()

    def post(self, request, *args, **kwargs):
        content_id = request.data.get('content_id', 0)
        self.kwargs['content_id'] = content_id
        return self.retrieve(request, *args, **kwargs)


    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "data": serializer.data,
            "errors": [],
            "status": 1
        }
        return Response(data)


class AssesmentAttemptView(generics.RetrieveAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'content_id'


    queryset = Content.objects.all()
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    
    serializer_class = AssesmentAttemptSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if 'language_id' in self.request.data:
            kwargs['context']['language_id'] = self.request.data['language_id']
        kwargs['context']['assessment'] = args[0].assessment_set.first()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        content_id = request.data.get('content_id', 0)
        self.kwargs['content_id'] = content_id
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "data": serializer.data,
            "errors": [],
            "status": 1
        }
        return Response(data)


class AttempQuestionSaveView(generics.CreateAPIView):

    queryset = Question.objects.all()
    serializer_class = AssesmentQuestionSaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        validated_data = serializer.validated_data
        
        # question_id=instance.question.question.values_list('question__question_id')
        correct_options = QuestionOptions.objects.filter(question_id=instance.question.question_id,is_correct=True)
        video_file = ""
        if correct_options.first().questionoptionsexplanation_set.first().video:
            video_file = correct_options.first().questionoptionsexplanation_set.first().video.url

        data = {
            "data": {
		        "time_taken": instance.time_taken,
		        "score": instance.marks,
		        "marks": instance.question.marks,
		        "is_correct": instance.is_correct,
		        "selected_option_id": validated_data.get('selected_option_id',''),
		        "correct_option_id": correct_options.values_list('id'),
		        "solution": {
			        "statement": correct_options.first().questionoptionsexplanation_set.first().explanation,
			        "video_file": video_file
		        }
	        },

            "errors":[],
            "status": 1
        }
        return Response(data)


class AssesmentAttemptSaveView(APIView):
    queryset = Question.objects.all()
    serializer_class = AssessmentAttemptSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": {
                    "resultData": "Logged Successfully"
                },
                "status": 1,
                "errors": []
            }
            return Response(data)
        errors = []
        for k,v in serializer.errors.items():
            errors.append("{}: {}".format(k,v))
        return Response({"errors": errors, "status": 0})



from .serializers import AssessmentAttemptReviewSerializer
class AssessmentAttemptReviewView(generics.RetrieveAPIView):

    queryset = AssessmentAttempt.objects.all()
    serializer_class = AssessmentAttemptReviewSerializer

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        content_id = request.data.get('content_id')
        if content_id:
            a=AssessmentAttempt.objects.filter(assessment__content_id=content_id,user=request.user).last()
            # a=AssessmentAttempt.objects.all().first()
            serializer = self.get_serializer(a)
            data = {
                
                    'data': serializer.data,
                    "errors": [],
                    "status": 1
                }
            
            return Response(data)
        return render_response(data=[], status=0, error=["content_id required"])

    def get(self, *args, **kwargs):
        return render_response(data=[], status=0, error=["Method not implemented"])


class DPPListView(generics.ListAPIView):

    queryset = Assessment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    serializer_class = DPPPlannerSerializer

    def post(self, request, *args, **kwargs):
        subject_id = request.data.get('subject_id', None)
        if subject_id:
            return self.get(self, request, *args, **kwargs)
        return render_response(data=[], status=0, error=["subject_id field required."])
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset)
        data = {
            
                'data': serializer.data,
                "errors": [],
                "status": 1
            }
        
        return Response(data)


class ExerciseListView(generics.ListAPIView):

    queryset = Assessment.objects.all()[:1]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    
    serializer_class = ExerciseSerializer

    def post(self, request, *args, **kwargs):
        subject_id = request.data.get('subject_id', None)
        if subject_id:
            return self.get(self, request, *args, **kwargs)
        return render_response(data=[], status=0, error=["subject_id field required."])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            
                'data': serializer.data,
                "errors": [],
                "status": 1
            }
        
        return Response(data)


class FacultyToDoView(generics.ListAPIView):

    queryset = DPPPlanner.objects.all()[:1]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = FacultyToDoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            
                'data': serializer.data,
                "errors": [],
                "status": 1
            }
        
        return Response(data)



class AssessmentScorecardView(generics.RetrieveAPIView):

    queryset = Assessment.objects.all()
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    serializer_class = AssessmentScoreCardSerializer
    
    def post(self, request, *args, **kwargs):
        content_id = request.data.get('content_id')
        if content_id:
            a=Assessment.objects.first()
            serializer = self.get_serializer(a)
            data = {
                
                    'data': serializer.data,
                    "errors": [],
                    "status": 1
                }
            
            return Response(data)
        return render_response(data=[], status=0, error=["content_id required"])

    def get(self, *args, **kwargs):
        return render_response(data=[], status=0, error=["Method not implemented"])

    # def post(self, *args, **kwargs):
    #     date = self.request.data.get('date', None)
    #     if date:
    #         serializer = self.get_serializer(self.request.user)
    #         return render_response(data=serializer.data, error=[], status=1)
    #     return render_response(data=[], status=0, error=["date field required, in format yyyy-mm-dd."])
    #     


class AssesmentLangagesListView(generics.ListAPIView):

    queryset = Language.objects.all()
    serializer_class = LanguageSerializerFull