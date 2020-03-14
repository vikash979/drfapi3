from rest_framework import serializers

from content.models import Content, StudyMaterial, StudyMaterialFile, Language
from content.models import Assessment, AssessmentSection, AssessmentSectionQuestion
from content.models import Question, QuestionOptions, QuestionOptionsExplanation, QuestionOptionsStatement, QuestionStatement
from content.models import QuestionOptionsStatement, AssessmentAttempt, AssesmentAttemptQuestion
from content.serializers import *
from content.models import Lecture,ContentTOCMapping,LectureTOCContent, DPPPlanner
from datetime import date, datetime, time
from apis.student.serializers import BaseTOCSerializer,TOCSerializerSmall
from apis.content.serializers import LanguageSerializer
from common.choices import ContentSubtypeChoices
from datetime import datetime, timedelta
import pytz

class TodoLectureSerializer(serializers.ModelSerializer):
    classs = serializers.SerializerMethodField(read_only=True)
    batch = serializers.SerializerMethodField(read_only=True)
    important_label = serializers.SerializerMethodField(read_only=True)
    activities =  serializers.SerializerMethodField(read_only=True)

    def get_activities(self,obj):
        sm_released = obj.lecturetoccontent_set.filter(is_released=True,content_toc__content__content_subtype__in=[ContentSubtypeChoices.NOTES,ContentSubtypeChoices.VIDEO]).count()
        dpp_released = obj.lecturetoccontent_set.filter(is_released=True,content_toc__content__content_subtype=ContentSubtypeChoices.DAILY_PRACTICE_PROBLEMS).count()
        ex_released = obj.lecturetoccontent_set.filter(is_released=True,content_toc__content__content_subtype=ContentSubtypeChoices.EXERCISE).count()
        activites =[{
                    "name": "Study Material",
                    "is_released": sm_released,
                    "value": "{} Released".format(sm_released)
                },
                {
                    "name": "Topics",
                    "is_delivered": obj.lecturetocmapping_set.filter(delivered_status=1).count(),
                    "value": "{} Topics Delivered".format(obj.lecturetocmapping_set.filter(delivered_status=1).count())
                },
                {
                    "name": "Exercise",
                    "is_released": ex_released,
                    "value": "{} Released".format(ex_released)
                },
                {
                    "name": "DPP",
                    "is_released": sm_released,
                    "value": "{} Released".format(dpp_released)
                }
                ]
        return activites

    def get_important_label(self,obj):
        now = datetime.now().replace(tzinfo=pytz.UTC)
        lecture_date = obj.start_date_time.replace(tzinfo=pytz.UTC)

        if now < lecture_date and now > (lecture_date - timedelta(hours=4)):
            delta = obj.start_date_time - now
            return "{}h, {}m remaining ".format(delta.seconds // 3600, delta.seconds // 60 % 60)
        return ""

    def get_classs(self,obj):
        return obj.classs.label
    
    def get_batch(self,obj):
        return obj.batch.label

    class Meta:
        model = Lecture
        fields = ['id','title', 'room','start_date_time','duration_hrs','classs','batch','is_tentative',
            'important_label','activities']
    
class FacultyTODOSerializer(serializers.Serializer):

    pending_action_dates = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    lectures = serializers.SerializerMethodField(read_only=True)

    def get_lectures(self,obj):
        request_date = self.context.get('request').data.get('date',False)
        user = self.context.get('request').user
        pub_date = date.today()
        if request_date:
            request_date = datetime.strptime(request_date, "%Y-%m-%d")
            pub_date = request_date.date()
        
        min_pub_date_time = datetime.combine(pub_date, time.min) 
        max_pub_date_time = datetime.combine(pub_date, time.max)  
        
        q = Lecture.objects.all()
        q = q.filter(faculty=user,start_date_time__gte=min_pub_date_time,\
            start_date_time__lte=max_pub_date_time)

        lectures = []
        for lecture in q:
            data = TodoLectureSerializer(lecture).data
            lectures.append(data)
        return lectures
    
    def get_date(self,obj):
        request_date = self.context.get('request').data.get('date',False)
        if request_date:
            return datetime.strptime(request_date, "%Y-%m-%d").date()
        return date.today()

    def get_pending_action_dates(self,obj):
        pending_dates = []
        lectures = Lecture.objects.filter(faculty=self.context['request'].user, is_delivered=True)
        for lecture in lectures:  # code must be optimize, do it in query instead of loop
            if not lecture.lecturetoccontent_set.filter(is_released=True).exists() or lecture.lecturetocmapping_set.filter(delivered_status=0).exists():
                    pending_dates.append(lecture.start_date_time)
        return pending_dates



        # pendig_toc_content = lectures.exclude(lecturetoccontent__is_released=True)

        # return list(Lecture.objects.filter(
        #     is_delivered=True, ).filter(
        #         lecturetocmapping__delivered_status=0).values_list("start_date_time", flat=True))

        # return ['2020-01-01','2020-01-02']

   
class ExerciseSerializer(serializers.Serializer):
    summary = serializers.SerializerMethodField(read_only=True)
    summary_note = serializers.SerializerMethodField(read_only=True)
    exercises = serializers.SerializerMethodField(read_only=True)
    information = serializers.SerializerMethodField(read_only=True)


    def get_information(self, obj):
        return {
            "value": "70 %", "message": "Batch is doing good with",
            "background_color": "#bad53c"
        }

    def get_exercises(self,obj):
        batch_id = self.context.get('request').data.get('batch_id',False)
        return [
                {
                    "title":"E002 - Lone Pair Bonds",
                    "released":"2020-01-01T12:00:00",
                    "stats":[
                            {"type":"attempted","name":"Attempted","value":"90/100"},
                            {"type":"avg_time", "name":"Avg Time","value":"22s"},
                            {"type":"correct","name":"Correct","value":"20"}
                        ]
                },
                {
                    "title":"E001 - ALone Pair Bonds",
                    "released":"2020-01-01T12:00:00",
                    "stats":[
                            {"type":"attempted","name":"Attempted","value":"90/100"},
                            {"type":"avg_time", "name":"Avg Time","value":"22s"},
                            {"type":"correct","name":"Correct","value":"20"}
                        ]
                }
            ]

    def summary_note(self,obj):
        return "This is average of all students"

    def get_summary(self,obj):
        return [
                {"type":"attempted","name":"Attempted","value":"90/100"},
                {"type":"avg_time", "name":"Avg Time","value":"22s"},
                {"type":"correct","name":"Correct","value":"20"}
            ]
        

class LectureContentReleasingSerializer(serializers.Serializer):
    toc_data = serializers.SerializerMethodField(read_only=True)
    
    def get_toc_data(self,obj):
        return TOCSerializerSmall(obj).data
        

class LectureContentReleaseSerializer(serializers.Serializer):

    lecture_id = serializers.IntegerField()
    toc_data = serializers.JSONField()
    
    def create(self, validated_data):
        lecture_id = validated_data['lecture_id']
        toc_data = validated_data['toc_data']
        print("toc_data",toc_data)
        for tocid in toc_data:
            for content_id in toc_data[tocid]:
                ctm = ContentTOCMapping.objects.filter(ref_id=tocid,content_id=content_id).first()
                ltc, created = LectureTOCContent.objects.get_or_create(
                    lecture_id=lecture_id,content_toc=ctm)
                ltc.is_released = True
                ltc.save()
        return True


class DPPReleaseSerializer(serializers.Serializer):

    content_id = serializers.IntegerField()
    lecture_id = serializers.IntegerField()
    
    def create(self, validated_data):
        lecture_id = validated_data['lecture_id']
        content_id = validated_data['content_id']
        
        lecture = Lecture.objects.get(pk=lecture_id)
        dpp = DPPPlanner.objects.filter(assessment__content_id=content_id,batch_id=lecture.batch_id)
        if dpp.exists():
            dpp=dpp.first() 
            dpp.is_released = True
            dpp.save()
        return True


class LectureTopicsDeliveredSerializer(serializers.Serializer):

    toc_id = serializers.IntegerField()
    lecture_id = serializers.IntegerField()
    
    def create(self, validated_data):
        lecture_id = validated_data['lecture_id']
        toc_id = validated_data['toc_id']
        
        ltm = LectureTOCMapping.objects.filter(lecture_id=lecture_id,toc_id=toc_id)
        if ltm.exists():
            ltm = ltm.first()
            ltm.is_delivered = True
            ltm.save()
        return True


class ExerciseCreateQuestionSerializer(serializers.Serializer):

    question_id = serializers.IntegerField()
   

class ExerciseCreateSerializer(serializers.Serializer):

    questions = ExerciseCreateQuestionSerializer(many=True)
    title = serializers.CharField()
    due_date = serializers.DateField()
    lecture_id = serializers.IntegerField()
    assessment_id = serializers.IntegerField()

    
    def create(self, validated_data):
        questions = validated_data['questions']
        title = validated_data['title']
        due_date = validated_data['due_date']
        lecture_id = validated_data['lecture_id']

        lecture = Lecture.objects.get(pk=lecture_id)
        unique_code = "EX: " + lecture.title
        c = Content.objects.create(content_type=1,content_subtype=1,unique_code=unique_code,created_by=self.request.user)
        a = Assessment.objects.get(pk=assessment_id)
        a.id = None
        a.title = title
        a.unique_code ="{}:{}".format(a.unique_code,lecture.id)
        a.save()

        asec = AssessmentSection.objects.create(title="Section 1",assessment=a) 

        for question in questions:
            question_id = question['question_id']
            AssessmentSectionQuestion.objects.create(question_id=question,assessment_section=asec)

        return a.title


class QuestionOptionsStatementSerializer(serializers.ModelSerializer):

    is_correct = serializers.BooleanField(source="question_option.is_correct")
    completion_percentage = serializers.SerializerMethodField()  

    def get_completion_percentage(self,obj):
        return 20

    class Meta:
        model = QuestionOptionsStatement
        fields = ["id", "statement",  "is_correct","completion_percentage"]

class AssessmentAttemptSectionQuestionSerializer(serializers.ModelSerializer):

    uid = serializers.CharField(source="question.uid")
    question_type = serializers.CharField(source="question.get_question_type_display")
    question_type_id = serializers.CharField(source="question.question_type")
    duration_seconds = serializers.IntegerField(source="question.duration_seconds")
    marks = serializers.FloatField(source="question.marks")
    difficulty = serializers.CharField(source="question.difficulty")
    statement = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    hint_message = serializers.SerializerMethodField()    
    
    class Meta:
        model = AssessmentSectionQuestion
        fields = ['id','negative_marking_per_q', 'question', 'uid', 'question_type','question_type_id',
        'duration_seconds', 'marks', 'difficulty', 'statement',
        'options', 'hint_message']

   
    def get_hint_message(self, obj):
        return None
    def get_statement(self, obj):
        if 'language_id' in self.context:
            if obj.question.questionstatement_set.filter(language_id=self.context['language_id']).exists():
                return obj.question.questionstatement_set.filter(
                    language_id=self.context['language_id']).first().statement
        
        return obj.question.questionstatement_set.first().statement

    def get_options(self, obj):
        options = QuestionOptionsStatement.objects.filter(
                question_option__question_id=obj.question_id)
        options = options.filter( language_id=self.context.get('language_id',1))
        return QuestionOptionsStatementSerializer(options, many=True, context=self.context).data

    



class AssesmentAttemptSectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSection
        fields = ['id', 'title', 'instructions', 'questions']

    def get_questions(self, obj):
        return AssessmentAttemptSectionQuestionSerializer(obj.assessmentsectionquestion_set, many=True).data
        # return list(obj.assessmentsectionquestion_set.values_list('id', flat=True))

class AssessmentAttemptReviewSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()
    # questions = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentAttempt
        fields = [
            "assessment", "user", "content", "language", "total_questions", 
            "attempted_questions", "visited_questions", "duration", "marks_obtained",
            "is_passed", "submit_date", "is_latest", "is_dynamic", "is_attempt", 
            "is_faculty_reviewed", "reviewed_date", "reviewed_by", "is_submitted", 
            "submission_reason",   'sections', 

        ]

    def get_language(self, obj):
        return LanguageSerializer(Language.objects.all(), many=True).data
    
   
    def get_sections(self, obj):
        sections = []
        for section in obj.assessment.assessmentsection_set.all():
            data = AssesmentAttemptSectionSerializer(section, context={"attempt": obj}).data
            sections.append(data)
            
        return sections
        
    


class FacultyDPPReleaseSerializer(serializers.ModelSerializer):
    total_questions = serializers.IntegerField(source="assessment.total_questions")
    unique_code = serializers.CharField(source="assessment.uid")

    class Meta:
        model = DPPPlanner
        fields = ['title', 'is_released', 'duration_mins', 'total_questions', 'unique_code']