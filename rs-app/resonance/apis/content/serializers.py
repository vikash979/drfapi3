from rest_framework import serializers

from content.models import Content, StudyMaterial, StudyMaterialFile, Language
from content.models import Assessment, AssessmentSection, AssessmentSectionQuestion
from content.models import Question, QuestionOptions, QuestionOptionsExplanation, QuestionOptionsStatement, QuestionStatement
from content.models import QuestionOptionsStatement, AssessmentAttempt, AssesmentAttemptQuestion
from content.models import DPPPlanner,AssessmentAttempt
from django.db.models import F, Sum, FloatField, Avg
from common.choices import AssessmentSolutionVisibilityChoices, AssessmentTimedChoices
from users.models import User, Student
class LanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Language
        fields = ['id', 'name']

class StudyMaterialFileSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    publish_status = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    view_analytics = serializers.DictField()
    file_url = serializers.ImageField()
    class Meta:
        model = StudyMaterialFile
        fields = [
            'publish_status', 'language', 'label', 'file_url', 'view_analytics'
        ]

    def get_label(self, obj):
        return obj.content

    def get_publish_status(self, obj):
        return obj.get_publish_status_display()


class StudyMaterialSerializer(serializers.ModelSerializer):
    file_details = StudyMaterialFileSerializer(source="files", many=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = StudyMaterial
        fields = [
            'type', 'title', 'downloadable', 'file_details'
        ]

    def get_type(self, obj):
        return obj.get_type_display()


class ContentViewAnalyticsSerializer(serializers.Serializer):

    file_id =  serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    last_view = serializers.SerializerMethodField()
    total_time_spent = serializers.SerializerMethodField()

    def get_file_id(self, obj):
        return 1

    def get_completion_percentage(self, obj):
        return "11.11%"

    def get_last_view(self, obj):
        return "2017-01-03 12:47:32"

    def get_total_time_spent(self, obj):
        return "1 hr"


class VideoFileSerializer(serializers.ModelSerializer):

    language_title = serializers.SerializerMethodField()
    class Meta:
        model = StudyMaterialFile
        fields = [
            'publish_status', 'language', 'content', 'file', 'language_title'
        ]

    def get_type(self, obj):
        return obj.get_type_display()

    def get_language_title(self, obj):

        return "Hindi"


class VideoSerializer(serializers.ModelSerializer):

    duration = serializers.SerializerMethodField()
    content_path = VideoFileSerializer(source="files", many=True)
    content_view_analytics = serializers.SerializerMethodField()

    class Meta:
        model = StudyMaterial
        fields = ['type', 'title', 'downloadable', 'faculty_only', 'content_path', 'duration', 'content_view_analytics']

    def get_duration(self, obj):
        return "3 Hours"

    def get_content_view_analytics(self, obj):

        return [ContentViewAnalyticsSerializer({"key": "value"}).data]


class ContentSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    content_subtype = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Content
        fields = [
            'title', 'unique_code', 'content', 'content_type','content_subtype', 'description', 'faculty_releasable',
            'faculty_only',
        ]

    def get_content(self, obj):
        if obj.content_type == 1:
            get_study_matrial_obj = StudyMaterial.objects.get(content_id=obj.id)
            return StudyMaterialSerializer(get_study_matrial_obj).data

    def get_content_type(self, obj):
        return obj.get_content_type_display()

    def get_content_subtype(self, obj):
        return obj.get_content_subtype_display()


class VideoDetailSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    content_subtype = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Content
        fields = [
            'title', 'unique_code', 'content', 'content_type','content_subtype', 'description', 'faculty_releasable',
            'faculty_only',
        ]

    def get_content(self, obj):
        if obj.content_type == 1:
            get_study_matrial_obj = StudyMaterial.objects.get(content_id=obj.id)
            return StudyMaterialSerializer(get_study_matrial_obj).data

    def get_content_type(self, obj):
        return obj.get_content_type_display()

    def get_content_subtype(self, obj):
        return obj.get_content_subtype_display()


class QuestionOptionsExplanationSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionOptionsExplanation
        fields = ['id', 'explanation']

class QuestionOptionsStatementSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source="question_option.id")
   
    class Meta:
        model = QuestionOptionsStatement
        fields = ["id", "statement"]

   
# class QuestionOptionsStatementSerializer(serializers.ModelSerializer):

#   is_correct = serializers.BooleanField(source="question_option.is_correct")

#   class Meta:
#       model = QuestionOptionsStatement
#       fields = ["id", "statement",  "is_correct"]



class QuestionOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionOptions
        fields = ['is_correct']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = [
            "uid", "question_type", "duration_seconds", "marks", "negative_marking", "source", 
            "difficulty"
        ]


class AssessmentSectionQuestionSerializer(serializers.ModelSerializer):

    uid = serializers.CharField(source="question.uid")
    question_type = serializers.CharField(source="question.get_question_type_display")
    duration_seconds = serializers.IntegerField()
    marks = serializers.FloatField()
    negative_marking = serializers.IntegerField(source="negative_marking_per_q")
    difficulty = serializers.CharField(source="question.difficulty")
    statement = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    # correct_answers = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSectionQuestion
        fields = ['id', 'uid', 'question_type',
        'duration_seconds', 'marks', 'negative_marking', 'difficulty', 'statement',
        'options', 'explanation']

    def get_statement(self, obj):
        language_id = self.context.get('language_id',1)#default english 
        if obj.question.questionstatement_set.filter(language_id=language_id).exists():
                return obj.question.questionstatement_set.filter(
                    language_id=language_id).first().statement
        return obj.question.questionstatement_set.first().statement

    def get_options(self, obj):
        language_id = self.context.get('language_id',1)#default english
        options = QuestionOptionsStatement.objects.filter(
                question_option__question_id=obj.question_id)
        options = options.filter( language_id=language_id)
        
        self.context['assessment'] = obj.assessment_section.assessment
        return QuestionOptionsStatementSerializer(options, many=True, context=self.context).data

    # def get_correct_answers(self, obj):
    #   queryset =  QuestionOptionsStatement.objects.filter(
    #           question_option__question_id=obj.question_id,
    #           question_option__is_correct=True)
    #   if 'language_id' in self.context:
    #       queryset = queryset.filter(language_id=self.context['language_id'])

    #   return QuestionOptionsStatementSerializer(queryset, many=True, context=self.context).data

    def get_explanation(self, obj):
        language_id = self.context.get('language_id',1)#default english 
        
        queryset = QuestionOptionsExplanation.objects.filter(
                question_option__question_id=obj.question_id)
        queryset = queryset.filter(language_id=language_id)

        return QuestionOptionsExplanationSerializer(queryset, many=True).data


class AssessmentSectionSerializer(serializers.ModelSerializer):

    questions = AssessmentSectionQuestionSerializer(
        many=True, source="assessmentsectionquestion_set")

    class Meta:
        model = AssessmentSection
        fields = ['title', 'questions']

class SEQuestionOptionsStatementSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source="question_option.id")
    is_correct = serializers.BooleanField(source="question_option.is_correct")
    class Meta:
        model = QuestionOptionsStatement
        fields = ["id", "statement","is_correct"]


class SESectionQuestionSerializer(serializers.ModelSerializer):

    uid = serializers.CharField(source="question.uid")
    question_type = serializers.CharField(source="question.get_question_type_display")
    duration_seconds = serializers.IntegerField()
    marks = serializers.FloatField()
    negative_marking = serializers.IntegerField(source="negative_marking_per_q")
    difficulty = serializers.CharField(source="question.difficulty")
    statement = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    # correct_answers = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSectionQuestion
        fields = ['id', 'uid', 'question_type',
        'duration_seconds', 'marks', 'negative_marking', 'difficulty', 'statement',
        'options', 'explanation']

    def get_statement(self, obj):
        language_id = self.context.get('language_id',1)#default english 
        if obj.question.questionstatement_set.filter(language_id=language_id).exists():
                return obj.question.questionstatement_set.filter(
                    language_id=language_id).first().statement
        return obj.question.questionstatement_set.first().statement

    def get_options(self, obj):
        language_id = self.context.get('language_id',1)#default english
        options = QuestionOptionsStatement.objects.filter(
                question_option__question_id=obj.question_id)
        options = options.filter( language_id=language_id)
        
        self.context['assessment'] = obj.assessment_section.assessment
        return SEQuestionOptionsStatementSerializer(options, many=True, context=self.context).data

    # def get_correct_answers(self, obj):
    #   queryset =  QuestionOptionsStatement.objects.filter(
    #           question_option__question_id=obj.question_id,
    #           question_option__is_correct=True)
    #   if 'language_id' in self.context:
    #       queryset = queryset.filter(language_id=self.context['language_id'])

    #   return QuestionOptionsStatementSerializer(queryset, many=True, context=self.context).data

    def get_explanation(self, obj):
        language_id = self.context.get('language_id',1)#default english 
        
        queryset = QuestionOptionsExplanation.objects.filter(
                question_option__question_id=obj.question_id)
        queryset = queryset.filter(language_id=language_id)

        return QuestionOptionsExplanationSerializer(queryset, many=True).data


class SESectionSerializer(serializers.ModelSerializer):

    questions = SESectionQuestionSerializer(
        many=True, source="assessmentsectionquestion_set")

    class Meta:
        model = AssessmentSection
        fields = ['title', 'questions']


class SolvedExamplesSerializer(serializers.ModelSerializer):

    sections = SESectionSerializer(source="assessmentsection_set", many=True)
    content_view_analytics = serializers.SerializerMethodField()
    type_id = serializers.SerializerMethodField()
    assessment_id = serializers.IntegerField(source="id")
    
    class Meta:
        model = Assessment
        fields = [
            "title", "timed_type", "timed_duration_mins", "content_id", "total_marks",
            "attempts_allowed", "is_graded", "difficulty", "result_after","assessment_id",
            "allowed_after_duedate", "sections", "content_view_analytics","type_id","content_id"]

    def get_type_id(self,obj):
        return obj.type

    def get_content_view_analytics(self, obj):
        return {
            "completion_percentage": "100",
            "last_view": "2017-01-03 12:47:32",
            "total_time_spent": "1 hr"
        }


class AssessmentPreviewSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()
    unique_no = serializers.CharField(source="uid")
    assesment_actions = serializers.SerializerMethodField()
    summary_values = serializers.SerializerMethodField()
    
    class Meta:
        model = Assessment
        fields = [
            'content_id', "title", "unique_no", "description", "instructions", 
            "assesment_actions", "summary_values","languages"]
    
    def get_languages(self, obj):
        return LanguageSerializer(Language.objects.all(), many=True).data

    def get_assesment_actions(self, obj):
        actions = []
        user = self.context['request'].user


        if obj.attempt_allowed(user):
            if obj.is_attempted(user):
                actions.append({"id": 1, "label": "Re-Attempt", "message": ""})
            else:
                actions.append({"id": 1, "label": "Attempt", "message": ""})
    
        if obj.is_attempted(user):  
            #if solution available, show review button
            if obj.is_solution_available(user):
                actions.append({"id": 1, "label": "Review", "message": ""})
            elif obj.is_result_available(user):
                actions.append({"id": 1, "label": "Result", "message": ""})
    

        return actions

    
    def get_summary_values(self, obj):

        time_duration = obj.timed_duration_mins * 60
        values = [
            {"label": "total_questions", "value": obj.total_questions}, 
            {"label": "Time Duration(s)", "value": time_duration},
            {"label": "Maximum Marks", "value": obj.total_marks},
            {"label": "Negative Marking", "value": "Yes" if obj.is_negative else "No"},
            {"label": "No. Of Attempts", "value": obj.attempts_allowed},
            {"label": "Attempted", "value": obj.attempts_allowed},
            {"label": "Correct", "value": obj.attempts_allowed},
            {"label": "Score", "value": obj.attempts_allowed},
            {"label": "Average Time Taken", "value": obj.attempts_allowed},
            {"label": "No. of attempts Taken", "value": obj.attempts_allowed},
        ]

        user = self.context['request'].user
        if obj.is_attempted(user):
            values = obj.get_attempt_summary(user)
        else:
            values = obj.get_summary()
        
        items = []
        for key, value in values.items():
            items.append({'label':key,'value':str(value)})
        return items


class LanguageSerializerFull(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['id', 'name']

class AssesmentAttemptSectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSection
        fields = ['id', 'title', 'instructions', 'questions']

    def get_questions(self, obj):
        return AssessmentAttemptSectionQuestionSerializer(obj.assessmentsectionquestion_set,context=self.context, many=True).data

class AssesmentReviewSectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSection
        fields = ['id', 'title', 'instructions', 'questions']

    def get_questions(self, obj):
        return AssessmentReviewSectionQuestionSerializer(obj.assessmentsectionquestion_set,context=self.context, many=True).data


class AssessmentAttemptSectionQuestionSerializer(serializers.ModelSerializer):

    uid = serializers.CharField(source="question.uid")
    question_type = serializers.CharField(source="question.get_question_type_display")
    question_type_id = serializers.CharField(source="question.question_type")
    # duration_seconds = serializers.IntegerField(source="question.duration_seconds")
    marks = serializers.FloatField(source="question.marks")
    difficulty = serializers.CharField(source="question.difficulty")
    negative_marking = serializers.IntegerField(source="negative_marking_per_q")
    statement = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    hint_message = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSectionQuestion
        fields = ['id','negative_marking', 'uid', 'question_type','question_type_id',
        'duration_seconds', 'marks', 'difficulty', 'statement',
        'options', 'hint_message']

    def get_hint_message(self, obj):
        return None

    def get_statement(self, obj):
        language_id = self.context.get('language_id',1)#default english
        qs = obj.question.questionstatement_set.filter(language_id=language_id)
        if qs.exists():
            return qs.first().statement
        
        return obj.question.questionstatement_set.first().statement

    def get_options(self, obj):
        options = QuestionOptionsStatement.objects.filter(
                question_option__question_id=obj.question_id)
        options = options.filter( language_id=self.context.get('language_id',1))
        return QuestionOptionsStatementSerializer(options, many=True, context=self.context).data


class AssessmentReviewSectionQuestionSerializer(serializers.ModelSerializer):

    uid = serializers.CharField(source="question.uid")
    question_type = serializers.CharField(source="question.get_question_type_display")
    question_type_id = serializers.CharField(source="question.question_type")
    duration_seconds = serializers.SerializerMethodField()
    # marks = serializers.FloatField(source="question.marks")
    difficulty = serializers.CharField(source="question.difficulty")
    negative_marking = serializers.IntegerField(source="negative_marking_per_q")
    statement = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    hint_message = serializers.SerializerMethodField()
    analytics = serializers.SerializerMethodField()
    solution = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSectionQuestion
        fields = ['id','negative_marking', 'uid', 'question_type','question_type_id',
        'duration_seconds', 'marks', 'difficulty', 'statement',
        'options', 'hint_message','analytics','solution']



    def get_duration_seconds(self,obj):
        if self.context['attempt'].assessment.timed_type == AssessmentTimedChoices.ON_QUESTION:
            return obj.duration_seconds
        return None

    def get_analytics(self,obj):
        aaq = AssesmentAttemptQuestion.objects.filter(question=obj,assessment_attempt = self.context['attempt']).last()
        # aaq = AssesmentAttemptQuestion.objects.filter(question=obj).last()
        
        if aaq:
            return {
                'time_taken': aaq.time_taken,
                'difficulty_level':aaq.question.question.get_difficulty_display(),
                'batch_avg_time':aaq.batch_avg_time(),
                'batch_correct_percentage':aaq.batch_correct_percentage(),
                'score':aaq.marks,
                'is_correct':aaq.is_correct,
                'selected_option':aaq.options.all().values_list('id',flat=True),
                'correct_option':QuestionOptions.objects.filter(question=aaq.question.question,is_correct=True).values_list('id',flat=True)
            }

        #get batch only stats
        aaq = AssesmentAttemptQuestion.objects.filter(question=obj).last()
        # aaq = AssesmentAttemptQuestion.objects.filter(question=obj).last()
        user = self.context['request'].user
        batch = Student.objects.get(user=user).batch
        if aaq:
            return {
                'time_taken': None,
                'difficulty_level':aaq.question.question.get_difficulty_display(),
                'batch_avg_time':aaq.batch_avg_time(batch=batch),
                'batch_correct_percentage':aaq.batch_correct_percentage(batch=batch),
                'score': 0,
                'is_correct': None,
                'selected_option':[],
                'correct_option':QuestionOptions.objects.filter(question=aaq.question.question,is_correct=True).values_list('id',flat=True)
            }
        return {}
    def get_solution(self,obj):
        correct_options = QuestionOptions.objects.filter(question_id=obj.question_id,is_correct=True)
        video_file = ""
        if correct_options.exists():
            if correct_options.first().questionoptionsexplanation_set.first().video:
                video_file = correct_options.first().questionoptionsexplanation_set.first().video.url

            return {
                "explanation":correct_options.first().questionoptionsexplanation_set.first().explanation,
                "video_file":video_file
            }
        return {}

    def get_hint_message(self, obj):
        return None

    def get_statement(self, obj):
        language_id = self.context.get('language_id',1)#default english
        qs = obj.question.questionstatement_set.filter(language_id=language_id)
        if qs.exists():
            return qs.first().statement
        
        return obj.question.questionstatement_set.first().statement

    def get_options(self, obj):
        options = QuestionOptionsStatement.objects.filter(
                question_option__question_id=obj.question_id)
        options = options.filter( language_id=self.context.get('language_id',1))
        return QuestionOptionsStatementSerializer(options, many=True, context=self.context).data

    

class AssesmentAttemptSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()
    unique_no = serializers.CharField(source="unique_code")
    is_graded = serializers.SerializerMethodField()
    duration_mins = serializers.SerializerMethodField()
    instructions = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()
    criteria = serializers.SerializerMethodField()
    # questions = serializers.SerializerMethodField()
    attempt_id = serializers.SerializerMethodField()
    

    class Meta:
        model = Content
        fields = ['id', 'title', 'unique_no', 'languages', 'is_graded', 'duration_mins', 
        'instructions', 'sections', 'criteria','attempt_id'
        ]

    def get_languages(self, obj):
        return LanguageSerializerFull(Language.objects.all(), many=True).data

    def get_criteria(self, obj):
        '''
        Save to be shown when individual question solution/result available

        '''
        assessment = Assessment.objects.get(content=obj)
        if assessment.is_single_question_operated():
            return {    
                "response_individual_question":1,
                "save_button_label" : "Save", 
                }

        return {    
            "response_individual_question":0,
            "save_button_label" : "Save and Next", 
            }

    def get_is_graded(self, obj):
        return self.context['assessment'].is_graded

    def get_duration_mins(self, obj):
        return self.context['assessment'].timed_duration_mins

    def get_instructions(self, obj):
        return self.context['assessment'].instructions

    def get_sections(self, obj):
        sections = self.context['assessment'].assessmentsection_set.all()

        return AssesmentAttemptSectionSerializer(sections, context=self.context,many=True).data

    def get_attempt_id(self, obj):
        a=Assessment.objects.get(pk=self.context['assessment'].id)
        AssessmentAttempt.objects.filter(assessment=a,content=a.content,user=self.context['request'].user).update(is_latest=False)
        aa=AssessmentAttempt.objects.create(assessment=a,content=a.content,user=self.context['request'].user,is_latest=True)
        return aa.id
    

class AssesmentQuestionSaveSerializer(serializers.Serializer):

    attempt_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    time_taken = serializers.FloatField()
    selected_option_id = serializers.ListField(required=False, allow_null=True)
    # action = serializers.IntegerField()

    # def validate_selected_option_id(self, value):
    #     if not value:
    #         return None
    #     try:
    #         return int(value)
    #     except ValueError:
    #         raise serializers.ValidationError('You must supply an integer')

    def create(self, validated_data):
        attempt_id = validated_data['attempt_id']
        question_id = validated_data['question_id']
        time_taken = validated_data['time_taken']
        selected_option_id = validated_data.get('selected_option_id', [])
        action = 2
        is_correct = None
        selected_option_id = list(filter(None, selected_option_id))
        if selected_option_id:
            if not QuestionOptions.objects.filter(pk__in=selected_option_id, is_correct=False).exists():
                is_correct = True
            else:
                is_correct = False

            action = 1
        attempt_question = AssesmentAttemptQuestion.objects.create(
            is_correct=is_correct, assessment_attempt_id=attempt_id, question_id=question_id, 
            time_taken=time_taken, action=action)
        
        if selected_option_id:
            attempt_question.options.add(*selected_option_id)
        return attempt_question


class AssessmentQuestionSerializer(serializers.Serializer):

    question_id = serializers.IntegerField()
    time_taken = serializers.FloatField()
    selected_option_id = serializers.ListField(required=False, allow_null=True)

   

class AssessmentAttemptSerializer(serializers.Serializer):

    attempt_id = serializers.IntegerField()
    questions = AssessmentQuestionSerializer(many=True)

    def create(self, validated_data):
        attempt_id = validated_data['attempt_id']
        questions = validated_data['questions']

        for question in questions:
            question_id = question['question_id']
            time_taken = question['time_taken']
            selected_option_id = question.get('selected_option_id', [])
            is_correct = None
            action = 2
            selected_option_id = list(filter(None, selected_option_id))
            if selected_option_id:
                action = 1
                if not QuestionOptions.objects.filter(id__in=selected_option_id, is_correct=False).exists():
                    is_correct = True
                else:
                    is_correct = False
            
            attempt_question = AssesmentAttemptQuestion.objects.create(
                assessment_attempt_id=attempt_id, question_id=question_id, 
                time_taken=time_taken, action=action, is_correct=is_correct)
            if selected_option_id:
                attempt_question.options.add(*selected_option_id)
        return Question.objects.first()

class QuestionsSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentAttempt

class AssesmentAttemptSectionSerializerFull(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentSection
        fields = ['title', 'instructions', 'questions']

    def get_questions(self, obj):
        questions = []
        for question in obj.questions:
            data = {
                "order": question.question.id,
                "label": question.question.id,
                "colour": question.check_correct(attempt=self.context['attempt'])
            }
            questions.append(data)
        return questions


class AssessmentAttemptReviewSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    questions_summary = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    is_passed = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentAttempt
        fields = [
            "content","assessment_id", "user_id", "content_id", "language",  
             "duration", "score", "is_passed", "submit_date", "is_latest", "is_dynamic", 
            "is_faculty_reviewed", "reviewed_date", "reviewed_by", "is_submitted", 
            "submission_reason",  'questions_summary', 'sections'
        ]



    
    def get_is_passed(self,obj):
        if obj.assessment.passing_marks:
            return obj.score >= obj.assessment.passing_marks
        return None

    def get_duration(self,obj):
        return obj.assessment.get_duration()
        
    def get_content(self, obj):
        assessment = obj.assessment
        data = {
            "content_id": obj.id,
            "title": assessment.title,
            "unique_no": assessment.uid,
            "is_graded": assessment.is_graded,
            "score_card_available": assessment.is_result_available(self.context['request'].user),
            "duration": assessment.get_duration(),
            "instructions": assessment.instructions
        }
        return data
    
    def get_language(self, obj):
        return LanguageSerializerFull(Language.objects.all(), many=True).data
    
    def get_questions_summary(self, obj):

        return [
             {"key": "Answered", "value": obj.attempted_count, "color": "#bad53c"},
             {"key": "Skipped", "value": obj.skipped_count, "color": "#bad53c"},
             {"key": "Not Visited", "value": obj.not_visited_count, "color": "#bad53c"},
             {"key": "Unreleased","value": None,"color": "#bad53c"},
             {"key": "Released ","value": None,"color": "#bad53c"},
             {"key": "Correct","value": obj.correct_count,"color": "#bad53c"},
             {"key": "Wrong","value": obj.wrong_count,"color": "#bad53c"},
         ]

    def get_sections(self, obj):
        # sections = []
        # for section in obj.assessment.assessmentsection_set.all():
        #     data = AssesmentAttemptSectionSerializer(section, context={"attempt": obj}).data
        #     sections.append(data)
            
        # return sections
        sections = obj.assessment.assessmentsection_set.all()
        ctx = self.context
        ctx['attempt'] = obj
        return AssesmentReviewSectionSerializer(sections, context=ctx,many=True).data



class DPPPlannerSerializer(serializers.ModelSerializer):

    information = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    dpps = serializers.SerializerMethodField()
    # dpp_summary = serializers.SerializerMethodField()
    class Meta:
        model = Assessment
        fields = ['information', 'note', 'summary', 'dpps']

    def get_information(self, obj):
        return  {
            "value": "70 %",
            "message": "Your attendance record is good at",
            "background_color": "#bad53c"
        }

    def get_note(self, obj):
        return ""

    def get_summary(self, obj):
        return  {
            "attempted": "90/100",
            "correct": "12",
            "score": "12",
            "avg_time": "12 sec"
        }
    def get_dpps(self, obj):
        return  [
                    {
                        "content_id":2,
                        "title": "Project Motion",
                           "is_attempted": 0,
                        "submit_by": "2020-01-01T12:00:00",
                        "time_left": "1 day left",
                        "total_questions": "60",
                        "duration_mins": "20 mins",
                        "actions": [
                            {"id": 1, "label": "Re-Attempt", "message": ""},
                            {"id": 5,"label": "Result","message": ""}
                        ],
                    },
                    {
                        "content_id":3,
                        "title": "Project Motion",
                           "is_attempted": 1,
                        "submit_by": "2020-01-01T12:00:00",
                        "time_left": "2 days left",
                        "total_questions": "60",
                        "duration_mins": "20 mins",
                        "actions": [
                            {"id": 1, "label": "Re-Attempt", "message": ""},
                            {"id": 5,"label": "Result","message": ""}
                        ],
                        "dpp_summary": {
                            "attempted": "90/100",
                            "correct": "12",
                            "score": "12",
                            "avg_time": "12 sec",
                            "summary":
                            {
                              "attempted": {
                                  "result":"90/100",
                                "easy": "2/5",
                                "medium": "2/5",
                                "hard": "2/5",
                                "very_hard": "2/5"
                              },
                              "correct": {
                                  "result":"58",
                                "easy": "10",
                                "medium": "10",
                                "hard": "10",
                                "very_hard": "10"
                              },
                              "avg_time": {
                                  "result":"33s",
                                "easy": "10s",
                                "medium": "10s",
                                "hard": "10s",
                                "very_hard": "10s"
                              }
                            }
                        }
                    }
                ]


class ExerciseSerializer(serializers.ModelSerializer):

    information = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    exercises = serializers.SerializerMethodField()
    filters = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = ['information', 'note', 'summary', 'exercises', 'filters']

    def get_information(self, obj):
        return {
            "value": "70 %", "message": "Your attendance record is good at",
            "background_color": "#bad53c"
        }
    
    def get_note(self, obj):
        return ""

    def get_summary(self, obj):
        return {
            "Attempted": "90/100",
            "correct": "12",
            "avg_time": "12 sec"
        }

    def get_exercises(self, obj):
        return [
            {
                "content_id":1,
                "title": "",
                "is_attempted": "",
                "submit_by": "",
                "time_left": "1 day left",
                "total_questions": "",
                "actions": [
                    {"id": 2,"label": "Re Attempt","message": ""},
                    {"id": 3,"label": "Review","message": ""},
                ],
                "exercise_summary": {
                            "attempted": "90/100",
                            "correct": "12",
                            "score": "12",
                            "avg_time": "12 sec",
                            "summary":
                            {
                              "attempted": {
                                  "result":"90/100",
                                "easy": "2/5",
                                "medium": "2/5",
                                "hard": "2/5",
                                "very_hard": "2/5"
                              },
                              "correct": {
                                  "result":"58",
                                "easy": "10",
                                "medium": "10",
                                "hard": "10",
                                "very_hard": "10"
                              },
                              "avg_time": {
                                  "result":"33s",
                                "easy": "10s",
                                "medium": "10s",
                                "hard": "10s",
                                "very_hard": "10s"
                              }
                            }
                        },
                "tagged_chapters": ["", "", ""],
                "tagged_exercise": ["", "", ""]
            }]
    def get_filters(self, obj):
        [{"chapter_title": "",  "exercises": ["", "", "", ""]}]


class FacultyToDoSerializer(serializers.ModelSerializer):

    pending_action_dates = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = ['pending_action_dates', 'date', 'lectures']

    def get_pending_action_dates(self, obj):

        return ["", ""]

    def get_date(self, obj):
        return "12-12-2019"

    def get_lectures(self, obj):
        return [{
            "lecture_title": "Mathematics Tool",
            "class": "",
            "batch": "",
            "room_no": "",
            "is_immediate": 1,
            "is_tentative": 0,
            "time": "3:00 AM",
            "duration": "3 hrs",
            "important_label": "30 mins left",
            "activities": [{
                    "name": "Study Material",
                    "is_released": 1,
                    "value": "2 Released"
                },
                {
                    "name": "Topics",
                    "is_delivered": 1,
                    "value": "3 Topics Delivered"
                },
                {
                    "name": "Exercise",
                    "is_released": 1,
                    "value": "3 Released"
                },
                {
                    "name": "DPP",
                    "is_released": 1,
                    "value": "3 Released"
                }
            ]
        }]

class AssessmentScoreCardSerializer(serializers.ModelSerializer):

    score_card_available = serializers.SerializerMethodField()
    assessment_summary = serializers.SerializerMethodField()
    tabs = serializers.SerializerMethodField()
    overall = serializers.SerializerMethodField()
    strengths = serializers.SerializerMethodField()
    weaknesses = serializers.SerializerMethodField()
    chapterwise = serializers.SerializerMethodField()
    topicwise = serializers.SerializerMethodField()
    subtopicwise = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = ['id', 'score_card_available', 'assessment_summary', 'tabs', 'overall',
            'strengths', 'weaknesses', 'chapterwise', 'topicwise', 'subtopicwise'
        ]

    def get_score_card_available(self, obj):
        return 1

    def get_assessment_summary(self, obj):
        # print(self.context['request'].user)
        return obj.get_attempt_summary(self.context['request'].user)
    

    def get_tabs(self, obj):
        return ["Overall", "Strength/Weakness", "Chapterwise", "Topicwise", "Subtopicwise"]

    def get_overall(self, obj):
        {
            "questions_attempted": {
                "you": "",
                "batch_average": "",
                "is_greater": 0
            },
            "correct_answers": {
                "you": "",
                "batch_average": "",
                "is_greater": 0
            },
            "accuracy": {
                "you": "",
                "batch_average": "",
                "is_greater": 0
            },
            "score": {
                "you": "",
                "batch_average": "",
                "max_score": "",
                "is_greater": 0
            },
            "avg_time_per_question": {
                "you": "",
                "batch_average": "",
                "is_greater": 0
            },
            "scoring_pattern": {
                "is_greater": 0,
                "easy": {
                    "you": "",
                    "batch_average": ""
                },
                "medium": {
                    "you": "",
                    "batch_average": ""
                },
                "difficult": {
                    "you": "",
                    "batch_average": ""
                },
                "hard": {
                    "you": "",
                    "batch_average": ""
                }
            }
        }
    def get_strengths(self, obj):
        return ["", "", ""]

    def get_weaknesses(self, obj):
        return ["", "", ""]

    def get_chapterwise(self, obj):
        return [{
                "chapter_title": "",
                "correct": {
                    "you": "",
                    "batch_average": ""
                },
                "avg_time": {
                    "you": "",
                    "batch_average": ""
                },
                "attempt": {
                    "you": "",
                    "batch_average": ""
                },
                "score": {
                    "you": "",
                    "batch_average": ""
                }
            },
            {
                "chapter_title": "",
                "correct": {
                    "you": "",
                    "batch_average": ""
                },
                "avg_time": {
                    "you": "",
                    "batch_average": ""
                },
                "attempt": {
                    "you": "",
                    "batch_average": ""
                },
                "score": {
                    "you": "",
                    "batch_average": ""
                }
            }
        ]
    def get_topicwise(self, obj):
        return [{
                "topic_title": "",
                "correct": {
                    "you": "",
                    "batch_average": ""
                },
                "avg_time": {
                    "you": "",
                    "batch_average": ""
                },
                "attempt": {
                    "you": "",
                    "batch_average": ""
                },
                "score": {
                    "you": "",
                    "batch_average": ""
                }
            },
            {
                "topic_title": "",
                "correct": {
                    "you": "",
                    "batch_average": ""
                },
                "avg_time": {
                    "you": "",
                    "batch_average": ""
                },
                "attempt": {
                    "you": "",
                    "batch_average": ""
                },
                "score": {
                    "you": "",
                    "batch_average": ""
                }
            }
        ] 
    def get_subtopicwise(self, obj):
        return [{
                "subtopic_title": "",
                "correct": {
                    "you": "",
                    "batch_average": ""
                },
                "avg_time": {
                    "you": "",
                    "batch_average": ""
                },
                "attempt": {
                    "you": "",
                    "batch_average": ""
                },
                "score": {
                    "you": "",
                    "batch_average": ""
                }
            },
            {
                "subtopic_title": "",
                "correct": {
                    "you": "",
                    "batch_average": ""
                },
                "avg_time": {
                    "you": "",
                    "batch_average": ""
                },
                "attempt": {
                    "you": "",
                    "batch_average": ""
                },
                "score": {
                    "you": "",
                    "batch_average": ""
                }
            }
        ]
    