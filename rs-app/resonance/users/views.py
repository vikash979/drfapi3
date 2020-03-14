from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import CreateView
from users.models import User, Student, Division,StudentBatch, EmploymentType, Designation, Department,Faculty,FacultyBatch,FacultySubject, StudentSubject
from institute.models import Batch, Center,Phase,Sessions,SessionProgram,Classs,Program,ProgramClass
from subject.models import Subject
from users.forms import StudentForm
from django.views.generic import TemplateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import StudentSerializer, StudentSubjectSerializer
from .facultyserializer import FacultyFacultySerializer
from rest_framework import permissions,authentication
import re
from datetime import datetime
from django.conf import settings
import django_filters
from django.core.files.storage import FileSystemStorage
from common.views import login_required_custom



#regex_var_email = re.compile('^\w+@\w+.(\w+)+$')
regex_var_email = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
regex_var_mobile = re.compile('^[5-9][0-9]{9}$')

def render_response(data=None, status=None, error=None):
    if data and status:
        return Response({'data': data, 'error': [], 'status': status})
    return Response({'data': None, 'error': [error], 'status': status})

class StudentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        get_student = Student.objects.all().first()
        get_student = Student.objects.filter(user=request.user).first()
        student_profile_serializer_data = StudentSerializer(get_student,many=False).data
        # get_student_subjects = StudentSubject.objects.filter(student_id = student_profile_serializer_data['id'])
        # subject_serializer = StudentSubjectSerializer(get_student_subjects, many=True)
        # student_profile_serializer_data['subjects'] = []
        # for i in enumerate(subject_serializer.data):
        #     student_profile_serializer_data['subjects'].append(dict())
        #     student_profile_serializer_data['subjects'][i[0]]['id'] = i[1]['subject']['id']
        #     student_profile_serializer_data['subjects'][i[0]]['label'] = i[1]['subject']['label']
        #     student_profile_serializer_data['subjects'][i[0]]['url'] = i[1]['subject']['master_subject']['url']
        #     student_profile_serializer_data['subjects'][i[0]]['background_code'] = i[1]['subject']['master_subject']['background_code']
        return render_response(data=student_profile_serializer_data, error=[], status=1)

class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        pass

class EmptyView(View):
    @login_required_custom(login_url='/')
    def get(self,request,*args,**kwargs):
        return HttpResponseRedirect('dashboard/')

class DashboardView(TemplateView):
    template_name = "users/index.html"
    @login_required_custom(login_url='/')
    def get(self,request,*args,**kwargs):
        context_data={}
        return render(request, self.template_name, context_data)

class StudentCreateView(CreateView):

	form_class = StudentForm
	template_name = "users/student-create.html"
	model = Student

	def form_valid(self, form):
		data = form.cleaned_data
		email = data['email']
		name = data['name']
		user = User.objects.create_user(name=name, email=email)
		student = form.save(commit=False)
		student.user = user
		student.save()
		return HttpResponse("Student Successfully Created ")


class LoginView(View):
	pass

	# model = User
context_data={}
def paginator_maker(request_args,model):
    page = request_args.GET.get("page")
    if page == None:
        page=1
    else:
        try:
            page=int(page)
        except:
            page=1
    paginator = Paginator(model,settings.PAGINATION_SIZE)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    batch_numpages = paginator.num_pages
    if batch_numpages > 0:
        batch_numpage =  batch_numpages
        if page >1:
            batch_previous_page = users.previous_page_number()
            current_page = users.number
        else:
            batch_previous_page = 1
            current_page = 1
        if page==batch_numpage:
            batch_next_page=page
        else:
            batch_next_page=users.next_page_number()
    context_data["batch_numpage"]=batch_numpages
    context_data["batch_previous_page"]=batch_previous_page
    context_data["batch_next_page"]=batch_next_page
    context_data["current_page"]=current_page
    return users

def render_statement(reques_args,status,message,template,model):
    context_data["status"]=status
    context_data["message"]=message
    context_data["data"]=model
    return render(reques_args, template, context_data)

def get_for_ed(request,model,template):
    context_data["status"]=""
    req_obj = model.objects.all().filter(object_status=0).order_by("-id")
    req_obj = paginator_maker(request,req_obj)
    context_data["data"]=req_obj
    return render(request, template, context_data)

def post_for_ed(request,model,template):
    req_obj_all = model.objects.all().filter(object_status=0).order_by("-id")
    req_obj_all = paginator_maker(request,req_obj_all)
    name= request.POST.get("name")
    id=request.POST.get("id")
    action=request.POST.get("action")
    id=id.strip()
    if action==None:
        if len(id)==0:
            if name:
                name=name.strip()
                if len(name)!=0:
                    req_obj = model.objects.get_or_create(name=name,object_status=0)
                    if req_obj[1]==False:
                        return render_statement(request,False,"Record Already Exists, Not Updated",template,req_obj_all)
                    elif req_obj[1]==True:
                        return render_statement(request,True,"Successfully created",template,req_obj_all)
                else:
                    return render_statement(request,False,"please provide your input",template,req_obj_all)
            else:
                return render_statement(request,False,"please provide your input",template,req_obj_all)
        else:
            id=id.strip()
            print("id is",id)
            id=int(id)
            name = request.POST.get("name")
            name = name.strip()
            req_data = request.POST
            if len(name) != 0:
                try:
                    req_update_object = model.objects.get(name= name,object_status=0)
                    return render_statement(request,False,"Record Already Exist",template,req_obj_all)
                except:
                    updatable = ["name"]
                    try:
                        req_obj = model.objects.get(id=id,object_status=0)
                    except:
                        return render_statement(request,False,"no record found",template,req_obj_all)
                    for attr in updatable :
                        if attr in req_data :
                            setattr(req_obj,attr,req_data[attr])
                    req_obj.save()
                    return render_statement(request,True,"Successfully updated",template,req_obj_all)
            else:
                return render_statement(request,False,"Please provide valid input",template,req_obj_all)
    else:
        if action=="delete":
            id = request.POST.get("id")
            if id!=None:
                id=id.strip()
                req_obj = model.objects.filter(id=id).delete()
                return render_statement(request,"Deleted","Successfully deleted",template,req_obj_all)


class DepartmentsViews(TemplateView):
    template_name = "users/department.html"
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_ed(request,Department,self.template_name)
    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_ed(request,Department,self.template_name)


class EmployementsViews(TemplateView):
    template_name = "users/employment-type.html"

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_ed(request,EmploymentType,self.template_name)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_ed(request,EmploymentType,self.template_name)

class DivisionsViews(TemplateView):
    template_name = "users/division.html"

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_ed(request,Division,self.template_name)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_ed(request,Division,self.template_name)

class DesignationViews(TemplateView):
    template_name = "users/designation.html"

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_ed(request,Designation,self.template_name)
    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_ed(request,Designation,self.template_name)

def render_statement_user(reques_args,status,message,template,model=None):

    req_division=Division.objects.all().filter(object_status=0).order_by("-id")
    req_department=Department.objects.all().filter(object_status=0).order_by("-id")
    req_designation=Designation.objects.all().filter(object_status=0).order_by("-id")
    req_employement=EmploymentType.objects.all().filter(object_status=0).order_by("-id")
    req_batch=Batch.objects.all().filter(object_status=0).order_by("-id")
    req_subject = Subject.objects.all().filter(object_status=0).order_by("-id")
    req_center = Center.objects.all().filter(object_status=0).order_by("-id")
    req_user = User.objects.filter(role__in=[1,2,3]).values('id','name')
    role_userob = []
    for user_details in req_user:
        role_userob.append(user_details['id'])

    requ_users = Faculty.objects.filter(user_id__in=role_userob).values('id',)
    context_data["division"]=req_division
    context_data["user"]=req_user
    context_data["department"]=req_department
    context_data["designation"]=req_designation
    context_data["employement"]=req_employement
    context_data["batch"]=req_batch
    context_data["subject"]=req_subject
    context_data["center"]=req_center
    context_data["status"]=status
    context_data["message"]=message
    return render(reques_args, template, context_data)

def func_for_error(request):
    req_dic2 = {}
    if "role" in request.POST :
        req_dic2["name"],req_dic2["department"],req_dic2["designation"]=request.POST.get("name"),request.POST.get("department"),request.POST.get("designation")
        req_dic2["center"],req_dic2["role"]=request.POST.get("center"),request.POST.get("role")
        req_dic2["division"],req_dic2["employement_type"]=request.POST.get("division"),request.POST.get("employement_type")
        req_dic2["employee_code"]=request.POST.get("employee_code")
        req_dic2["country"]=request.POST.get("Country")
        req_dic2["state"]=request.POST.get("State")
        req_dic2["city"]=request.POST.get("City")
        req_dic2["email"],req_dic2["mobile"],req_dic2["short_name"]=request.POST.get("email"),request.POST.get("mobile"),request.POST.get("short_name")
        req_dic2["subject"]= "".join(request.POST.getlist("subject"))
        req_dic2["batch"]= "".join(request.POST.getlist("batch"))
        req_dic2["reporting"] = request.POST.get("reporting")
    else:
        req_dic2["name"],req_dic2["student_email"],req_dic2["student_mobile"]=request.POST.get("name"), request.POST.get("student_email"), request.POST.get("student_mobile")
        req_dic2["student_dob"],req_dic2["gender"],req_dic2["division"]=request.POST.get("student_dob"),request.POST.get("gender"), request.POST.get("division")
        req_dic2["medium"],req_dic2["center"],req_dic2["role_number"]=request.POST.get("medium"), request.POST.get("center"), request.POST.get("role_number")
        req_dic2["phase"], req_dic2["session"], req_dic2["program"], req_dic2["classs"]=request.POST.get("phase"), request.POST.get("session"), request.POST.get("program"), request.POST.get("class")
        req_dic2["father_name"], req_dic2["mother_name"], req_dic2["father_email"], req_dic2["mother_email"],req_dic2["father_mobile"],req_dic2["mother_mobile"]=request.POST.get("father_name"), request.POST.get("mother_name"), request.POST.get("father_email"), request.POST.get("mother_email"),request.POST.get("father_mobile"),request.POST.get("mother_mobile")
        req_dic2["country"],req_dic2["state"],req_dic2["city"]=request.POST.get("country"),request.POST.get("state"),request.POST.get("city")
    return req_dic2

def get_for_faculty(request,template,model=None):

    return render_statement_user(request,"","",template)

def post_for_faculty(request,template,model=None):
    action=request.POST.get("action")
    if action==None:
        reporting = request.POST.get("reporting")
        if len(reporting)!=0:
            reporting = int(reporting)
        profile_picture = request.FILES.get("profile_pic")
        name,subject,role=request.POST.get("name"), request.POST.getlist("subject"), request.POST.get("role")
        department,designation,employement_type=request.POST.get("department"),request.POST.get("designation"), request.POST.get("employement_type")
        batch,center,division=request.POST.getlist("batch"), request.POST.get("center"), request.POST.get("division")
        mobile, email, short_name, employee_code=request.POST.get("mobile"), request.POST.get("email"), request.POST.get("short_name"), request.POST.get("employee_code")
        if name and subject and role and department and designation and employement_type and center and division and mobile and email and employee_code:
            name,role,department,designation,employement_type,center,division,mobile,email,employee_code=name.strip(),role.strip(),department.strip(),designation.strip(),employement_type.strip(),center.strip(),division.strip(),mobile.strip(),email.strip(),employee_code.strip()
            if len(subject)!=0 and len(name)!=0 and len(role)!=0 and len(department)!=0 and len(designation)!=0 and len(employement_type)!=0 and len(center)!=0 and len(division)!=0 and len(mobile)!=0 and len(email)!=0 and len(employee_code)!=0:
                faculty_result_email = bool(regex_var_email.search(email))
                faculty_result_mobile = bool(regex_var_mobile.search(mobile))
                if faculty_result_email==True and faculty_result_mobile ==True:
                    email=email
                    mobile=mobile
                else:
                    # context_data["req_update"]=func_for_error(request)
                    return render_statement_user(request,False,"Either your email or mobile number is not correct",template)
                try:

                    req_user=User.objects.get(username=employee_code)
                    
                    # context_data["req_update"]=func_for_error(request)
                    return render_statement_user(request,False,"User Already Exists",template)
                except:
                    if profile_picture!=None:
                        req_user = User.objects.create(username=employee_code,is_staff=True,name=name,profile_picture=profile_picture,email=email,mobile=mobile,role=role,password='reson@123')
                    else:
                        req_user = User.objects.create(username=employee_code,is_staff=True,name=name,email=email,mobile=mobile,role=role,password='reson@123')

                    try:
                        Faculty.objects.get(user_id=reporting)
                        req_faculty=Faculty.objects.create(user=User.objects.get(id=req_user.id),status=True,department=Department.objects.get(id=department),designation=Designation.objects.get(id=designation),division=Division.objects.get(id=division),employment_type=EmploymentType.objects.get(id=employement_type),center=Center.objects.get(id=center),short_name=short_name,reporting_manager=Faculty.objects.get(user_id=User.objects.get(id=reporting)))
                    except:
                        req_faculty=Faculty.objects.create(user=User.objects.get(id=req_user.id),status=True,department=Department.objects.get(id=department),designation=Designation.objects.get(id=designation),division=Division.objects.get(id=division),employment_type=EmploymentType.objects.get(id=employement_type),center=Center.objects.get(id=center),short_name=short_name)

                    for record in subject:
                        req_Faculty_subject=FacultySubject.objects.create(faculty=Faculty.objects.get(id=req_faculty.id), subject=Subject.objects.get(id=record))
                    if len(batch)!=0:
                        for batchrecord in batch:
                            req_Faculty_batch=FacultyBatch.objects.create(faculty=Faculty.objects.get(id=req_faculty.id), batch=Batch.objects.get(id=batchrecord))
                    return render_statement_user(request,True,"Faculty Successfully Created",template,model)
            else:
                context_data["req_update"]=func_for_error(request)
                return render_statement_user(request,False,"Fields cannot be blank",template)
        else:
            context_data["req_update"]=func_for_error(request)
            return render_statement_user(request,False,"Please check your input",template)
    else:
        if action=="delete":
            id = request.POST.get("id")
            if id!=None:
                id=id.strip()
                req_obj = Faculty.objects.filter(id=id).delete()
                req_all_obj = Faculty.objects.all().filter(status=True,object_status=0).order_by("-id")
                req_dic = {}
                req_all_obj = paginator_maker(request,req_all_obj)
                context_data["data"]=req_all_obj
                for i in req_all_obj:
                    req_dic2={}
                    req_dic2["name"],req_dic2["id"],req_dic2["department"],req_dic2["designation"]=i.user.name,i.id,i.department.name,i.designation.name
                    req_dic2["center"],req_dic2["role"],req_dic[i.user.name]=i.center.name,i.user.role,req_dic2
                    req_Faculty_subject=FacultySubject.objects.filter(faculty_id=i.id)
                    fac_sub = ""
                    for j in req_Faculty_subject:
                        fac_sub+=" {},".format(j.subject.label)
                    req_dic2["subject"]= fac_sub
                context_data["fulldata"]=req_dic
                return render_statement_user(request,"Deleted","Successfully Deleted","users/listing.html")

def get_for_updatefaculty(request,template,model=None):
    req_dic2 = {}
    req_dic2["name"],req_dic2["username"],req_dic2["id"],req_dic2["department"],req_dic2["designation"]=model.user.name,model.user.username,model.id,model.department.id,model.designation.id
    req_dic2["center"],req_dic2["role"]=model.center.id,model.user.role
    req_dic2["division"],req_dic2["employement_type"]=model.division.id,model.employment_type.id
    req_dic2["country"]=model.center.country.id
    req_dic2["state"]=model.center.state.id
    req_dic2["city"]=model.center.city.id
    req_dic2["profile_pic"]="/media/"+str(model.user.profile_picture)
    req_dic2["email"],req_dic2["mobile"],req_dic2["short_name"]=model.user.email,model.user.mobile,model.short_name
    
    req_dic2["reporting"]=model.reporting_manager.user.id
    req_Faculty_subject=FacultySubject.objects.filter(faculty_id=model.id,object_status=0)
    req_Faculty_Batch = FacultyBatch.objects.filter(faculty_id=model.id,object_status=0)
    fac_sub = ""
    fac_batch =""
    for j in req_Faculty_subject:
        fac_sub+=str(j.subject.id)
    req_dic2["subject"]= fac_sub
    if len(req_Faculty_Batch)!=0:
        for k in req_Faculty_Batch:
            fac_batch+=str(k.batch.id)
        req_dic2["batch"]= fac_batch
    else:
        req_dic2["batch"]= fac_batch
    context_data["req_update"]=req_dic2
    return render_statement_user(request,"","",template)


def post_for_updatefaculty(request,template,model=None):
    id=request.POST.get("id")
    reporting = request.POST.get("reporting")
    if len(reporting)!=0:
        reporting = int(reporting)
    profile_picture = request.FILES.get("profile_pic")
    name,subject,role=request.POST.get("name"), request.POST.getlist("subject"), request.POST.get("role")
    department,designation,employement_type=request.POST.get("department"),request.POST.get("designation"), request.POST.get("employement_type")
    batch,center,division=request.POST.getlist("batch"), request.POST.get("center"), request.POST.get("division")
    mobile, email, short_name, employee_code=request.POST.get("mobile"), request.POST.get("email"), request.POST.get("short_name"), request.POST.get("employee_code")
    if name and subject and role and department and designation and employement_type and center and division and mobile and email and employee_code:
        name,role,department,designation,employement_type,center,division,mobile,email,employee_code=name.strip(),role.strip(),department.strip(),designation.strip(),employement_type.strip(),center.strip(),division.strip(),mobile.strip(),email.strip(),employee_code.strip()
        if len(subject)!=0 and len(name)!=0 and len(role)!=0 and len(department)!=0 and len(designation)!=0 and len(employement_type)!=0 and len(center)!=0 and len(division)!=0 and len(mobile)!=0 and len(email)!=0 and len(employee_code)!=0:
            faculty_result_email = bool(regex_var_email.search(email))
            faculty_result_mobile = bool(regex_var_mobile.search(mobile))
            if faculty_result_email==True and faculty_result_mobile ==True:
                email=email
                mobile=mobile
            else:
                return render_statement_user(request,False,"Either your email or mobile number is not correct",template,model)
            
            try:
                req_user=Faculty.objects.get(id=id).user
                req_user_id=req_user.id
            except:
                return render_statement_user(request,False,"No Record Found on id",template,model)
            if req_user_id == reporting:
                return render_statement_user(request,False,"Cannot assign the selected reporting manager",template,model)
            if req_user.username == employee_code:
                if profile_picture!=None:
                    fs1=FileSystemStorage()
                    fs1.save(profile_picture.name, profile_picture)
                    update_user= User.objects.filter(id=req_user_id).update(name=name,email=email,mobile=mobile,role=role,profile_picture=profile_picture)
                else:
                    update_user= User.objects.filter(id=req_user_id).update(name=name,email=email,mobile=mobile,role=role)
                update_faculty=Faculty.objects.filter(id=id)
                if type(reporting)==int:
                    update_faculty=Faculty.objects.filter(id=id,object_status=0).update(department_id=department,designation_id=designation,division_id=division,employment_type_id=employement_type,center_id=center,short_name=short_name,reporting_manager=Faculty.objects.get(user_id=User.objects.get(id=reporting)))
                else:
                    update_faculty=Faculty.objects.filter(id=id,object_status=0).update(department_id=department,designation_id=designation,division_id=division,employment_type_id=employement_type,center_id=center,short_name=short_name)
                req_Faculty_Subject=FacultySubject.objects.filter(faculty_id=id).update(object_status=1)
                req_Faculty_Batch=FacultyBatch.objects.filter(faculty_id=id).update(object_status=1)
                for record in subject:
                    req_Faculty_subject=FacultySubject.objects.create(faculty_id=id, subject_id=record)
                if len(batch)!=0:
                    for batchrecord in batch:
                        req_Faculty_batch=FacultyBatch.objects.create(faculty_id=id, batch_id=batchrecord)
                return render_statement_user(request,True,"Faculty Successfully Updated",template,model)
            else:
                return render_statement_user(request,False,"Employee Code cannot be updated",template,model)
        else:
            return render_statement_user(request,False,"Fields cannot be blank",template)
    else:
        return render_statement_user(request,False,"Please check your input",template)

class FacultyFilter(django_filters.FilterSet):
    designation_id = django_filters.ModelMultipleChoiceFilter(queryset=Designation.objects.all())
    department_id = django_filters.ModelMultipleChoiceFilter(queryset=Department.objects.all())
    division_id = django_filters.ModelMultipleChoiceFilter(queryset=Division.objects.all())
    employement_type_id = django_filters.ModelMultipleChoiceFilter(queryset=EmploymentType.objects.all())
    subject_id = django_filters.ModelMultipleChoiceFilter(queryset=FacultySubject.objects.all())
    batch_id = django_filters.ModelMultipleChoiceFilter(queryset=FacultyBatch.objects.all())
    class Meta:
        model = Faculty
        fields = ['designation_id', 'department_id', 'division_id', 'employement_type_id']

class FacultySubjectFilter(django_filters.FilterSet):
    subject_id = django_filters.ModelMultipleChoiceFilter(queryset=FacultySubject.objects.all())
    class Meta:
        model = FacultySubject
        fields = ['subject_id']

class FacultyBatchFilter(django_filters.FilterSet):
    batch_id = django_filters.ModelMultipleChoiceFilter(queryset=FacultyBatch.objects.all())
    class Meta:
        model = FacultyBatch
        fields = ['batch_id']

class FacultiesViews(TemplateView):
    template_name = "users/listing.html"
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        req_all_obj = Faculty.objects.all().filter(status=True,object_status=0).order_by("-id")
        req_all_obj = FacultyFilter(request.GET, queryset=req_all_obj)
        req_all_obj = FacultySubjectFilter(request.GET, queryset=req_all_obj.qs)
        req_all_obj = FacultyBatchFilter(request.GET, queryset=req_all_obj.qs)


        req_all_obj=paginator_maker(request,req_all_obj.qs)
        req_dic = {}
        context_data["data"]=req_all_obj
        for i in req_all_obj:
            req_dic2={}
            req_dic2["name"],req_dic2["id"],req_dic2["department"],req_dic2["designation"]=i.user.name,i.id,i.department.name,i.designation.name
            req_dic2["center"],req_dic2["role"],req_dic2["profile_pic"],req_dic[i.user.name]=i.center.name,i.user.role,"/media/"+str(i.user.profile_picture),req_dic2
            req_Faculty_subject=FacultySubject.objects.filter(faculty_id=i.id)
            fac_sub = ""
            for j in req_Faculty_subject:
                fac_sub+=" {},".format(j.subject.label)
            req_dic2["subject"]= fac_sub
        context_data["fulldata"]=req_dic
        return render_statement_user(request,"","",self.template_name)

class AddFacultiesViews(TemplateView):
    template_name = "users/add.html"

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        
        return get_for_faculty(request,self.template_name)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        req_all_obj = Faculty.objects.all().filter(status=True).order_by("-id")
        context_data["data"]=req_all_obj
        return post_for_faculty(request,self.template_name)

class UpdateFacultiesViews(TemplateView):
    template_name = "users/update_faculty.html"

    @login_required_custom(login_url='/')
    def get(self, request,id, *args, **kwargs):
        try:
            req_fac_obj = Faculty.objects.get(id=id,status=True,object_status=0)
        except:
            context_data["data"]=None
            return render_statement_user(request,False,"No Record Found",self.template_name,context_data)
        return get_for_updatefaculty(request,self.template_name,req_fac_obj)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        req_all_obj = Faculty.objects.all().filter(status=True).order_by("-id")
        context_data["data"]=req_all_obj
        return post_for_updatefaculty(request,self.template_name)

def render_statement_student(reques_args,status,message,template,model=None):
    req_division=Division.objects.all().filter(object_status=0).order_by("-id")
    req_phase = Phase.objects.all().filter(object_status=0).order_by("-id")
    req_batch = Batch.objects.all().filter(object_status=0).order_by("-id")
    req_session = Sessions.objects.all().filter(object_status=0).order_by("-id")
    req_class = Classs.objects.all().filter(object_status=0).order_by("-id")
    req_sub_batch = StudentBatch.objects.all().filter(object_status=0).values()
    req_program = Program.objects.all().filter(object_status=0).order_by("-id")
    req_center = Center.objects.all().filter(object_status=0).order_by("-id")
    context_data["division"],context_data["batch"],context_data["subject_batch"],context_data["phase"],context_data["session"],context_data["class"],context_data["program"]=req_division,req_batch,req_sub_batch,req_phase,req_session,req_class,req_program
    context_data["status"]=status
    context_data["message"]=message
    context_data["center"]=req_center
    return render(reques_args, template, context_data)

def get_for_updatestudent(request,template,model=None):
    context_data["data"]=model
    context_data["subject"]=Subject.objects.all().filter(object_status=0).order_by("-id")
    return render_statement_student(request,"","",template)

def post_for_add_student(request,template):
    action=request.POST.get("action")
    if action==None:
        profile_picture = request.FILES.get("profile_pic")
        subject_ob = request.POST.getlist('subject')
        name,student_email,student_mobile=request.POST.get("name"), request.POST.get("student_email"), request.POST.get("student_mobile")
        student_dob,gender,division=request.POST.get("student_dob"),request.POST.get("gender"), request.POST.get("division")
        medium,center,role_number=request.POST.get("medium"), request.POST.get("center"), request.POST.get("role_number")
        phase, session, program, classs=request.POST.get("phase"), request.POST.get("session"), request.POST.get("program"), request.POST.get("class")
        father_name, mother_name, father_email, mother_email,father_mobile,mother_mobile=request.POST.get("father_name"), request.POST.get("mother_name"), request.POST.get("father_email"), request.POST.get("mother_email"),request.POST.get("father_mobile"),request.POST.get("mother_mobile")
        if name and student_email and student_mobile and gender and student_dob and division and center and medium and role_number and session and program and classs:
            name,student_email,student_mobile,gender,division,center,medium,role_number,session,program,classs=name.strip(),student_email.strip(),student_mobile.strip(),gender.strip(),division.strip(),center.strip(),medium.strip(),role_number.strip(),session.strip(),program.strip(),classs.strip()
            if len(name)!=0 and len(student_email)!=0 and len(student_mobile)!=0 and len(gender)!=0 and len(division)!=0 and len(center)!=0 and len(medium)!=0 and len(role_number)!=0 and len(session)!=0 and len(program)!=0 and len(classs)!=0:
                role_number=str(role_number)
                date_of_birth = datetime.strptime(student_dob, "%Y-%m-%d").date()
                student_result_email = bool(regex_var_email.search(student_email))
                student_result_mobile = bool(regex_var_mobile.search(student_mobile))
                if student_result_email==True and student_result_mobile ==True:
                    student_email=student_email
                    student_mobile=student_mobile
                else:
                    # context_data["req_update"]=func_for_error(request)
                    return render_statement_student(request,False,"Either your email or mobile number is not correct",template)
                father_email,mother_email,father_mobile,mother_mobile=father_email.strip(),mother_email.strip(),father_mobile.strip(),mother_mobile.strip()
                try:
                    req_user=User.objects.get(username=role_number)
                    # context_data["req_update"]=func_for_error(request)
                    return render_statement_student(request,False,"User Already Exists",template)
                except:
                    if profile_picture!=None:
                        req_user = User.objects.create(username=role_number,name=name,email=student_email,mobile=student_mobile,password='reson@123',gender=gender,date_of_birth=date_of_birth,profile_picture=profile_picture)
                    else:
                        req_user = User.objects.create(username=role_number,name=name,email=student_email,mobile=student_mobile,password='reson@123',gender=gender,date_of_birth=date_of_birth)
                    req_student=Student.objects.create(user_id=req_user.id,status=True,roll_no=role_number,session_id=session,classs_id=classs,program_id=program,phase_id=phase,center_id=center,division_id=division,medium=medium,father_name=father_name,mother_name=mother_name)

                    StudentBatch.objects.create(student_id = req_student.id,batch_id  = int(request.POST.get("current_batch")))
                    if len(father_email)!=0:
                        result_email = bool(regex_var_email.search(father_email))
                        if result_email==True:
                            Student.objects.filter(user_id=req_user.id).update(father_email=father_email)
                    if len(mother_email)!=0:
                        result_email = bool(regex_var_email.search(mother_email))
                        if result_email==True:
                            Student.objects.filter(user_id=req_user.id).update(mother_email=mother_email)
                    if len(father_mobile)!=0:
                        result_mobile=bool(regex_var_mobile.search(father_mobile))
                        if result_mobile==True:
                            Student.objects.filter(user_id=req_user.id).update(father_mobile=father_mobile)
                    if len(mother_mobile)!=0:
                        result_mobile=bool(regex_var_mobile.search(mother_mobile))
                        if result_mobile==True:
                            Student.objects.filter(user_id=req_user.id).update(mother_mobile=mother_mobile)
                    return render_statement_student(request,True,"Student Successfully Created",template)
            else:
                # context_data["req_update"]=func_for_error(request)
                return render_statement_student(request,False,"Fields cannot be blank",template)
        else:
            # context_data["req_update"]=func_for_error(request)
            return render_statement_student(request,False,"Fields cannot be blank",template)
    else:
        if action=="delete":
            id = request.POST.get("id")
            if id!=None:
                id=id.strip()
                req_obj = Student.objects.filter(id=id).delete()
                req_all_obj = Student.objects.all().filter(status=True,object_status=0).order_by("-id")
                req_all_obj=paginator_maker(request,req_all_obj)
                context_data["data"]=req_all_obj
                return render_statement_student(request,"Deleted","Successfuly deleted","users/students.html")

def post_for_updatestudent(request,template,model=None):
    id=request.POST.get("id")
    profile_picture = request.FILES.get("profile_pic")
    current_batch = request.POST.get("current_batch")
    name,student_email,student_mobile=request.POST.get("name"), request.POST.get("student_email"), request.POST.get("student_mobile")
    student_dob,gender,division=request.POST.get("student_dob"),request.POST.get("gender"), request.POST.get("division")
    medium,center,role_number=request.POST.get("medium"), request.POST.get("center"), request.POST.get("role_number")
    phase, session, program, classs=request.POST.get("phase"), request.POST.get("session"), request.POST.get("program"), request.POST.get("class")
    father_name, mother_name, father_email, mother_email,father_mobile,mother_mobile=request.POST.get("father_name"), request.POST.get("mother_name"), request.POST.get("father_email"), request.POST.get("mother_email"),request.POST.get("father_mobile"),request.POST.get("mother_mobile")
    if name and student_email and student_mobile and student_dob and gender and division and center and medium and role_number and phase and session and program and classs:
        name,student_email,student_mobile,gender,division,center,medium,role_number,phase,session,program,classs=name.strip(),student_email.strip(),student_mobile.strip(),gender.strip(),division.strip(),center.strip(),medium.strip(),role_number.strip(),phase.strip(),session.strip(),program.strip(),classs.strip()
        if len(name)!=0 and len(student_email)!=0 and len(student_mobile)!=0 and len(gender)!=0 and len(division)!=0 and len(center)!=0 and len(medium)!=0 and len(role_number)!=0 and len(phase)!=0 and len(session)!=0 and len(program)!=0 and len(classs)!=0:
            role_number=str(role_number)
            date_of_birth = datetime.strptime(student_dob, "%Y-%m-%d").date()
            student_result_email = bool(regex_var_email.search(student_email))
            student_result_mobile = bool(regex_var_mobile.search(student_mobile))
            try:
                req_user=Student.objects.get(id=id).user
                req_user_id=req_user.id
            except:
                context_data["data"]=None
                return render_statement_student(request,False,"No Record Found on id",template)
            if student_result_email==True and student_result_mobile ==True:
                student_email=student_email
                student_mobile=student_mobile
            else:
                context_data["data"]=req_user
                return render_statement_student(request,False,"Either your email or mobile number is not correct",template)
            if req_user.username == role_number:
                if profile_picture!=None:
                    fs1=FileSystemStorage()
                    fs1.save(profile_picture.name, profile_picture)
                    update_user= User.objects.filter(id=req_user_id).update(name=name,email=student_email,mobile=student_mobile,gender=gender,date_of_birth=date_of_birth,profile_picture=profile_picture)
                else:
                    update_user= User.objects.filter(id=req_user_id).update(name=name,email=student_email,mobile=student_mobile,gender=gender,date_of_birth=date_of_birth)
                update_student=Student.objects.filter(id=id,object_status=0).update(roll_no=role_number,session_id=session,classs_id=classs,program_id=program,phase_id=phase,center_id=center,division_id=division,medium=medium,father_name=father_name,mother_name=mother_name)
                Student.objects.filter(id=id,object_status=0)
                StudentBatch.objects.filter(student_id=id).update(batch=Batch.objects.get(id=int(request.POST.get("current_batch"))))
                if len(father_email)!=0:
                    result_email = bool(regex_var_email.search(father_email))
                    if result_email==True:
                        Student.objects.filter(user_id=req_user.id).update(father_email=father_email)
                if len(mother_email)!=0:
                    result_email = bool(regex_var_email.search(mother_email))
                    if result_email==True:
                        Student.objects.filter(user_id=req_user.id).update(mother_email=mother_email)
                if len(father_mobile)!=0:
                    result_mobile=bool(regex_var_mobile.search(father_mobile))
                    if result_mobile==True:
                        Student.objects.filter(user_id=req_user.id).update(father_mobile=father_mobile)
                if len(mother_mobile)!=0:
                    result_mobile=bool(regex_var_mobile.search(mother_mobile))
                    if result_mobile==True:
                        Student.objects.filter(user_id=req_user.id).update(mother_mobile=mother_mobile)
                return render_statement_student(request,True,"Student Details Updated",template,model)
            else:
                return render_statement_student(request,False,"Student roll number cannot be updated",template,model)
        else:
            return render_statement_student(request,False,"Fields cannot be blank",template,model)
    else:

        return render_statement_student(request,False,"Please check your input",template,model)


class StudentFilter(django_filters.FilterSet):
    program_id = django_filters.ModelMultipleChoiceFilter(queryset=Program.objects.all())
    center_id = django_filters.ModelMultipleChoiceFilter(queryset=Center.objects.all())
    division_id = django_filters.ModelMultipleChoiceFilter(queryset=Division.objects.all())
    session_id = django_filters.ModelMultipleChoiceFilter(queryset=Sessions.objects.all())
    phase_id = django_filters.ModelMultipleChoiceFilter(queryset=Phase.objects.all())
    class Meta:
        model = Student
        fields = ['center_id', 'division_id', 'session_id', 'program_id', 'phase_id']

class StudentsViews(TemplateView):
    template_name = "users/students.html"

    @login_required_custom(login_url='/')

    def get(self, request, *args, **kwargs):

        req_all_obj = Student.objects.all().filter(status=True,object_status=0).order_by("-id")
        req_all_obj = StudentFilter(request.GET, queryset=req_all_obj)
        req_all_obj=paginator_maker(request,req_all_obj.qs)
        all_student_batch = StudentBatch.objects.all().values("batch__label").order_by("student_id")
        context_data["student_batch"] = all_student_batch
        context_data["data"]=req_all_obj

        # for student in req_all_obj:
            
        return render_statement_student(request,"","",self.template_name)

class AddStudentsViews(TemplateView):
    template_name = "users/add-student.html"

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return render_statement_student(request,"","",self.template_name)


    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_add_student(request,self.template_name)

class UpdateStudentViews(TemplateView):
    template_name = "users/student_update.html"

    @login_required_custom(login_url='/')
    def get(self, request, id, *args, **kwargs):
        try:
            req_fac_obj = Student.objects.get(id=id,status=True,object_status=0)
            context_data["profile_pic"]="/media/"+str(req_fac_obj.user.profile_picture)
        except:
            context_data["data"]=None
            return render_statement_student(request,False,"No Record Found",self.template_name,context_data)
        ee = StudentBatch.objects.get(student_id=id)
        context_data["batch_data"] = ee.batch.id
        # context_data["batch_data"] = ''
        # if len(ee) > 0:
        #    batch_id =  ee[0]['batch_id']
        #    current_batch = Batch.objects.filter(id=batch_id).values()
        #    context_data["batch_data"]=current_batch
        return get_for_updatestudent(request,self.template_name,req_fac_obj)
    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        req_all_obj = Student.objects.all().filter(status=True).order_by("-id")
        # context_data["data"]=req_all_obj
        return post_for_updatestudent(request,self.template_name)



def get_program_session_batch(request):
    session_filter = request.GET.get('session_id')
    session_filter = int(session_filter)
    session_program_id = SessionProgram.objects.filter(session_id=session_filter)
    all_program = {x.program.label:[x.program.id,x.program.label] for x in session_program_id}
    return JsonResponse({"sub_data":all_program}, safe=False)

def get_programsession_phase(request):
    session_filter = request.GET.get('session_id')
    session_filter = int(session_filter)
    Program_filter = request.GET.get('program_id')
    Program_filter=int(Program_filter)
    req_phase = Phase.objects.filter(session_program__program_id=Program_filter,session_program__session_id=session_filter)
    all_phase = {x.label:[x.id,x.label] for x in req_phase}
    return JsonResponse({"sub_data":all_phase}, safe=False)

def get_program_class(request):
    program_filter = request.GET.get('program_id')



    session_program_id = ProgramClass.objects.filter(program_id=program_filter).values('id','classs')
    sub_data =[subject_class for subject_class in session_program_id ]
    class_ob = []
    for clas in sub_data:
        class_data = Classs.objects.filter(id=clas['classs']).values('id','label')
        cl_data =[cl_class for cl_class in class_data ]
        for class_dt in cl_data:
            class_dat = {"class_id":class_dt['id'],"class_label":class_dt['label']}
            class_ob.append(class_dat)
    return JsonResponse({"sub_data":class_ob}, safe=False)



def get_reporting_manager_stcd(request):
    program_filter = request.GET.get('reporting_man')
    session_program_id = Faculty.objects.filter(user_id=program_filter).values('id','employee_code')
    sub_data =[subject_class for subject_class in session_program_id ]
    class_ob = []
    return JsonResponse({"sub_data":"class_ob"}, safe=False)



def get_phase_batch(request):
    program_filter = request.GET.get('phase_id')
    session_program_id = Batch.objects.filter(phase_id=program_filter).values('id','label')
    sub_data =[subject_class for subject_class in session_program_id ]

    return JsonResponse({"sub_data":sub_data}, safe=False)


class FacultyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        get_faculty = Faculty.objects.all()
        get_faculty = Faculty.objects.filter(user=request.user).first()
        faculty_profile_serializer_data = FacultyFacultySerializer(get_faculty,many=False)
        data = faculty_profile_serializer_data.data
        return render_response(data=data, error=[], status=1)
