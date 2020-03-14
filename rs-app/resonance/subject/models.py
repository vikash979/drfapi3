from django.db import models
from django.conf import settings
from common.models import BaseResonanceModel,BaseTOCModel
from common.choices import TOCLevelChoices
from django.contrib.auth import get_user_model
from common.choices import *


class MasterSubject(BaseTOCModel):
    short_code = models.CharField(max_length=20)
    url = models.ImageField(upload_to='subjects/')
    background_code = models.CharField(max_length=10, default='#0000FF')
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.label

class Subject(BaseTOCModel):
    subject_choice = (
        (1, "One"),
        (2, "Two"),
    )

    description = models.TextField(blank=True,null=True)
    classs = models.ForeignKey("institute.Classs",related_name ="subject_class", null=True, on_delete=models.SET_NULL)
    master_subject = models.ForeignKey(MasterSubject,on_delete=models.CASCADE)
    # subject_optional  = models.IntegerField(choices = subject_choice,default = 1)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.label


class TOC(BaseResonanceModel):
    label = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    level = models.SmallIntegerField(choices=TOCLevelChoices.CHOICES, default=0)
    parent = models.ForeignKey("self",null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey("subject.Subject",related_name ="toc" , null=True,on_delete=models.SET_NULL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.label

    @property  
    def get_unit(self):
        return self.toc_set.all()

    @property
    def get_chapter(self):
        return self.toc_set.all()

    @property
    def get_topic(self):
        return self.toc_set.all()
    @property
    def get_subtopic(self):
        return self.toc_set.all()


# class SubjectUnit(BaseTOCModel):
#     order = models.IntegerField()
#     subject = models.ForeignKey(Subject,null=True, on_delete=models.SET_NULL)


# class UnitChapter(BaseTOCModel):
#     order = models.BigIntegerField(default=0)
#     unit = models.ForeignKey(SubjectUnit, null=True, on_delete=models.SET_NULL)

# class ChapterTopic(BaseTOCModel):
#     order = models.BigIntegerField(default=0)
#     chapter = models.ForeignKey(UnitChapter, null=True, on_delete=models.SET_NULL)

# class TopicSubtopic(BaseTOCModel):
#     order = models.IntegerField(default=0)
#     level = models.PositiveSmallIntegerField(default=0)
#     topic = models.ForeignKey(ChapterTopic,null=True, on_delete=models.SET_NULL)
#
