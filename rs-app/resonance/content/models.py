from django.db import models
from common.models import BaseResonanceModel,TOCMapping
from common.choices import *
from django.utils.text import slugify
from institute.models import Sessions, Phase, Program, Batch
from django.contrib.auth import get_user_model
from django.core import serializers
from datetime import date, datetime, time
from django.conf import settings
from django.db.models import F, Sum, FloatField, Avg
from users.models import Student,User

class BaseContent(BaseResonanceModel):
    title = models.CharField(max_length=120,blank=True,null=True)
    unique_code = models.CharField(max_length=120,blank=True,null=True)
    content_type = models.SmallIntegerField(choices=ContentTypeChoices.CHOICES, default=0)
    content_subtype = models.SmallIntegerField(choices=ContentSubtypeChoices.CHOICES, default=0)

    class Meta:
        abstract = True


class Content(BaseContent):
    description = models.TextField(blank=True,null=True)
    faculty_releasable = models.BooleanField(default=False)
    faculty_only = models.BooleanField(default=False)
    created_by =  models.ForeignKey(settings.AUTH_USER_MODEL, null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class ContentTOCMapping(BaseContent):
    content =  models.ForeignKey(Content, null=True,on_delete=models.CASCADE)
    level = models.SmallIntegerField(choices=ContentMappingLevelChoices.CHOICES, default=0)
    ref_id = models.IntegerField(default=0)


class Concept(models.Model):
    '''
    This class holds information related to core concept terms,
    will be mapped with student, faculty and content
    '''
    name = models.CharField("Concept", max_length=20)
    slug = models.SlugField("Concept slug", editable=False)

    def __str__(self):
        return self.concept_slug

    def save(self, *args, **kwargs):
        self.concept_slug = slugify(self.name)
        super(Concept, self).save(*args, **kwargs)


class UserConcept(BaseResonanceModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='concepts')
    concept = models.ForeignKey("content.Concept", on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return "{} {}".format(self.user.name, self.concept.name)


class Language(BaseResonanceModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Question(BaseResonanceModel):

    uid = models.CharField(
        max_length=120,blank=True,null=True,help_text="The unique identifier of question",
        unique=True)
    question_type = models.SmallIntegerField(choices=QuestionTypeChoices.CHOICES, default=0)
    duration_seconds = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)
    negative_marking = models.FloatField(default=0)
    source = models.SmallIntegerField(
        choices=QuestionCategoryChoices.CHOICES, default=0, null=True, blank=True)
    difficulty = models.SmallIntegerField(choices=DifficultyLevelChoices.CHOICES, default=0)

    def __str__(self):
        return self.uid


class QuestionStatement(BaseResonanceModel):
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    statement = models.TextField()
    def __str__(self):
        return self.statement


class QuestionOptions(BaseResonanceModel):
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "%i - %i - %s"  %(self.question_id, self.id, self.is_correct)


class QuestionOptionsStatement(BaseResonanceModel):
    question_option = models.ForeignKey(QuestionOptions, null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    statement = models.TextField()

    def __str__(self):
        return self.statement


class QuestionOptionsExplanation(BaseResonanceModel):
    question_option = models.ForeignKey(QuestionOptions, null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    explanation = models.TextField()
    video = models.FileField(upload_to='study_material/question/solution/',blank=True,null=True)

    def __str__(self):
        return self.explanation


class QuestionTOCMapping(TOCMapping):
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)


class Lecture(BaseResonanceModel):
    title =  models.CharField(max_length=120,blank=True,null=True,default='Lecture Title')
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField(blank=True, null=True)
    duration_hrs = models.IntegerField(default=0)
    faculty =  models.ForeignKey(settings.AUTH_USER_MODEL, null=True,on_delete=models.SET_NULL)
    classs = models.ForeignKey('institute.Classs', null=True,on_delete=models.SET_NULL)
    subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE)

    session = models.ForeignKey('institute.Sessions', null=True,on_delete=models.SET_NULL)
    program = models.ForeignKey('institute.Program', null=True,on_delete=models.SET_NULL)
    phase = models.ForeignKey('institute.Phase', null=True,on_delete=models.SET_NULL)
    batch = models.ForeignKey('institute.Batch', null=True,on_delete=models.SET_NULL)
    room =  models.CharField(max_length=120,blank=True,null=True,help_text="The class where lecture is happening",default='Room Number #')
    created_by =  models.ForeignKey(settings.AUTH_USER_MODEL, null=True,on_delete=models.SET_NULL,related_name="created_lectures")

    is_tentative = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    sequence_no = models.IntegerField(default=0)

    @property
    def chapter(self):
        return self.lecturetocmapping_set.first().toc_id

    def chapter_title(self):
        return self.lecturetocmapping_set.first().toc.label


class LectureTOCMapping(TOCMapping):
    lecture = models.ForeignKey(Lecture, null=True, on_delete=models.SET_NULL)
    delivered_status = models.SmallIntegerField(
        choices=LectureDeliveryStatusChoices.CHOICES, default=0)


class Assessment(BaseResonanceModel):
    type = models.SmallIntegerField(choices=QuestionCategoryChoices.CHOICES, default=0)
    title =  models.CharField(max_length=120,blank=True,null=True)
    uid = models.CharField(max_length=20, unique=True)
    timed_type = models.SmallIntegerField(choices=AssessmentTimedChoices.CHOICES, default=0)
    reset_time_every_attempt = models.BooleanField(default=True)
    timed_duration_mins = models.IntegerField(default=0)
    content = models.ForeignKey(Content, blank=True, null=True, on_delete=models.SET_NULL)

    total_marks = models.IntegerField(default=0)
    passing_marks = models.IntegerField(default=0)
    attempts_allowed = models.IntegerField(default=0, help_text="0 is for unlimited attempts")
    is_graded = models.BooleanField(default=False)
    closed_after_passing = models.BooleanField(default=False)
    difficulty = models.SmallIntegerField(choices=DifficultyLevelChoices.CHOICES, default=0)
    result_after = models.SmallIntegerField(
        choices=AssessmentResultChoices.CHOICES, default=0)
    allowed_after_duedate= models.BooleanField(default=False)
    instructions = models.TextField(null=True)
    description = models.TextField(null=True)
    show_solution_after = models.PositiveSmallIntegerField(
        choices=AssessmentSolutionVisibilityChoices.CHOICES, default=2)
    is_negative = models.BooleanField(default=False)
    total_questions = models.PositiveSmallIntegerField(default=0)


    def __str__(self):
        return "{0}".format(self.title)

    def get_summary(self):

        summary=dict()
        summary['Total Questions'] = self.get_total_questions()

        if self.timed_type != AssessmentTimedChoices.NONE:
            summary['Total Duration(s)'] = self.get_duration()

        if self.is_graded:
            summary['Maximum Marks'] = self.total_marks
            summary['Negative Marking'] = self.is_negative
        summary['No of Attempts'] = self.attempts_allowed if self.attempts_allowed else "Unlimited"
        return summary


    def get_duration(self):
        if self.timed_type != AssessmentTimedChoices.NONE:
            time_duration = self.timed_duration_mins * 60
            if self.timed_type == AssessmentTimedChoices.ON_QUESTION:
                time_duration=AssessmentSectionQuestion.objects.filter(assessment_section__assessment=self).aggregate(sum=Sum('duration_seconds'))['sum']
        return None

    def get_total_questions(self):
        return AssessmentSectionQuestion.objects.filter(assessment_section__assessment_id=self.id).count()


    def get_attempt_summary(self,user):
        ast_atmpt = AssessmentAttempt.objects.filter(assessment=self,user=user).last()
        summary=dict()
        if ast_atmpt:
            summary['Attempted'] = "{}/{}".format(ast_atmpt.attempted_questions.count(),self.get_total_questions())
            summary['Avg. Time Taken'] = ast_atmpt.avg_time_taken
            summary['No. of Attempts Taken'] = AssessmentAttempt.objects.filter(assessment=self,user=user).count()
            summary['Correct'] = ast_atmpt.correct_count
            summary['Score'] = ast_atmpt.score
        return summary

    def is_attempted(self,user):
        return AssessmentAttempt.objects.filter(user=user,assessment=self).exists()

    def attempt_allowed(self,user):
        attempts = AssessmentAttempt.objects.filter(user=user,assessment=self)
        if attempts.count():
            ast_atmpt = attempts.last()
            if self.closed_after_passing and self.passing_marks <= ast_atmpt.score:
                return False
        return self.attempts_allowed == 0  or attempts.count() < self.attempts_allowed

    def is_solution_available(self,user):
        # ASSESSMENT_PASSING = 2
        # ALL_ATTEMPTS = 3
        # EVERY_ATTEMPT = 4
        if self.show_solution_after == AssessmentSolutionVisibilityChoices.EVERY_ATTEMPT:
            return True

        attempts = AssessmentAttempt.objects.filter(assessment=self,user=user).count()
        if self.show_solution_after == AssessmentSolutionVisibilityChoices.ALL_ATTEMPTS:
            return self.attempt_allowed !=0 and attempts >= self.attempts_allowed

        if self.show_solution_after == AssessmentSolutionVisibilityChoices.EVERY_QUESTION and attempts:
            return True

        if self.show_solution_after == AssessmentSolutionVisibilityChoices.ASSESSMENT_PASSING:
            ast_atmpt = AssessmentAttempt.objects.filter(assessment=self,user=user).last()
            return ast_atmpt and self.passing_marks <= ast_atmpt.score

    def is_result_available(self,user):
        # ASSESSMENT_PASSING = 2
        # ALL_ATTEMPTS = 3
        # EVERY_ATTEMPT = 4
        if self.result_after == AssessmentSolutionVisibilityChoices.EVERY_ATTEMPT:
            return True

        attempts = AssessmentAttempt.objects.filter(assessment=self,user=user).count()
        if self.result_after == AssessmentSolutionVisibilityChoices.ALL_ATTEMPTS:
            return self.attempt_allowed !=0 and attempts >= self.attempts_allowed

        if self.result_after == AssessmentSolutionVisibilityChoices.EVERY_QUESTION and attempts:
            return True

        if self.result_after == AssessmentSolutionVisibilityChoices.ASSESSMENT_PASSING:
            ast_atmpt = AssessmentAttempt.objects.filter(assessment=self,user=user).last()
            return self.passing_marks <= ast_atmpt.score
        return False

    def is_single_question_operated(self):
        return self.show_solution_after == AssessmentSolutionVisibilityChoices.EVERY_QUESTION \
            or self.result_after == AssessmentSolutionVisibilityChoices.EVERY_QUESTION

class AssessmentSection(BaseResonanceModel):
    title =  models.CharField(max_length=120,blank=True,null=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    negative_marking_per_q = models.IntegerField(default=0)
    instructions = models.TextField(null=True)

    def __str__(self):
        return self.title

    @property
    def questions(self):
        return self.assessmentsectionquestion_set.select_related('question')


class AssessmentSectionQuestion(BaseResonanceModel):
    assessment_section = models.ForeignKey(AssessmentSection, on_delete=models.CASCADE)
    negative_marking_per_q = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    duration_seconds= models.IntegerField(default=0)
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.assessment_section.title

    def check_correct(self, attempt):
        if attempt.assesmentattemptquestion_set.filter(question=self.question).exists():
            if attempt.assesmentattemptquestion_set.filter(question=self.question, is_correct=True).exists():
                return "Correct Color"
            return "Incorrect Color"
        return "Not Attempted Color"


class StudyMaterial(BaseResonanceModel):
    type = models.SmallIntegerField(choices=StudyMaterialTypeChoices.CHOICES, default=0)
    title = models.CharField(max_length=120,blank=True,null=True)
    downloadable = models.BooleanField(default=False)
    faculty_only = models.BooleanField(default=False)
    content = models.ForeignKey(Content, blank=True, null=True, on_delete=models.SET_NULL)
    duration_mins = models.IntegerField(default=0)


class StudyMaterialFile(models.Model):
    publish_status = models.SmallIntegerField(choices=PublishStatusChoices.CHOICES, default=0)
    study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE,related_name="files")
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    content = models.TextField(blank=True,null=True)
    file = models.FileField(upload_to='study_material/notes/',blank=True,null=True)

    @property
    def files(self):
        return self.file

    @property
    def file_url(self):
        return self.file

    @property
    def view_analytics(self):
        data = {
                "completion_percentage": "11.11%",
                "last_view": "2017-01-03 12:47:32",
                "last_page": "36",
                "total_time_spent":"1 hr",
            }
        return data


# class StudyMaterialTOCMapping(TOCMapping):
# 	study_material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE,related_name="toc")


class LectureTOCContent(BaseResonanceModel):
    lecture = models.ForeignKey(Lecture, null=True, on_delete=models.SET_NULL)
    batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
    content_toc = models.ForeignKey(ContentTOCMapping, null=True, on_delete=models.SET_NULL)
    faculty_releasable = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)
    delivered_status = models.SmallIntegerField(
        choices=LectureDeliveryStatusChoices.CHOICES, default=0)
    due_date = models.DateTimeField(blank=True, null=True)


class DPPPlanner(BaseResonanceModel):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    title = models.CharField(max_length=120,blank=True,null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    duration_mins = models.IntegerField(default=0)
    classs = models.ForeignKey('institute.Classs', null=True,on_delete=models.SET_NULL)
    subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE)
    session = models.ForeignKey('institute.Sessions', null=True,on_delete=models.SET_NULL)
    program = models.ForeignKey('institute.Program', null=True,on_delete=models.SET_NULL)
    phase = models.ForeignKey('institute.Phase', null=True,on_delete=models.SET_NULL)
    batch = models.ForeignKey('institute.Batch', null=True,on_delete=models.SET_NULL)
    is_tentative = models.BooleanField(default=True)
    is_released = models.BooleanField(default=False)
    sequence_no = models.IntegerField(default=0)
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.title if self.title else ""


class AssessmentAttempt(BaseResonanceModel):

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    total_questions = models.FloatField(null=True)
    attempted_questions = models.PositiveSmallIntegerField(default=0)
    visited_questions = models.PositiveSmallIntegerField(default=0)
    duration = models.FloatField(null=True, blank=True)
    marks_obtained = models.FloatField(default=0)
    is_passed = models.BooleanField(default=True)
    submit_date = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    is_latest = models.BooleanField(default=False)
    is_dynamic = models.BooleanField(default=False)
    is_faculty_reviewed = models.BooleanField(default=False)
    reviewed_date = models.DateField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
        related_name="reviewd_by")
    is_submitted = models.NullBooleanField()
    submission_reason = models.TextField(null=True)

    @property
    def skipped_questions(self):
        return self.visited_questions - self.attempted_questions

    @property
    def avg_time_taken(self):
        total_time_taken = self.assesmentattemptquestion_set.aggregate(sum=Sum('time_taken'))['sum']
        total_questions = self.assesmentattemptquestion_set.count()
        if total_questions:
            return total_time_taken / total_questions
        return 0

    @property
    def attempted_questions(self):
        return self.assesmentattemptquestion_set.filter(action=1)

    @property
    def attempted_count(self):
        return self.attempted_questions.count()

    @property
    def visited_questions(self):
        return self.assesmentattemptquestion_set.filter(action=3)

    @property
    def visited_count(self):
        return self.visited_questions.count()

    @property
    def skipped_questions(self):
        return self.assesmentattemptquestion_set.filter(action=2)

    @property
    def skipped_count(self):
        return self.skipped_questions.count()

    @property
    def not_visited_count(self):
        return AssessmentSectionQuestion.objects.filter(assessment_section__assessment = self.assessment).count() \
             -  self.all_questions.count()

    @property
    def correct_questions(self):
        return self.assesmentattemptquestion_set.filter(is_correct=True)

    @property
    def correct_count(self):
        return self.correct_questions.count()

    @property
    def wrong_questions(self):
        return self.assesmentattemptquestion_set.filter(is_correct=False)

    @property
    def wrong_count(self):
        return self.wrong_questions.count()

    @property
    def all_questions(self):
        return self.assesmentattemptquestion_set.all()

    @property
    def score(self):
        score = 0
        for q in self.assesmentattemptquestion_set.all():
            if q.is_correct is not None:
                score += q.marks
        return score

class AssesmentAttemptQuestion(BaseResonanceModel):
    ATTEMPTED = 1
    SKIPPED = 2
    VISITED = 3

    CHOICES = (
        (ATTEMPTED, "Attempted"),
        (SKIPPED, "Skipped"),
        (VISITED, "Visited"),
    )

    assessment_attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(AssessmentSectionQuestion, on_delete=models.CASCADE)
    action = models.PositiveSmallIntegerField(choices=CHOICES, default=2) # skipped, attempted, Visited
    is_correct = models.NullBooleanField()
    options = models.ManyToManyField(QuestionOptions, blank=True)
    time_taken = models.FloatField(default=0)

    @property
    def is_answered(self):
        return 0

    @property
    def	is_visited(self):
        return 0

    @property
    def	is_marked_for_review(self):
        return 1

    @property
    def	is_released(self):
        1

    @property
    def	released_here(self):
        return 0

    @property
    def	release_note(self):
        return ""

    @property
    def duration(self):
        return 10

    @property
    def marks(self):
        if self.action == AssesmentAttemptQuestion.SKIPPED:
            return 0
        return self.question.marks if self.is_correct else -self.question.negative_marking_per_q

    def get_batch_questions(self,batch=None):
        if not batch:
            batch = Student.objects.filter(user=self.assessment_attempt.user).first().batch
        batch_users = Student.objects.filter(batch=batch).values_list('user')
        batch_attempts = AssessmentAttempt.objects.filter(user__in=batch_users,is_latest=True)
        batch_question = AssesmentAttemptQuestion.objects.filter(assessment_attempt__in=batch_attempts,question=self.question)
        return batch_question

    def batch_avg_time(self,batch=None):
        batch_question = self.get_batch_questions(batch=batch)
        return batch_question.aggregate(avg=Avg('time_taken'))['avg']

    def batch_correct_percentage(self,batch=None):
        batch_question = self.get_batch_questions(batch=batch)
        correct = batch_question.filter(is_correct=True).count()
        total = batch_question.count()
        if total:
            return int((correct*100)/total)
        return 0

class NotesAccessLog(BaseResonanceModel):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file = models.ForeignKey(StudyMaterialFile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    checked_pages = models.CharField(max_length=520,blank=True,null=True)
    last_page = models.SmallIntegerField(default=0)
    start_date_time = models.DateTimeField(blank=True,null=True)
    end_date_time = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)


class VideoAccessLog(BaseResonanceModel):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file = models.ForeignKey(StudyMaterialFile, on_delete=models.CASCADE)
    file_duration_viewed = models.SmallIntegerField(default=0)
    start_date_time = models.DateTimeField(blank=True,null=True)
    end_date_time = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
