from django.contrib import admin
from .models import (
    Lecture, LectureTOCMapping, Content, ContentTOCMapping, StudyMaterial, StudyMaterialFile,
     Language, Assessment, DPPPlanner, AssessmentSection, AssessmentSectionQuestion, Question,
     LectureTOCContent,QuestionStatement, QuestionOptions, QuestionOptionsStatement, 
     QuestionOptionsExplanation, AssessmentAttempt,NotesAccessLog,VideoAccessLog,AssesmentAttemptQuestion
)
# Register your models here.

admin.site.register(Lecture)
admin.site.register(Language)
admin.site.register(LectureTOCMapping)
admin.site.register(Content)
admin.site.register(ContentTOCMapping)
admin.site.register(StudyMaterial)
admin.site.register(StudyMaterialFile)
admin.site.register(Assessment)
admin.site.register(LectureTOCContent)
admin.site.register(DPPPlanner)
admin.site.register(AssessmentSection)
admin.site.register(AssessmentSectionQuestion)
admin.site.register(Question)
admin.site.register(QuestionStatement)
admin.site.register(QuestionOptions)
admin.site.register(QuestionOptionsStatement)
admin.site.register(QuestionOptionsExplanation)
admin.site.register(AssessmentAttempt)
admin.site.register(NotesAccessLog)
admin.site.register(VideoAccessLog)
admin.site.register(AssesmentAttemptQuestion)