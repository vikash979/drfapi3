from django.shortcuts import render, redirect
from django.core import serializers
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from common.choices import (
    QuestionCategoryChoices, DifficultyLevelChoices, AssessmentTimedChoices,
    AssessmentResultChoices, AssessmentSolutionVisibilityChoices, AssessmentResultChoices
)
from django.views.generic import TemplateView, ListView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView
)
from rest_framework.views import APIView
from .serializers import (
    FacultyTODOSerializer,LectureContentReleasingSerializer,LectureContentReleaseSerializer,
    DPPReleaseSerializer,LectureTopicsDeliveredSerializer,ExerciseCreateSerializer,ExerciseSerializer,
    AssessmentAttemptReviewSerializer, FacultyDPPReleaseSerializer
)
from rest_framework import permissions,authentication
from common.choices import (
    DifficultyLevelChoices, QuestionTypeChoices
)
from content.models import DPPPlanner
from content.models import Lecture,LectureTOCContent,LectureTOCMapping,AssessmentAttempt
from content.views import render_response
from subject.models import TOC
from apis.student.serializers import TOCSerializer, BaseTOCSerializer
from apis.content.views import TOCListView


class FacultyTodoListAPIView(generics.RetrieveAPIView):

    serializer_class = FacultyTODOSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, *args, **kwargs):
        return render_response(data=[], status=0, error=["Post method error, date field required, in format yyyy-mm-dd."])

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return render_response(data=serializer.data, error=[], status=1)
        


class FacultyExerciseListAPIView(generics.RetrieveAPIView):

    serializer_class = ExerciseSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, *args, **kwargs):
        return render_response(data=[], status=0, error=["Post method error, date field required, in format yyyy-mm-dd."])

    def post(self, *args, **kwargs):
        batch_id = self.request.data.get('batch_id', None)
        if batch_id:
            lecture = Lecture.objects.filter(batch_id=batch_id,faculty=self.request.user).first()
            lecture = Lecture.objects.first()
            serializer = self.get_serializer(lecture)
            return render_response(data=serializer.data, error=[], status=1)
        return render_response(data=[], status=0, error=["batch_id field required."])



class LectureContentReleasingAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    serializer_class = LectureContentReleasingSerializer

    queryset = LectureTOCMapping.objects.all()

    def get_queryset(self):
        tocs=LectureTOCMapping.objects.filter(lecture_id=self.request.data.get('lecture_id')).values_list('toc_id')
        return TOC.objects.filter(id__in=tocs)

    def post(self, request, *args, **kwargs):
        lecture_id = request.data.get('lecture_id', None)
        if lecture_id:
            return self.get(self, request, *args, **kwargs)
        return render_response(data=[], status=0, error=["lecture_id field required."])

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return render_response(data=serializer.data, error=[], status=1)



class LectureContentReleaseView(generics.CreateAPIView):

    queryset = LectureTOCMapping.objects.all()
    serializer_class = LectureContentReleaseSerializer
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
        print(validated_data, instance)
        
        data = {
            "data": {
                "Saved Successfully"
            },

            "errors":[],
            "status": 1
        }
        return Response(data)


class DPPReleaseView(LectureContentReleaseView):
    serializer_class = DPPReleaseSerializer


class LectureTOCDeliveredView(LectureContentReleaseView):
    serializer_class = LectureTopicsDeliveredSerializer

class ExerciseCreateView(LectureContentReleaseView):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
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
        
        return Response({"errors": serializer.errors, "status": 0})

    serializer_class = ExerciseCreateSerializer

class TOCContentView(TOCListView):

    def get_queryset(self):
        # print("data",self.request.data)
        #need to get subject id from batch and faculty mapping
        # lectures = Lecture.objects.filter(faculty=self.request.user,batch_id =self.request.data.get('batch_id', 0) )
        from users.models import FacultySubject
        subject_id = FacultySubject.objects.filter(faculty__user_id=self.request.user.id).first().subject_id
        return TOC.objects.filter(parent__isnull=True,subject_id=subject_id)
        # return TOC.objects.none()

    def post(self, request, *args, **kwargs):
        batch_id = request.data.get('batch_id', None)
        if batch_id:
            return self.get(self, request, *args, **kwargs)
        return render_response(data=[], status=0, error=["batch_id field required."])


class AssessmentAttemptReviewView(generics.RetrieveAPIView):

    queryset = AssessmentAttempt.objects.all()
    serializer_class = AssessmentAttemptReviewSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        assessment_id = request.data.get('assessment_id')
        if assessment_id:
            a=AssessmentAttempt.objects.all().first()
            serializer = self.get_serializer(a)
            data = {
                
                    'data': serializer.data,
                    "errors": [],
                    "status": 1
                }
            
            return Response(data)
        return render_response(data=[], status=0, error=["assessment_id required"])

    def get(self, *args, **kwargs):
        return render_response(data=[], status=0, error=["Method not implemented"])


class QuestionStudentResponsesListAPI(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    serializer_class = TOCSerializer

    queryset = TOC.objects.filter(parent__isnull=True)

    
    def post(self, request, *args, **kwargs):
        assessment_id = request.data.get('assessment_id', None)
        question_id = request.data.get('question_id', None)

        if assessment_id and question_id:
            return self.get(self, request, *args, **kwargs)
        return render_response(data=[], status=0, error=["assessment_id and question_id, both fields required."])

    # def list(self, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_queryset(), many=True)
    #     return render_response(data=serializer.data, error=[], status=1)

    def list(self, request, *args, **kwargs):
        responses = [
                    ["Rank", "Name", "Answer", "Result", "Attempts", "Avg. Time", "Score"],
                    ["1", "Radhika Sharma", "B", "Wrong", "1", "33s", "+12"],
                    ["2", "Radhika Sharma", "B", "Wrong", "1", "33s", "+12"],
                    ["3", "Radhika Sharma", "B", "Wrong", "1", "33s", "+12"],
                    ["4", "Radhika Sharma", "B", "Wrong", "1", "33s", "+12"],
                    ["5", "Radhika Sharma", "B", "Wrong", "1", "33s", "+12"],
                    ["6", "Radhika Sharma", "B", "Wrong", "1", "33s", "+12"],
                ]
        data = {
            'data':responses,
            "errors": [],
            "status": 1
        }
        return Response(data)

    
class FacultyDPPtoReleaseView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = FacultyDPPReleaseSerializer
    # allowed_methods = ['post']

    def get_queryset(self):
        import datetime
        lecture_id = self.request.data['lecture_id']
        lecture = Lecture.objects.get(id=lecture_id)
        next_date = datetime.datetime.today()
        next_date_lecture = Lecture.objects.filter(
            faculty=self.request.user, start_date_time__gt=lecture.start_date_time).order_by('start_date_time').first()
        if next_date_lecture:
            next_date = next_date_lecture.start_date_time
        queryset = DPPPlanner.objects.filter(faculty=self.request.user, start_date__lte=next_date)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            # return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        data = {
            "data": {
                "dpps": data
            },
            "status": 1,
            "errors": []
        }
        
        return Response(data)

    