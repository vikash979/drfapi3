from django.db import models
from django.conf import settings
from common.choices import ObjectStatusChoices,TOCLevelChoices
# from users.models import User
# from django.contrib.auth import get_user_model
# Create your models here.

# User = get_user_model()
from django.db.models.query import QuerySet

class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(object_status = ObjectStatusChoices.DELETED)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

class ObjectManager(models.Manager):
    def get_queryset(self):
        return SoftDeletionQuerySet(self.model).filter(object_status=ObjectStatusChoices.ACTIVE)

    def complete(self):
        return super().get_queryset()

class BaseResonanceModel(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    object_status = models.SmallIntegerField(choices=ObjectStatusChoices.CHOICES, default=ObjectStatusChoices.ACTIVE)

    # updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,limit_choices_to={'is_staff': True})
    objects = ObjectManager()

    class Meta:
        abstract = True

class BaseTOCModel(BaseResonanceModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=200)

    class Meta:
        abstract = True


class TOCMapping(BaseResonanceModel):

    level = models.SmallIntegerField(choices=TOCLevelChoices.CHOICES)
    toc = models.ForeignKey('subject.TOC',null=True,on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def get_toc_object(self):
        pass
