from django.contrib import admin
from .models import (
    MasterSubject, Subject, TOC
)

admin.site.register(MasterSubject)
admin.site.register(Subject)
admin.site.register(TOC)
# admin.site.register(SubjectUnit)
# admin.site.register(UnitChapter)
# admin.site.register(ChapterTopic)
# admin.site.register(TopicSubtopic)
