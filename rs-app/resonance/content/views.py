from django.shortcuts import render, redirect
from django.core import serializers
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from .filters import QuestionFilter
from common.choices import (
    QuestionCategoryChoices, DifficultyLevelChoices, AssessmentTimedChoices,
    AssessmentResultChoices, AssessmentSolutionVisibilityChoices, AssessmentResultChoices,
    ContentMappingLevelChoices
)
from django.urls import reverse
from django.views.generic import TemplateView, ListView, View
from subject.models import TOC
from .models import (
    Lecture, LectureTOCMapping, Question, Language, Content, ContentTOCMapping,
    QuestionStatement, QuestionOptions, QuestionOptionsStatement,
    QuestionOptionsExplanation, Assessment, AssessmentSection, AssessmentSectionQuestion
)
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView
)
from .serializers import (
    LectureSerializer, LecturePageNumberPagination
)
from rest_framework import permissions,authentication
from common.choices import (
    DifficultyLevelChoices, QuestionTypeChoices
)
from common.views import login_required_custom
from common.views import login_required_custom,login_api_required
from users.models import Student

def render_response(data=None, status=None, error=None):
    if data and status:
        return Response({'data': data, 'error': [], 'status': status})
    return Response({'data': data, 'error': [error], 'status': status})

class LoginRequiredMixin(object):

    @login_required_custom(login_url='/')
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args, **kwargs)

class AssessmentCreateTemplateView(TemplateView):
    template_name = "content/html/assesment_create.html"

    def get_checkbox_value(self, arg_value=None):
        if arg_value:
            return True
        return False

    def get_context_data(self, error=None, *args, **kwargs):
        context = super(AssessmentCreateTemplateView, self).get_context_data(**kwargs)
        context['type'] = QuestionCategoryChoices.CHOICES
        context['timed_type'] = AssessmentTimedChoices.CHOICES
        context['difficulty'] = DifficultyLevelChoices.CHOICES
        context['result_after'] = AssessmentResultChoices.CHOICES
        context['show_solution_after'] = AssessmentSolutionVisibilityChoices.CHOICES
        context['result_after'] = AssessmentResultChoices.CHOICES
        if error:
            context['error'] = error
        return context

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        title_var = self.request.POST.get('title')
        unique_code_var = self.request.POST.get('unique_code')
        type_var = self.request.POST.get('type')
        timed_type_var = self.request.POST.get('timed-type')
        total_mask_var = self.request.POST.get('total-mask')
        duration_var = self.request.POST.get('duration')
        section_count = self.request.POST.get('section_count')
        passing_marks_var = self.request.POST.get('passing-marks')
        attempts_var = self.request.POST.get('attempts')
        difficulty_var = self.request.POST.get('difficulty')
        result_after_var = self.request.POST.get('result-after')
        is_graded_var = self.get_checkbox_value(self.request.POST.get('is_graded', None))
        reset_time_every_attempt_var = self.get_checkbox_value(self.request.POST.get('reset_time_every_attempt', None))
        closed_after_passing_var = self.get_checkbox_value(self.request.POST.get('closed_after_passing', None))
        allowed_after_duedate_var = self.get_checkbox_value(self.request.POST.get('allowed_after_duedate', None))
        instructions_var = self.request.POST.get('instructions')
        description_var = self.request.POST.get('description')
        try:
            toc_id = request.GET.get('toc_id', None)
            if toc_id:
                toc_obj = TOC.objects.get(pk=toc_id)
                content_create_obj = Content.objects.create(
                                title=title_var,
                                content_type=2,
                                content_subtype=type_var,
                                description=description_var)
                content_toc_mapping_obj = ContentTOCMapping.objects.create(
                        content_id=content_create_obj.id,
                        level=ContentMappingLevelChoices.get_by_toc_level(toc_obj.level),
                        ref_id=toc_id)
                create_assesment = Assessment.objects.create(
                        type=int(type_var),
                        uid=unique_code_var,
                        title=title_var,
                        content_id=content_create_obj.id,
                        timed_duration_mins=duration_var,
                        attempts_allowed=attempts_var,
                        passing_marks=passing_marks_var,
                        is_graded=is_graded_var,
                        total_marks=int(total_mask_var),
                        timed_type=int(timed_type_var),
                        difficulty=difficulty_var,
                        result_after=result_after_var,
                        show_solution_after=1,
                        reset_time_every_attempt=reset_time_every_attempt_var,
                        closed_after_passing=closed_after_passing_var,
                        allowed_after_duedate=allowed_after_duedate_var,
                        instructions=instructions_var,
                        description=description_var)
            else:
                context = self.get_context_data(error="toc_id is required for assessment", *args, **kwargs)
                return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            context = self.get_context_data(error="Assessment UID object already exist.", *args, **kwargs)
            return render(request, self.template_name, context)
        else:
            for i in range(1, int(section_count) + 1):
                AssessmentSection.objects.create(
                        title="Section {}".format(i),
                        assessment_id=create_assesment.id,
                        instructions="")
        params = "?class={}&subject={}&success=true".format(toc_obj.subject_id,toc_obj.subject.classs_id)
        params += '&modified_id=' + str(content_create_obj.id)
        return redirect(reverse('content') + params)

class AssessmentEditTemplateView(TemplateView):
    template_name = 'content/html/assessment_edit.html'
    model = Assessment
    content_model = Content

    def get_checkbox_value(self, arg_value=None):
        if arg_value:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(AssessmentEditTemplateView, self).get_context_data(**kwargs)
        obj = self.model.objects.get(id=self.kwargs['id'])
        context['type'] = QuestionCategoryChoices.CHOICES
        context['timed_type'] = AssessmentTimedChoices.CHOICES
        context['difficulty'] = DifficultyLevelChoices.CHOICES
        context['result_after'] = AssessmentResultChoices.CHOICES
        context['show_solution_after'] = AssessmentSolutionVisibilityChoices.CHOICES
        context['result_after'] = AssessmentResultChoices.CHOICES
        context['assessment_obj'] = obj
        return context

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.filter(id=self.kwargs['id'])
        title_var = self.request.POST.get('title')
        type_var = self.request.POST.get('type')
        timed_type_var = self.request.POST.get('timed-type')
        total_mask_var = self.request.POST.get('total-mask')
        duration_var = self.request.POST.get('duration')
        passing_marks_var = self.request.POST.get('passing-marks')
        attempts_var = self.request.POST.get('attempts')
        difficulty_var = self.request.POST.get('difficulty')
        result_after_var = self.request.POST.get('result-after')
        is_graded_var = self.get_checkbox_value(self.request.POST.get('is_graded', None))
        reset_time_every_attempt_var = self.get_checkbox_value(self.request.POST.get('reset_time_every_attempt', None))
        closed_after_passing_var = self.get_checkbox_value(self.request.POST.get('closed_after_passing', None))
        allowed_after_duedate_var = self.get_checkbox_value(self.request.POST.get('allowed_after_duedate', None))
        instructions_var = self.request.POST.get('instructions')
        description_var = self.request.POST.get('description')
        get_content_obj = self.content_model.objects.filter(id=obj[0].content_id)
        get_content_obj.update(
            title=title_var,
            content_type=2,
            content_subtype=type_var,
            description=description_var)
        obj.update(
            title=title_var,
            type=type_var,
            timed_type=timed_type_var,
            timed_duration_mins=duration_var,
            total_marks=total_mask_var,
            passing_marks=passing_marks_var,
            attempts_allowed=attempts_var,
            is_graded=is_graded_var,
            difficulty=difficulty_var,
            result_after=result_after_var,
            reset_time_every_attempt=reset_time_every_attempt_var,
            closed_after_passing=closed_after_passing_var,
            allowed_after_duedate=allowed_after_duedate_var,
            instructions=instructions_var,
            description=description_var)
        return redirect('AssessmentTemplateView')

class AssessmentTemplateView(LoginRequiredMixin,ListView):
    template_name = 'content/html/dpp.html'
    model = Assessment
    paginate_by = settings.PAGINATION_SIZE
    ordering = ['-id']

class AssessmentSectionEditTemplateView(TemplateView):
    template_name = "content/html/assessment_section_edit.html"
    model = AssessmentSection

    def get_context_data(self, *args, **kwargs):
        context = super(AssessmentSectionEditTemplateView, self).get_context_data(**kwargs)
        context['accessmentid'] = self.kwargs['assessment_id']
        assessment_queryset = AssessmentSection.objects.get(id=self.kwargs['edit_id'])
        context['title'] = assessment_queryset.title
        context['negative_marking_per_q'] = assessment_queryset.negative_marking_per_q
        context['instructions'] = assessment_queryset.instructions
        return context

    def post(self, request, *args, **kwargs):
        section_title_var = self.request.POST.get('section_title')
        negative_marking_per_q_var = self.request.POST.get('negative_marking_per_q')
        instructions_var = self.request.POST.get('instructions')
        assessment_queryset = AssessmentSection.objects.filter(id=self.kwargs['edit_id'])
        assessment_queryset.update(
                title=section_title_var,
                negative_marking_per_q=negative_marking_per_q_var,
                instructions=instructions_var)
        return redirect('AssessmentSectionQuestionTemplateView', id=self.kwargs['assessment_id'])

class AssessmentSectionQuestionTemplateView(ListView):
    template_name = "content/html/assessment_section_question.html"
    model = AssessmentSection
    paginate_by = settings.PAGINATION_SIZE
    ordering = ['-id']

    def get_queryset(self):
        return self.model.objects.filter(assessment_id=self.kwargs['id']).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(AssessmentSectionQuestionTemplateView, self).get_context_data(**kwargs)
        context['section'] = AssessmentSection.objects.filter(assessment_id=self.kwargs['id']).order_by('-id')
        context['id'] = self.kwargs['id']
        return context

    def post(self, request, *args, **kwargs):
        section_var = self.request.POST.get('section')
        section_title_var = self.request.POST.get('section_title')
        negative_marking_per_q_var = self.request.POST.get('negative_marking_per_q')
        instructions_var = self.request.POST.get('instructions')
        get_section_obj = AssessmentSection.objects.filter(id=int(section_var))
        get_section_obj.update(
                title=section_title_var,
                negative_marking_per_q=float(negative_marking_per_q_var),
                instructions=instructions_var)
        return redirect('AssessmentSectionAddQuestionTemplateView', id=get_section_obj.first().id)

class AddSectionView(View):
    def post(self, request, *args, **kwargs):
        assessmentid = self.kwargs['id']
        section_title_var = self.request.POST.get('section_title')
        section_count_var = int(self.request.POST.get('section_count'))
        instructions_var = self.request.POST.get('instructions')
        negative_marking_per_q_var = self.request.POST.get('negative_marking_per_q')
        for i in range(1, section_count_var + 1):
            AssessmentSection.objects.create(
                    title=section_title_var,
                    assessment_id=int(assessmentid),
                    negative_marking_per_q=negative_marking_per_q_var,
                    instructions=instructions_var)
        return redirect("AssessmentSectionQuestionTemplateView", id=assessmentid)

class AssessmentSectionListView(ListView):
    template_name = "content/html/assessment_section_list.html"
    model = AssessmentSectionQuestion

    def get_queryset(self):
        return self.model.objects.filter(assessment_section_id=self.kwargs['id'])

    def get_context_data(self, *args, **kwargs):
        context = super(AssessmentSectionListView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

    def post(self, request, *args, **kwargs):
        '''
        delete AssessmentSectionQuestion objects using post
        '''
        self.model.objects.get(id=self.request.POST.get('delete_id')).delete()
        return redirect('AssessmentSectionListView', id=self.kwargs['id'])

class AssessmentSectionAddQuestionTemplateView(ListView):
    template_name = "content/html/assessment_question.html"
    model = AssessmentSectionQuestion
    paginate_by = settings.PAGINATION_SIZE
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        context = super(AssessmentSectionAddQuestionTemplateView, self).get_context_data(**kwargs)
        context['question'] = Question.objects.all().order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        question_var = self.request.POST.getlist('question')
        assessment_id_var = self.kwargs['id']
        negative_marking_per_q_var = self.request.POST.get('negative_marking_per_q')
        get_section_obj = AssessmentSection.objects.get(id=int(assessment_id_var))
        for i in question_var:
            AssessmentSectionQuestion.objects.create(
                assessment_section_id=get_section_obj.id,
                negative_marking_per_q=float(negative_marking_per_q_var),
                question_id=int(i))
        return redirect('AssessmentSectionListView', id=assessment_id_var)


class QuestionListTemplateView(LoginRequiredMixin, ListView):
    model = Question
    paginate_by = settings.PAGINATION_SIZE
    template_name = 'content/html/question-bank.html'
    ordering = ['-id']
    filterset_class = QuestionFilter

    def get_queryset(self):
        queryset_model = self.filterset_class(self.request.GET, queryset=self.model.objects.all())
        return queryset_model.qs.order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionListTemplateView, self).get_context_data(**kwargs)
        context['source'] = QuestionCategoryChoices.CHOICES
        context['difficulty'] = DifficultyLevelChoices.CHOICES
        context['question_type'] = QuestionTypeChoices.CHOICES
        return context

class QuestionTemplateView(TemplateView):
    template_name = 'content/html/add.html'
    @login_required_custom(login_url='/')
    def get(self, request, error=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['difficulty_level'] = DifficultyLevelChoices.CHOICES
        context['question_type'] = QuestionTypeChoices.CHOICES
        context['languages'] = Language.objects.all()
        context['source'] = QuestionCategoryChoices.CHOICES
        if error:
            context['error'] = error
        return render(request, self.template_name, context)
    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        true_option_value = int(self.request.POST.get('option_true_value')) - 1
        unique_number_var = self.request.POST.get('unique_number')
        source_name_var = self.request.POST.get('source_name')
        source_unique_number_var = self.request.POST.get('source_unique_number')
        section_number_var = self.request.POST.get('section_number')
        description_var = self.request.POST.get('description')
        option_var = self.request.POST.getlist('option')
        language_var = self.request.POST.get('language')
        mask_var = self.request.POST.get('mask')
        negative_mask_var = self.request.POST.get('negative-mark')
        duration_var = self.request.POST.get('duration')
        difficulty_level_var = self.request.POST.get('difficulty-level')
        solution_var = self.request.POST.get('solution')
        answer_var = self.request.POST.get('answer')
        solution_image_var = self.request.POST.get('solution_image')
        question_type_var = self.request.POST.get('question_type')
        try:
            question_create = Question.objects.create(
                        uid=unique_number_var,
                        question_type=question_type_var,
                        duration_seconds=int(duration_var),
                        marks=int(mask_var),
                        negative_marking=round(float(negative_mask_var), 2),
                        source=1,
                        difficulty=difficulty_level_var)
        except:
            exception_error = "Question with this unique id already exist."
            return self.get(request, error=exception_error, *args, **kwargs)
        else:
            question_statement_create = QuestionStatement.objects.create(
                    question_id=question_create.id,
                    language_id=int(language_var),
                    statement=description_var)
            for i in enumerate(option_var):
                if i[0] == true_option_value:
                    question_option_create = QuestionOptions.objects.create(
                        question_id=question_create.id,
                        is_correct=True)
                    QuestionOptionsExplanation.objects.create(
                        question_option_id=question_option_create.id,
                        language_id=int(language_var),
                        explanation=solution_var)
                else:
                    question_option_create = QuestionOptions.objects.create(
                        question_id=question_create.id,
                        is_correct=False)
                QuestionOptionsStatement.objects.create(
                    question_option_id = question_option_create.id,
                    language_id=int(language_var),
                    statement=i[1])
            return redirect('add_question_bank')


class LectureListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    queryset = Lecture.objects.all()
    ordering = ['id']
    serializer_class = LectureSerializer
    pagination_class = LecturePageNumberPagination
    page_size = 1

    def post(self, request, *args, **kwargs):
        subject_id = request.data.get('subject_id', None)
        if subject_id:
            return self.get(self, request, *args, **kwargs)
        return render_response(data=[], status=0, error=["subject_id field required."])

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return Lecture.objects.filter(subject_id=self.request.data.get('subject_id'),batch=student.batch)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return render_response(data=self.get_paginated_response(serializer.data), error=[], status=1)
        serializer = self.get_serializer(queryset, many=True)
        return render_response(data=self.get_paginated_response(serializer.data), error=[], status=1)


class FacultyLectureListAPIView(LectureListAPIView):

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request,args,kwargs)

    def get_queryset(self):
        return Lecture.objects.filter(faculty=self.request.user)
