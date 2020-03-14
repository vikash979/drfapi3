import datetime
import random

from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied
from common.models import BaseResonanceModel
# from django.contrib.auth.models import UserManager
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models import Count

from institute.models import Batch,Program,Phase,Center

from common.choices import LanguageMediumChoices
from subject.models import Subject

class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django's Group and Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without'
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_groups_set",
        related_query_name="resonance_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_permissions_set",
        related_query_name="resonance_user",
    )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through their
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False

def filter_user_queryset_by_hierarchy(user, queryset,filter_on='assign_to_user__in'):

    if user.is_superuser:
        return queryset
    else:
        all_childrens = user.get_all_child
        return queryset.filter(**{filter_on:all_childrens})


class UserManager(BaseUserManager):
    def create_user(self,username, email, mobile, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(username=username,mobile=mobile, name=name, email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, mobile, name, password):
        user = self.create_user(
            username=username, email=email, password=password, mobile=mobile, name=name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        (1, "Admin"),
        (2, "Author"),
        (3, "Faculty"),
        (4, "Learner"),

    )
    gender_choice = (
        (1, 'Male'),
        (2, 'Female')
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender =  models.PositiveSmallIntegerField(choices=gender_choice,  default=1)
    profile_picture = models.ImageField(upload_to='users/profile/')
    username = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.BigIntegerField("Student Mobile")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','mobile', 'name']

    def has_module_perms(self, app_label):
        return True

    @property
    def get_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def is_member(self, group_name):
        if self.groups.filter(name__iexact=group_name).exists():
            return True
        return False

    def get_full_name(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Token.objects.get_or_create(user=self)


class Division(BaseResonanceModel):
    name = models.CharField('Department name', max_length=120)

    def __str__(self):
        return self.name


class Student(BaseResonanceModel):
    roll_no = models.CharField("Role No", max_length=120,null=True,blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    father_name = models.CharField("Father name", max_length=120,default="",null=True,blank=True)
    father_email = models.CharField("Father Email",max_length=50,default="",null=True,blank=True)
    father_mobile = models.BigIntegerField("Father mobile",default=0,null=True,blank=True)
    mother_name = models.CharField("Mother name", max_length=120,default="",null=True,blank=True)
    mother_email = models.CharField("Mother email",max_length=50,default="",null=True,blank=True)
    mother_mobile = models.BigIntegerField("Mother mobile",default=0,null=True,blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    batch = models.ForeignKey("institute.Batch", null=True, on_delete=models.SET_NULL)
    classs = models.ForeignKey('institute.Classs', null=True,on_delete=models.SET_NULL,blank=True)
    # subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE)
    session = models.ForeignKey('institute.Sessions', null=True,on_delete=models.SET_NULL,blank=True)
    program = models.ForeignKey('institute.Program', null=True,on_delete=models.SET_NULL,blank=True)
    phase = models.ForeignKey('institute.Phase', null=True,on_delete=models.SET_NULL,blank=True)
    # phase_start_date = models.DateField()
    center = models.ForeignKey('institute.Center',null=True,on_delete=models.SET_NULL,blank=True)
    division = models.ForeignKey(Division,null=True,on_delete=models.SET_NULL,blank=True)
    medium = models.PositiveSmallIntegerField(choices=LanguageMediumChoices.CHOICES, default=0,null=True,blank=True)

    def __str__(self):
        return self.user.name

    @property
    def name(self):
        return self.user.name

    @property
    def center_name(self):
        return self.center.name

    @property
    def city_name(self):
        return self.center.city.label

    @property
    def unread_notice_count(self):
        return 123

    @property
    def profile_picture(self):
        return self.user.profile_picture

    def save(self, *args, **kwargs):
        existing = None
        if self.id:
            try:
                existing = Student.objects.get(id=self.id)
            except:
                pass

        super(Student, self).save(*args, **kwargs)

        if not existing:
            subjects = Subject.objects.filter(classs=self.classs)
            for s in subjects:
                StudentSubject.objects.create(student=self,subject=s)
        StudentBatch.objects.get_or_create(student=self,batch=self.batch)

class StudentBatch(BaseResonanceModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey('institute.Batch', null=True,on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('student', 'batch',)


class StudentSubject(BaseResonanceModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey('subject.Subject', null=True,on_delete=models.SET_NULL)


class StudentClassPath(BaseResonanceModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name="class_path")
    classs = models.ForeignKey('institute.Classs', null=True,on_delete=models.SET_NULL)
    is_current = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name="students_class_path")


class Department(BaseResonanceModel):
    name = models.CharField("Department", max_length=120)

    def __str__(self):
        return self.name


class Designation(BaseResonanceModel):
    name = models.CharField("Designation", max_length=120)

    def __str__(self):
        return self.name


class EmploymentType(BaseResonanceModel):
    name = models.CharField("Employment Type Name", max_length=120)

    def __str__(self):
        return self.name


class Faculty(BaseResonanceModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_joining = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    created_on = models.DateTimeField('created Date', auto_now_add=True)
    department = models.ForeignKey(Department, related_name="department", null=True,on_delete=models.SET_NULL)
    designation = models.ForeignKey(Designation, related_name="designation", null=True, on_delete=models.SET_NULL)
    employment_type = models.ForeignKey(EmploymentType, related_name="employee_type", null=True, on_delete=models.SET_NULL)
    employee_code = models.CharField(max_length=20)
    division = models.ForeignKey(Division,null=True,  on_delete=models.SET_NULL)
    center=models.ForeignKey(Center,null=True, related_name="center", on_delete=models.SET_NULL)
    reporting_manager = models.ForeignKey("self",null=True, blank=True, on_delete=models.SET_NULL)
    short_name = models.CharField(max_length=255,blank=True,null=True,default="")

class FacultyBatch(BaseResonanceModel):
    faculty = models.ForeignKey(Faculty,  on_delete=models.CASCADE, related_name='batch')
    batch = models.ForeignKey(Batch, related_name="faculty_batch", on_delete=models.CASCADE,null=True)

    def __str__(self):
        return "{} : {}".format(self.faculty.user.name,self.batch.label)

class FacultySubject(BaseResonanceModel):
    faculty = models.ForeignKey(Faculty,  on_delete=models.CASCADE, related_name='subject')
    subject = models.ForeignKey(Subject, related_name="faculty_subject", on_delete=models.CASCADE,null=True)

    def __str__(self):
        return "{} : {}".format(self.faculty.user.name,self.subject.label)

class FacultyProgram(BaseResonanceModel):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='programs')
    Program = models.ForeignKey('institute.Program', related_name="faculty_program", on_delete=models.CASCADE,null=True)

    def __str__(self):
        return "{} : {}".format(self.faculty.user.name,self.Program.label)

class FacultyPhase(BaseResonanceModel):
    faculty = models.ForeignKey(Faculty,  on_delete=models.CASCADE, related_name='phases')
    phase = models.ForeignKey('institute.Phase', related_name="faculty_phase", on_delete=models.CASCADE,null=True)

    def __str__(self):
        return "{} : {}".format(self.faculty.user.name,self.phase.label)
# class UserConcept(BaseResonanceModel):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='concepts')
#     concept = models.ForeignKey("content.Concept", on_delete=models.SET_NULL,null=True)
#
#     def __str__(self):
#         return "{} {}".format(self.user.name, self.concept.name)
