from django.shortcuts import render, redirect
from django.views.generic import TemplateView , View

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from institute.models import Classs, Program, Target, Sessions, SessionProgram, Phase, Batch, CscDetails,Center, ProgramClass
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
# from users.views import paginator_maker
import django_filters
from django.core.paginator import Paginator
from content.models import Lecture, Assessment, DPPPlanner
from subject.models import Subject
from content.service import create_lectures,doc_to_html
from common.choices import QuestionCategoryChoices,ContentMappingLevelChoices
from rest_framework import viewsets
from . import serializers
from rest_framework.response import Response
from subject.models import MasterSubject,Subject,TOC
from rest_framework import status
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from django.views.generic.edit import UpdateView
from institute.forms import LectureForm
from users.models import User
from django.urls import reverse_lazy
from rest_framework.decorators import action
from django.http import HttpResponseRedirect
pagination_ob = settings.PAGINATION_SIZE
from django.db.models import Q
from common.views import login_required_custom,login_api_required
from django.contrib.auth.decorators import permission_required
from django.urls import reverse

class CscDetailsSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CscDetailsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = CscDetails
        fields = ["label","id","parent"]

class CenterSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CenterSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Center
        fields = ["name","id"]

class CscFinderApiView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        type= request.GET.get("type")
        parent = request.GET.get("parent")
        if type != None:
            type=type.strip()
            if len(type)!=0:
                try:
                    type=int(type)
                except:
                    return Response(data={"data":{},"error":"Please Provide Numeric Value","status":False}, status=status.HTTP_200_OK)
                if type in [1,2,3]:
                    if parent == None:
                            parent_obj = CscDetails.objects.filter(csc_type=type)
                            serializer_var = CscDetailsSerializer(parent_obj, many=True)
                            return Response(data={"data":serializer_var.data,"error":"","status":True}, status=status.HTTP_200_OK)
                    elif parent != None:
                        parent=parent.strip()
                        try:
                            parent=int(parent)
                        except:
                            return Response(data={"data":{},"error":"Please Provide Numeric Value","status":False}, status=status.HTTP_200_OK)
                        req_obj = CscDetails.objects.filter(csc_type=type,parent=parent)
                        serializer_var = CscDetailsSerializer(req_obj, many=True)
                        return Response(data={"data":serializer_var.data,"error":"","status":True}, status=status.HTTP_200_OK)

                else:
                    return Response(data={"data":{},"error":"No Record Found","status":False}, status=status.HTTP_200_OK)
            else:
                return Response(data={"data":{},"error":"No Record Found","status":False}, status=status.HTTP_200_OK)
        else:
            return Response(data={"data":{},"error":"No Record Found","status":False}, status=status.HTTP_200_OK)

class CenterFinderApiView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        parent = request.GET.get("parent")
        if parent == None:
                return Response(data={"data":{},"error":"Please Provide city","status":False}, status=status.HTTP_200_OK)
        elif parent != None:
            parent=parent.strip()
            try:
                parent=int(parent)
            except:
                return Response(data={"data":{},"error":"Please Provide Numeric Value","status":False}, status=status.HTTP_200_OK)
            req_obj = Center.objects.filter(city_id=parent,status=True)
            serializer_var = CenterSerializer(req_obj, many=True)
            return Response(data={"data":serializer_var.data,"error":"","status":True}, status=status.HTTP_200_OK)



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
    paginator = Paginator(model,pagination_ob)
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

def get_for_centers(request,model,template):
    context_data["status"]=""
    req_obj = model.objects.all().filter(object_status=0).order_by("-id")
    req_obj = paginator_maker(request,req_obj)
    context_data["data"]=req_obj
    return render(request, template, context_data)

def post_for_centers(request,model,template):
    req_obj_all = model.objects.all().filter(object_status=0).order_by("-id")
    req_obj_all = paginator_maker(request,req_obj_all)
    name= request.POST.get("name")
    country_id = request.POST.get("country_id")
    state_id = request.POST.get("state_id")
    city_id = request.POST.get("city_id")
    id=request.POST.get("id")
    action=request.POST.get("action")
    id=id.strip()
    if action==None:
        if len(id)==0:
            if name and country_id and state_id and city_id:
                name=name.strip()
                country_id=country_id.strip()
                state_id=state_id.strip()
                city_id=city_id.strip()
                if len(name)!=0 and len(country_id)!=0 and len(state_id)!=0 and len(city_id)!=0:
                    req_obj = model.objects.get_or_create(name=name,country_id=country_id,state_id=state_id,city_id=city_id,object_status=0,status=True)
                    if req_obj[1]==False:
                        return render_statement(request,False,"Record Already Exist",template,req_obj_all)
                    elif req_obj[1]==True:
                        return render_statement(request,True,"Successfuly created",template,req_obj_all)
                else:
                    return render_statement(request,False,"please provide your input",template,req_obj_all)
            else:
                return render_statement(request,False,"please provide your input",template,req_obj_all)
        else:
            id=id.strip()
            id=int(id)
            name = name.strip()
            country_id=country_id.strip()
            state_id=state_id.strip()
            city_id=city_id.strip()
            req_data = request.POST
            if len(name) != 0 and len(country_id) != 0 and len(state_id) and len(city_id)!= 0:
                try:
                    req_update_object = model.objects.get(id=id,name= name,country_id=country_id,state_id=state_id,city_id=city_id,object_status=0)
                    return render_statement(request,True,"Successfully Updated",template,req_obj_all) 
                except:
                    try:
                        req_update_object = model.objects.get(name= name,country_id=country_id,state_id=state_id,city_id=city_id,object_status=0)
                        return render_statement(request,False,"Record Already Exist",template,req_obj_all)
                    except:
                        updatable = ["name","country_id","state_id","city_id"]
                        try:
                            req_obj = model.objects.get(id=id,object_status=0)
                        except:
                            return render_statement(request,False,"no record found",template,req_obj_all)
                        for attr in updatable :
                            if attr in req_data :
                                setattr(req_obj,attr,req_data[attr])
                        req_obj.save()
                        return render_statement(request,True,"Successfuly updated",template,req_obj_all)
            else:
                return render_statement(request,False,"Please provide valid input",template,req_obj_all)
    else:
        if action=="delete":
            id = request.POST.get("id")
            if id!=None:
                id=id.strip()
                req_obj = model.objects.filter(id=id).update(object_status=1)
                return render_statement(request,"Deleted","Successfuly deleted",template,req_obj_all)

class CenterView(TemplateView):
    template_name = "institutes/centers.html"
    @login_required_custom(login_url='/')
    def get(self, request, id=None):
        return get_for_centers(request,Center,self.template_name)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_centers(request,Center,self.template_name)

class Testt():
    def __init__(self):
        return("hell")

    def common_message(self,condition,model_name):
        context_data={}
        if condition==False:

            context_data["status"] = False
            context_data["message"] = "record already exist"
            req_obj = Classs.objects.all().values()
        else:
            context_data["status"] = True
            context_data["message"] = "Updated Successfully exist"
            req_obj = model_name.objects.all().values()
            context_data["data"] = req_obj

class ClassViews(TemplateView):
    template_name = "institutes/class.html"

    def paginator_maker(request_args,model):
        page = request_args.GET.get("page")
        if page == None:
            page=1
        else:
            page=int(page)
        paginator = Paginator(model,2)
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

    @login_required_custom(login_url='/')
    def get(self, request, id=None):


        if id == None:
            template_name = self.template_name
        else:
            template_name = "institutes/edit_class.html"
        context_data = {}
        context_data["status"] = False
        req_count = Classs.objects.all().count()

        if req_count > 0:
            if id == None:
                req_obj = Classs.objects.all().values().order_by("-id")
            else:
                req_obj = Classs.objects.get(id=id)
            context_data["data"] = req_obj
        else:
            context_data["data"] ={}
        if req_count > 0:

            if id == None:
                paginator = Paginator(req_obj,pagination_ob)


                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))

                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                context_data['data']=users
                #context_data['pagination']=program_record
                program_numpages = program_numpages+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data = {}
            
        return render(request, template_name, context_data)

    @login_required_custom(login_url='/')
    def post(self,request):
        context_data = {}
        req_obj = Classs.objects.all().values().order_by("-id")
        context_data["data"] = req_obj
        if request.method == "POST":
            label = request.POST.get('title')
            description = request.POST.get('description')
            short_code = request.POST.get('short_code')
            order = request.POST.get('order')
            if label:
                label = label.strip()
                if len(label) != 0 and int(order) > 0:
                    if request.POST.get('hidden_id')=='':
                        class_label = Classs.objects.filter(Q(label=label) | Q(short_code=short_code)).count()
                        if class_label ==0:
                            class_view,class_post = Classs.objects.get_or_create(label=label,short_code=short_code,description=description,order=order)
                        else:
                            class_post =False
                        if class_post==False:
                            context_data["status"] = False
                            context_data["message"] = "Class name and Short Code Already Exist"
                            
                        else:
                            context_data["status"] = True
                            context_data["message"] = "Updated Successfully"
                          
                    else:
                        class_label = Classs.objects.filter(id=request.POST.get('hidden_id')).count()
                        if class_label != 0:
                            try:
                                if Classs.objects.filter(id=request.POST.get('hidden_id')).update(label=label,short_code=short_code,description=description,order=order) ==True:
                                    context_data["status"] = True
                                    context_data["message"] = "Updated Successfully"
                                else:
                                    context_data["status"] = False
                                    context_data["message"] = "Can Not be Update"
                            except:
                                context_data["status"] = False
                                context_data["message"] = "Class name and Short Code Already Exist"
                        else:
                            context_data["status"] = False
                            context_data["message"] = ""
                            req_obj = Classs.objects.all().values().order_by("-id")
                else:
                    context_data["status"] = False
                    context_data["message"] = "please provide your input"
            else:
                  if request.POST.get("action") =='delete':
                        try:
                            hiddenID = request.POST.get("delete")
                            Classs.objects.get(id=hiddenID).delete()
                            context_data["status"] = "Deleted"
                            context_data["message"] = "Deleted Successfully"
                            req_obj = Classs.objects.all().values().order_by("-id")
                            context_data["data"] = req_obj
                        except:
                            context_data["status"] = False
                            context_data["message"] = ""
        else:
            context_data["status"] = False
            context_data["message"] = "please provide your input"
        paginator = Paginator(req_obj,pagination_ob)
        if request.GET.get('page')==None:
            page =1
        else:
            page = int(request.GET.get('page'))
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        program_numpages = paginator.num_pages
        context_data['data']=users
        program_numpages = program_numpages+1
        context_data['PAGINATION_COUNT'] = range(1,program_numpages)
        context_data["data"] = users
        return render(request, self.template_name, context_data)

class ClassRemoveViews(TemplateView):
    def get(self, request, id=None):
        pass



class ProgramViews(TemplateView):
    template_name = "institutes/program.html"
    @login_required_custom(login_url='/')
    def get(self, request, id=None):
        context_data = {}
        if id == None:
            template_name = self.template_name
            req_obj = Program.objects.all().values().order_by("-id")
        else:
            template_name = "institutes/edit_program.html"
            session_program =  [class_objects for program_objects in ProgramClass.objects.filter(program_id=id).values() 
             for class_objects in Classs.objects.filter(id=program_objects['classs_id']).values('label','id')]
            req_obj = Program.objects.get(id=id)
            classs_pro = [xx for xx in Classs.objects.all().values('label','id')]
            session_pr = [program_ob for program_ob in session_program if program_ob in classs_pro]
            session_pr_error = [program_ob for program_ob in classs_pro if program_ob not in session_program]
            context_data['class_program'] = session_pr
            context_data['class_program_error'] = session_pr_error
        context_data["status"] = False
        req_count = Program.objects.all().count()
        target = Target.objects.all().values().order_by("-id")
        sessionId = ''       
        if ((request.GET.get('session_program') !=None ) and  (request.GET.get('program_name') ==None) or (request.GET.get('session_program') !=''  and  request.GET.get('program_name') =='')):         
            sessionId = "session"
            hh = [xx['program_id'] for xx in SessionProgram.objects.filter(session_id=request.GET.get('session_program')).values('program_id','session_id')]
        else:
            sessionId = ''
        if sessionId!='':
            req_obj = Program.objects.filter(id__in =hh).values()
            req_count = len(req_obj)
        else:
            req_obj = req_obj
        if req_count > 0:
            context_data["data"] = req_obj
            context_data['program_ob']=Program.objects.all()
        else:
            pass
        if req_count > 0:
            paginator = Paginator(req_obj,pagination_ob)
            if id == None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                program_record = {"program_numpage":program_numpages}
                context_data['data']=users
                program_numpages = program_numpages+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data['data'] = {}
        context_data['target'] = target
        context_data['classs'] = Classs.objects.all().order_by("-id")
        context_data['session']= Sessions.objects.all()
        context_data['session_program']=request.GET.get('session_program')
        context_data['program_name']=request.GET.get('program_name')
        return render(request, template_name, context_data)

    @login_required_custom(login_url='/')
    def post(self, request, id=None):
        context_data = {}
        req_obj = Program.objects.all().values().order_by("-id")
        context_data["data"] = req_obj
        context_data['classs'] = Classs.objects.all()
        if request.method == "POST":
            short_code = request.POST.get('Short_code')
            label = request.POST.get('name')
            if label:
                label = label.strip()
                if len(label) != 0:
                    target = request.POST.get('target')
                    description = request.POST.get('description')
                    if request.POST.get('hidden_id')=='':
                        try:
                            class_view,class_post = Program.objects.get_or_create(label=label,short_code=short_code,description=description,target=Target.objects.get(id=target))
                            try:
                                for class_ob in request.POST.getlist('class_name'):
                                    ProgramClass.objects.get_or_create(classs=Classs.objects.get(id=class_ob),program=Program.objects.get(id=class_view.id))
                            except:
                                pass
                        except:
                            class_post = False
                        if class_post==False:
                            context_data["status"] = False
                            context_data["message"] = "Program Name already exist"
                        else:
                            context_data["status"] = True
                            context_data["message"] = "Updated Successfully "
                            context_data["data"] = req_obj
                    else:
                        try:
                            if  Program.objects.filter(id=request.POST.get('hidden_id')).update(label=label,short_code=short_code,description=description,target=Target.objects.get(id=target)) ==True:
                                ProgramClass.objects.filter(program_id=request.POST.get('hidden_id')).delete()
                                try:
                                    for classs_id in request.POST.getlist('class_name'):
                                        ProgramClass.objects.get_or_create(program_id=request.POST.get('hidden_id'),classs_id=classs_id)
                                except:
                                    pass
                                context_data["status"] = True
                                context_data["message"] = "Program Name  Updated "
                            else:
                                context_data["status"] = False
                                context_data["message"] = "Program Can Not be Update"
                        except:
                            context_data["status"] = False
                            context_data["message"] = "Program name Already Exist"
                        context_data["data"] = req_obj
                else:
                    context_data["status"] = False
                    context_data["message"] = "please provide your input"
                    context_data["data"] = req_obj
            else:
                if request.POST.get("action") =='delete':
                        try:
                            hidden_obID = request.POST.get("delete")
                            vv = Program.objects.get(id=int(hidden_obID)).delete()
                            context_data["status"] = "Deleted"
                            context_data["message"] = "Deleted SuccessFully"
                        except:
                            context_data["status"] = ""
                            context_data["message"] = ""
        else:
             context_data["status"] = False
             context_data["message"] = "please provide your input"
        context_data["data"] = req_obj
        paginator = Paginator(req_obj,pagination_ob)
        if request.GET.get('page')==None:
            page =1
        else:
            page = int(request.GET.get('page'))
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        program_numpages = paginator.num_pages
        program_record = {"program_numpage":program_numpages}
        context_data['data']=users
        context_data['pagination']=program_record
        program_numpages = program_numpages+1
        context_data['PAGINATION_COUNT'] = range(1,program_numpages)
        context_data["data"] = users
        target = Target.objects.all().values()
        context_data['target'] = target
        context_data['session_status'] =False
        context_data['session']= Sessions.objects.all()
        return render(request, self.template_name, context_data)
        


class SessionViews(TemplateView):
    template_name = "institutes/session.html"
    @login_required_custom(login_url='/')
    def get(self, request, id=None):
        if id == None:
            template_name = self.template_name
        else:
            template_name = "institutes/session-phase.html"
        context_data = {}
        context_data["status"] = ''
        req_count = Sessions.objects.all().count()
        if req_count > 0:
            if id == None:
                req_obj = Sessions.objects.all().values().order_by("-id")
            else:
                req_obj = Sessions.objects.get(id=id)
                session_program =  [program_objects for session_program_obj in SessionProgram.objects.filter(session_id=id).values() for program_objects in Program.objects.filter(id=session_program_obj['program_id']).values('label','id')]
                programe = [xx for xx in Program.objects.all().values('label','id')]
                session_pr = [program_ob for program_ob in session_program if program_ob in programe]
                session_pr_error = [program_ob for program_ob in programe if program_ob not in session_program]
                context_data['session_program'] = session_pr
                context_data['session_program_error'] = session_pr_error
            context_data["data"] = req_obj
        else:
            context_data["data"] ={}
        if req_count > 0:
            if id == None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                    program_record = {"program_numpage":program_numpage}
                else:
                    program_record = {"program_numpage":program_numpages}
                context_data['data']=users
                context_data['pagination']=program_record
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data['data'] ={}
        context_data['Sessions'] = Sessions.objects.all().values()
        context_data["program"] = Program.objects.all().values('label','id')
        return render(request, template_name, context_data)


    @login_required_custom(login_url='/')
    def post(self,request,id=None):
        context_data = {}
        req_obj = Sessions.objects.all().values().order_by("-id")
        context_data["data"] = req_obj
        program = Program.objects.all().values()
        context_data["program"] = program
        if request.method == "POST":
            label = request.POST.get('name')
            short_code = request.POST.get('short_code')
            if label:
                label = label.strip()
                if len(label) != 0:
                    description = request.POST.get('description')
                    if request.POST.get('enddate') !='':
                        endi = request.POST.get('enddate').split("/")
                        end_date = endi[2]+"-"+endi[0]+"-"+endi[1]
                    else:
                        end_date = request.POST.get('enddate')
                    if request.POST.get('startdate') !='':
                        start = request.POST.get('startdate').split("/")
                        start_date = start[2]+"-"+start[0]+"-"+start[1]
                    else:
                        start_date = request.POST.get('startdate')
                    if request.POST.get('hidden_id')=='':
                        class_view = Sessions.objects.filter(label=label).count()
                        if class_view == 0:
                            try:
                                class_view,class_post = Sessions.objects.get_or_create(label=label,description=description,short_code=short_code,start_date=start_date,end_date=end_date)
                                try:
                                    for program in request.POST.getlist('program_name'):
                                        session_phase = SessionProgram.objects.get_or_create(session=class_view,program=Program.objects.get(id=program))
                                except:
                                    pass
                            except:
                                class_post = False
                        else:
                            class_post = False
                        if class_post==False:
                            context_data["status"] = False
                            context_data["message"] = "Session Name already exist"
                        else:
                            context_data["status"] = True
                            context_data["message"] = "Updated Successfully"
                    else:
                        session_label = Sessions.objects.filter(id=request.POST.get('hidden_id')).count()
                        if session_label > 0:
                            try:
                                if Sessions.objects.filter(id=request.POST.get('hidden_id')).update(label=label,short_code=short_code,description=description,start_date=start_date,end_date=end_date) ==True:
                                    SessionProgram.objects.filter(session_id=request.POST.get('hidden_id')).delete()
                                    for program in request.POST.getlist('program_name'):
                                        SessionProgram.objects.get_or_create(session_id=request.POST.get('hidden_id'),program_id=program)
                                    context_data["status"] = True
                                    context_data["message"] = "Updated Successfuly"
                                else:
                                    context_data["status"] = False
                                    context_data["message"] = "Updated Successfully exist"
                            except:
                                context_data["status"] = False
                                context_data["message"] = "Session name Already Exist"
                        else:
                            context_data["status"] = False
                            context_data["message"] = "Session name Already Exist"
                else:
                    context_data["status"] = False
                    context_data["message"] = "please provide your input"
            else:
                  if request.POST.get("action") =='delete':
                        try:
                            hiddenonId = request.POST.get("delete")
                            vv = Sessions.objects.get(id=int(hiddenonId)).delete()
                            context_data["status"] = "Deleted"
                            context_data["message"] = "Deleted SuccessFully"
                        except:
                            context_data["status"] = False
                            context_data["message"] = ""
        else:
            context_data["status"] = False
            context_data["message"] = "please provide your input"
            #req_obj = Sessions.objects.all.values().order_by("-id")

        context_data["data"] = req_obj
        program = Program.objects.all().values()
        paginator = Paginator(req_obj,pagination_ob)
        if request.GET.get('page')==None:
            page =1
        else:
            page = int(request.GET.get('page'))

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        program_numpages = paginator.num_pages
        if program_numpages > 0:
            program_numpage =  program_numpages
            program_record = {"program_numpage":program_numpages} 
        else:
            program_record = {"program_numpage":program_numpages}
        context_data['data']=req_obj
        context_data['pagination']=program_record
        program_numpages = program_numpage+1
        context_data['PAGINATION_COUNT'] = range(1,program_numpages)
        context_data["data"] = users
        context_data["program"] = program
        return render(request, self.template_name, context_data)



class PhaseViews(TemplateView,Testt):
    template_name = "institutes/program-phases.html"
    @login_required_custom(login_url='/')
    def get(self, request, id=None):
        if id == None:
            template_name = self.template_name
        else:
            template_name = "institutes/edit-program-phases.html"
        context_data = {}
        context_data["status"] = False
        req_count = Phase.objects.all().count()
        if req_count > 0:
            if id == None:
                req_obj = Phase.objects.all().values().order_by("-id")
            else:
                req_obj = Phase.objects.get(id=id)
            context_data["data"] = req_obj
        else:
            context_data["data"] ={}
        session_program = SessionProgram.objects.all().values()
        session_obj =[]
        session_objt ={}
        if req_count > 0:
            if id == None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                    program_record = {"program_numpage":program_numpages} 
                else:
                    program_record = {"program_numpage":program_numpages}

                context_data['data']=users
                context_data['pagination']=program_record
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data = {}
            context_data['session_program'] = session_program
        context_data['session_programe']= [{"program_objects":program_objects,"session_objects":session_objects,"session_program_obj":session_program_obj['id']} for session_program_obj in SessionProgram.objects.all().values() for program_objects in Program.objects.filter(id=session_program_obj['program_id']).values('label') for session_objects in Sessions.objects.filter(id=session_program_obj['session_id']).values('label')]
        return render(request, template_name, context_data)
    @login_required_custom(login_url='/')
    def post(self,request,id=None):
        context_data = {}
        req_obj = Phase.objects.all().values().order_by("-id")
        req_count = Phase.objects.all().count()
        context_data["data"] = req_obj
        if request.method == "POST":
            label = request.POST.get('title')
            short_code = request.POST.get('short_code')
            startdate = request.POST.get('startdate')
            if label:
                label = label.strip()
                if len(label) != 0:
                    description = request.POST.get('description')
                    session_program = request.POST.get('program')
                    import datetime
                    if request.POST.get('startdate') !='':
                        try:
                            start_dates = datetime.datetime.strptime(request.POST.get('startdate'), "%m/%d/%Y").strftime("%Y-%m-%d")
                        except:
                            start = request.POST.get('startdate').split("/")
                            start_dt = start[2]
                            st_years = start_dt.split(" ")
                            start_phase = st_years[0]
                            start_dates = start_phase+"-"+start[0]+"-"+start[1]
                        start_date = start_dates
                    else:
                        start_date = request.POST.get('startdate')
                    if request.POST.get('enddate') !='':
                        try:
                            end_dates = datetime.datetime.strptime(request.POST.get('enddate'), "%m/%d/%Y").strftime("%Y-%m-%d")
                        except:
                            endi = request.POST.get('enddate').split("/")
                            end_dt = endi[2]
                            years = end_dt.split(" ")
                            year_phase = years[0]
                            end_dates = year_phase+"-"+endi[0]+"-"+endi[1]
                        end_date = end_dates
                    else:
                        end_date = request.POST.get('enddate')
                    if request.POST.get('hidden_id')=='':
                        class_view = Phase.objects.filter(label=label).count()
                        try:
                            class_view,class_post = Phase.objects.get_or_create(label=label,short_code=short_code,description=description,session_program=SessionProgram.objects.get(id=session_program),start_date=start_date,end_date=end_date)
                        except:
                            class_post = False
                        if class_post==False:
                            context_data["status"] = False
                            context_data["message"] = "Phase or Short Code Name already exist"
                            req_obj = Phase.objects.all().values().order_by("-id")
                        else:
                            context_data["status"] = True
                            context_data["message"] = "Updated Successfully "
                            req_obj = Phase.objects.all().values().order_by("-id")
                            context_data["data"] = req_obj
                            req_count = Phase.objects.all().count()
                    else:
                        phase_label = Phase.objects.filter(id=request.POST.get('hidden_id')).count()
                        if phase_label > 0:
                            try:
                                if Phase.objects.filter(id=request.POST.get('hidden_id')).update(label=label,short_code=short_code,description=description,session_program=SessionProgram.objects.get(id=session_program),start_date=start_date,end_date=end_date) ==True:
                                    context_data["status"] = True
                                    context_data["message"] = "Updated SuccessFully"
                                else:
                                    context_data["status"] = False
                            except:
                                context_data["status"] = False
                                context_data["message"] = "Phase name Already Exist"
                        else:
                            context_data["status"] = False
                            context_data["message"] = ""
                else:
                    context_data["status"] = False
                    context_data["message"] = "please provide your input"      
                context_data["data"] = req_obj
            else:
                  if request.POST.get("action") =='delete':
                        try:
                            phase_id = request.POST.get("delete")
                            Phase.objects.get(id=phase_id).delete()
                            context_data["status"] = "Deleted"
                            context_data["message"] = "Deleted SuccessFully"
                        except:
                            context_data["status"] = False
                            context_data["message"] = ""
        else:
            context_data["status"] = False
            context_data["message"] = "please provide your input"
        session_program = SessionProgram.objects.all().values()
        session_obj =[]
        context_data["session_program"]  = session_program
        if req_count > 0:
            if id == None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                    program_record = {"program_numpage":program_numpages} 
                else:
                    program_record = {"program_numpage":program_numpages}
                context_data['data']=users
                context_data['pagination']=program_record
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data = {}
        context_data['session_programe']= [{"program_objects":program_objects,"session_objects":session_objects,"session_program_obj":session_program_obj['id']} for session_program_obj in SessionProgram.objects.all().values() for program_objects in Program.objects.filter(id=session_program_obj['program_id']).values('label') for session_objects in Sessions.objects.filter(id=session_program_obj['session_id']).values('label')]
        return render(request, self.template_name, context_data)


################################batches###########################

class BatchViews(TemplateView,Testt):
    template_name = "institutes/program-batches.html"
    @login_required_custom(login_url='/')
    def get(self, request, id=None):
        if id == None:
            template_name = self.template_name
        else:
            template_name = "institutes/edit-program-batches.html"
        context_data = {}
        context_data["status"] = ''
        req_count = Batch.objects.all().count()
        if req_count > 0:
            if id == None:
                req_obj = Batch.objects.all().values().order_by("-id")
            else:
                req_obj = Batch.objects.get(id=id)
            context_data["data"] = req_obj
        else:
            context_data["data"] ={}
        phase = Phase.objects.all().values()
        if req_count > 0:
            if id == None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                else:
                    program_record = {"program_numpage":program_numpage}
                context_data['data']=users
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data = {}
        context_data["phase"]  = phase
        return render(request, template_name, context_data)

    @login_required_custom(login_url='/')
    def post(self,request,id=None):
        context_data = {}
        req_obj = Batch.objects.all().values().order_by("-id")
        if request.method == "POST":
            label = request.POST.get('title')
            short_code = request.POST.get('short_code')
            startdate = request.POST.get('startdate')
            times_slot = request.POST.get('time')
            if label:
                label = label.strip()
                if len(label) != 0:
                    description = request.POST.get('description')
                    phase_ob = request.POST.get('programs')
                    if request.POST.get('hidden_id')=='':
                        class_view = Batch.objects.filter(label=label).count()
                        try:
                            class_view,class_post = Batch.objects.get_or_create(label=label,short_code=short_code,description=description,phase=Phase.objects.get(id=phase_ob),times_slot=times_slot)
                        except:
                            class_post = False
                        if class_post==False:
                            context_data["status"] = False
                            context_data["message"] = "Batches Name Already Exist "
                        else:
                            context_data["status"] = True
                            context_data["message"] = "Batches Updated Successfully "
                            
                    else:
                        try:
                            if Batch.objects.filter(id=request.POST.get('hidden_id')).update(label=label,short_code=short_code,description=description,phase=Phase.objects.get(id=phase_ob),times_slot=times_slot) ==True:
                                context_data["status"] = True
                                context_data["message"] = "Updated Successfully"
                            else:
                                context_data["status"] = False
                                context_data["message"] = "Not Updated"
                        except:
                            context_data["status"] = False
                            context_data["message"] = "Batches name Already Exist"
                else:
                    context_data["status"] = False
                    context_data["message"] = "please provide your input"
            else:
                  if request.POST.get("action") =='delete':
                        try:
                            hidden_id = request.POST.get("delete")
                            Batch.objects.get(id=hidden_id).delete()
                            context_data["status"] = "Deleted"
                            context_data["message"] = "Deleted SuccessFully"
                        except:
                            context_data["status"] = ""
                            context_data["message"] = ""
        else:
            context_data["status"] = False
            context_data["message"] = "please provide your input"
        req_count =  Batch.objects.all().count()
        phase = Phase.objects.all().values().order_by("-id")
        if req_count > 0:
            if id == None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                else:
                    program_record = {"program_numpage":program_numpage}
                context_data['data']=users
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data = {}
        context_data["phase"]  = phase
        return render(request, self.template_name, context_data)



class Program_Class_subjectViews(TemplateView):
    template_name = "institutes/program_class_subject.html"
    @login_required_custom(login_url='/')
    def get(self,request,id=None):
        context_data = {}
        if id == None:
            template_name = self.template_name
            context_data["hid"] = id
        else:
            template_name = "institutes/program_class_subject.html"
            context_data["hid"] = int(id)
        context_data["status"] = True
        context_data["id"] = id
        
       
        req_count = ProgramClass.objects.all().count()
        target = ProgramClass.objects.all().values()
        subject_class = []
        if req_count > 0:
            req_objj = ProgramClass.objects.filter(program_id=id).values()
            for xx in req_objj:
                program_id = xx['program_id']
                class_id = xx ['classs_id']
                program_ob = {"Program_name":Program.objects.filter(id=program_id).values('label'),"class_name":Classs.objects.filter(id=class_id).values('label'),"Subject_name":Subject.objects.filter(classs=Classs.objects.get(id=class_id)).values('label')}
                subject_class.append(program_ob)
            req_obj = subject_class
            context_data["data"] = req_obj
        else:
            pass
        if req_count > 0:
            paginator = Paginator(req_obj,pagination_ob)
            if id != None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                    program_next = users.has_next()
                    program_previous = users.has_previous()
                    program_user_changes = users.has_other_pages()
                    if program_next == True:
                        program_next_page_number = users.next_page_number()
                        program_numpages
                    if page >1:
                        current_page = users.number
                    else:
                        current_page = 1
                    program_index = users.start_index()
                    program_end = users.end_index()
                    if program_next != True:
                        program_record ={"program_numpage":program_numpages,"program_next":program_next,"program_previous":program_previous,"program_user_changes":program_user_changes,"program_index":program_index,"program_end":program_end,"current_page":current_page,"paginator.page_range":paginator.page_range}
                    else:
                        program_next_page_number = users.next_page_number()
                        program_record = {"program_numpage":program_numpages,"program_next":program_next,"program_previous":program_previous,"program_user_changes":program_user_changes,"program_index":program_index,"program_end":program_end,"current_page":current_page,"program_next_page_number":program_next_page_number,"paginator.page_range":paginator.page_range}
                else:
                    program_record = {"program_numpage":program_numpage}
                context_data['data']=users
                context_data['pagination']=program_record
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data['data'] = {}
        context_data['program'] = Program.objects.all().values()
        if (request.GET.get('subject') == None) or (request.GET.get('subject')=='') or  (request.GET.get('subject') == 'True'):
            context_data['subject'] = True
        else:
            context_data['subject'] = False
        return render(request, template_name, context_data)




class TargetViews(TemplateView):
    template_name = "institutes/target.html"

    @login_required_custom(login_url='/')
    def get(self, request, id=None):
        context_data = {}
        if id == None:
            template_name = self.template_name
        else:
            template_name = "institutes/edit_target.html"
        context_data["status"] = ''
        req_count = Target.objects.all().count()
        target = Target.objects.all().values()
        if req_count > 0:
            if id == None:
                req_obj = Target.objects.all().values()
            else:
                req_obj = Target.objects.get(id=id)
            context_data["data"] = req_obj
        else:
            pass
        if req_count > 0:
            paginator = Paginator(req_obj,pagination_ob)
            if id == None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                    program_record = {"program_numpage":program_numpage}
                else:
                    program_record = {"program_numpage":program_numpage}
                context_data['data']=users
                context_data['pagination']=program_record
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
        else:
            context_data['data'] = {}
        return render(request, template_name, context_data)

    @login_required_custom(login_url='/')
    def post(self, request, id=None):
        context_data = {}

        req_obj = Target.objects.all().values().order_by("-id")
        context_data["data"] = req_obj
        if request.method == "POST":
            label = request.POST.get('name')
            short_code = request.POST.get('short_code')
            if label:
                label = label.strip()
                if len(label) != 0:
                    if request.POST.get('hidden_id')=='':
                        try:

                            class_view,class_post = Target.objects.get_or_create(label=label,short_code=short_code)
                        except:
                            class_post = False

                        if class_post==False:
                            context_data["status"] = False
                            context_data["message"] = "Target  already exist"
                        else:
                            context_data["status"] = True
                            context_data["message"] = "Target Updated Successfully"
                    else:
                        try:
                            if  Target.objects.filter(id=request.POST.get('hidden_id')).update(label=label,short_code=short_code) ==True:
                                context_data["status"] = True
                                context_data["message"] = "Target Updated Successfully"
                            else:
                                context_data["status"] = False
                                context_data["message"] = "Can Not be Update"
                        except:
                            context_data["status"] = False
                            context_data["message"] = "target Already Exist"
                        context_data["data"] = req_obj
                else:
                    context_data["status"] = False
                    context_data["message"] = "please provide your input"
            else:
                if request.POST.get("action") =='delete':
                        try:
                            delete_id = request.POST.get("delete")
                            vv = Target.objects.filter(id=delete_id).hard_delete()
                            context_data["status"] = "Deleted"
                            context_data["message"] = "Deleted SuccessFully"
                        except:
                            context_data["status"] = ''
                            context_data["message"] = ""
        else:
             context_data["status"] = False
             context_data["message"] = "please provide your input"
             context_data["data"] = req_obj
        paginator = Paginator(req_obj,pagination_ob)
        if request.GET.get('page')==None:
            page =1
        else:
            page = int(request.GET.get('page'))
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        program_numpages = paginator.num_pages
        if program_numpages > 0:
            program_numpage =  program_numpages
            program_record = {"program_numpage":program_numpage}
        else:
            program_record = {"program_numpage":program_numpage}
        context_data['data']=users
        context_data['pagination']=program_record
        program_numpages = program_numpage+1
        context_data['PAGINATION_COUNT'] = range(1,program_numpages)
        context_data["data"] = users
        return render(request, self.template_name, context_data)

from subject.models import TOC
from content.serializers import TocSerializer
from content.models import LectureTOCMapping

@login_api_required(login_url='/')
def get_toc_by_subject_id(request):
    subject_id = request.POST.get('subject_id')
    tocs = TOC.objects.filter(subject_id=subject_id).order_by('id')
    tocs = TocSerializer(tocs, many=True)
    return JsonResponse(tocs.data, safe=False)

@login_api_required(login_url='/')
def get_dpp_by_subject_id(request):
    subject_id = request.POST.get('subject_id')
    assessments = Assessment.objects.filter(dppplanner__subject_id=subject_id).order_by('id')
    assessments = [{'id':assessment.id, 'title':assessment.title} for assessment in assessments]
    return JsonResponse(assessments, safe=False)

@login_api_required(login_url='/')
def update_dpp_release_status(request):
    dpp_id = request.POST.get('dpp_id')
    dpp=DPPPlanner.objects.get(id=dpp_id)
    dpp.is_released=True
    dpp.save()
    return JsonResponse({'status':'success'})

@login_api_required(login_url='/')
def create_lecture_toc_mapping(request):
    lecture_id = request.POST.get('lecture_id')
    toc_ids = request.POST.getlist('toc_ids[]')
    LectureTOCMapping.objects.filter(lecture_id=lecture_id).delete()
    for id in toc_ids:
        content_toc = ContentTOCMapping.objects.filter(ref_id=id).first()
        if content_toc:
            content_toc = content_toc
            LectureTOCContent.objects.get_or_create(content_toc=content_toc, lecture_id=lecture_id)
        toc = TOC.objects.get(id=id)
        LectureTOCMapping.objects.create(lecture_id=lecture_id, toc_id=id, level=toc.level)
    return JsonResponse({'status':'success'})

class DPPFilter(django_filters.FilterSet):
    classs = django_filters.NumberFilter(field_name='classs')
    subject = django_filters.NumberFilter(field_name='subject')
    session = django_filters.NumberFilter(field_name='session')
    program = django_filters.NumberFilter(field_name='program')
    phase = django_filters.NumberFilter(field_name='phase')
    batch = django_filters.NumberFilter(field_name='batch')
    class Meta:
        model = DPPPlanner
        fields = ['classs', 'subject', 'session', 'program', 'phase', 'batch']

class DppView(TemplateView):
    template_name = "institutes/dpp.html"


    def get_context_data(self):
        ctx = super(DppView, self).get_context_data()
        ctx['classes'] = Classs.objects.all()
        ctx['subjects'] = Subject.objects.all()
        ctx['sessions'] = Sessions.objects.all()
        ctx['programmes'] = Program.objects.all()
        ctx['phases'] = Phase.objects.all()
        ctx['batches'] = Batch.objects.all()
        ctx['dpps'] = Assessment.objects.filter(type=QuestionCategoryChoices.DAILY_PRACTICE_PROBLEMS)
        return ctx

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        filtered_dpps = DPPFilter(request.GET, queryset=DPPPlanner.objects.all())
        ctx['dpps'] = filtered_dpps.qs.distinct()
        if request.GET:
            assessments = Assessment.objects.filter(type=QuestionCategoryChoices.DAILY_PRACTICE_PROBLEMS, dppplanner__isnull=True)
            ctx['unplanned_count'] = assessments.count()
            ctx['selected_batches'] = request.GET.getlist('batch')

        for dpp in ctx['dpps']:
            dpp.released_button = True if dpp.assessment.content and dpp.assessment.content.faculty_releasable and not dpp.is_released \
                else False
        return render(request, self.template_name, ctx)

class DppEditView(UpdateView):
    model = DPPPlanner
    template_name = "institutes/edit-dpp.html"
    fields = ['start_date', 'end_date', 'faculty', 'is_tentative']
    success_url = reverse_lazy('DppView')

    def get_context_data(self, **kwargs):
        ctx = super(DppEditView, self).get_context_data(**kwargs)
        ctx['faculties'] = User.objects.filter(role=3)
        ctx['object'] = self.object
        ctx['redirect'] = self.request.POST.get('redirect') or self.request.META.get('HTTP_REFERER')
        return ctx

    def form_valid(self, form):
        super().form_valid(form)
        if 'redirect' in self.request.POST:
            return HttpResponseRedirect(self.request.POST.get('redirect'))
        return HttpResponseRedirect(self.success_url)

class LectureFilter(django_filters.FilterSet):
    class Meta:
        model = Lecture
        fields = ['classs', 'subject', 'session', 'program', 'phase']

class LecturePlannerView(TemplateView):
    template_name = "institutes/lecture-planner.html"
    def get_context_data(self):
        ctx = super(LecturePlannerView, self).get_context_data()
        ctx['classes'] = Classs.objects.all()
        ctx['subjects'] = Subject.objects.all()
        ctx['sessions'] = Sessions.objects.all()
        ctx['programs'] = Program.objects.all()
        ctx['phases'] = Phase.objects.all()
        ctx['batches'] = Batch.objects.all()
        return ctx

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        lecture_filter = LectureFilter(request.GET, queryset=Lecture.objects.all())
        ctx['lectures'] = lecture_filter.qs
        # selected_filters = {}
        total_lectures = lecture_filter.qs
        if 'batch' in request.GET:
            total_lectures = total_lectures.filter(batch_id__in=request.GET.getlist('batch'))
        paginator = Paginator(total_lectures, pagination_ob)
        page_number = request.GET.get('page')
        try:
            ctx['lectures'] = paginator.page(page_number)
        except PageNotAnInteger:
            ctx['lectures'] = paginator.page(1)
        except EmptyPage:
            ctx['lectures'] = paginator.page(paginator.num_pages)
        if request.GET:
            ctx['selected_batches'] = request.GET.getlist('batch')
        for lecture in ctx['lectures']:
            lecture.toc_count = lecture.lecturetocmapping_set.count()
        if 'phase' in request.GET:
            ctx['phase'] = Phase.objects.get(id=request.GET['phase'])
        return render(request, self.template_name, ctx)



from django.http import JsonResponse
def corresponding_objects(request):
    objs = []
    field_name = request.GET.get('field_name')

    if field_name == 'classs':
        field_value=request.GET.get('field_value')
        subjects = Subject.objects.filter(classs__id=field_value)
        for phase in subjects:
            objs.append({'id':phase.id, 'value':phase.label})
        return JsonResponse(objs, safe=False)

    if field_name == 'program':
        field_value=request.GET.get('field_value')
        phases = Phase.objects.filter(session_program__program__id=field_value)
        for phase in phases:
            objs.append({'id':phase.id, 'value':phase.label})
        return JsonResponse(objs, safe=False)

    if field_name == 'session':
        field_value=request.GET.get('field_value')
        programs = Program.objects.filter(sessionprogram__session__id=field_value)
        for phase in programs:
            objs.append({'id':phase.id, 'value':phase.label})
        return JsonResponse(objs, safe=False)

    if field_name == 'phase':
        field_value=request.GET.get('field_value')
        batches = Batch.objects.filter(phase_id=field_value)
        for phase in batches:
            objs.append({'id':phase.id, 'value':phase.label})
        return JsonResponse(objs, safe=False)

from content.service import create_lectures

#@login_required_custom(login_url='/')
@login_api_required(login_url='/')
def create_lecture(request):
    try:
        create_lectures(**request.POST)
    except Exception as e:
        print(e, "errors")
        pass
    return JsonResponse({'status':'success'})

@login_api_required(login_url='/')
def delete_lecture(request):
    lecture_id = request.POST.get('lecture_id')
    Lecture.objects.filter(id=lecture_id).delete()
    return JsonResponse({'success':True})


class EditLecturePlanner(UpdateView):
    template_name='institutes/edit-lecture-planner.html'
    model = Lecture
    fields = ['title', 'duration_hrs', 'faculty', 'room', 'start_date_time','is_tentative']
    success_url = reverse_lazy('LecturePlannerView')

    def get_context_data(self, **kwargs):
        ctx = super(EditLecturePlanner, self).get_context_data(**kwargs)
        ctx['faculties'] = User.objects.filter(role=3)
        ctx['object'] = self.object
        ctx['redirect'] = self.request.POST.get('redirect') or self.request.META.get('HTTP_REFERER')
        return ctx

    def form_valid(self, form):
        super().form_valid(form)
        if 'redirect' in self.request.POST:
            return HttpResponseRedirect(self.request.POST.get('redirect'))
        return HttpResponseRedirect(self.success_url)


class TocViews(TemplateView):
    template_name = "html/index.html"

    def get(self, request, id=None):
        if id == None:
            template_name = self.template_name
        context_data = {}
        context_data["status"] = True
        return render(request, self.template_name, context_data)


class TocUnitModelViewSet(TemplateView):

    def post(self,request,*args, **kwargs):
        HttpResponse("hello")
def CreatedLectureTocIds(request):
    lecture = Lecture.objects.get(id=request.POST.get('lecture_id'))
    toc_ids = list(lecture.lecturetocmapping_set.values_list('toc_id', flat=True))
    return JsonResponse({'toc_ids':toc_ids})

class StudyMaterialView(TemplateView):
    template_name = "institutes/study-material.html"

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['subjects'] = Subject.objects.all()
        ctx['classes'] = Classs.objects.all()
        return ctx


class ContentView(TemplateView):
    template_name = "institutes/content.html"
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        ctx = super().get_context_data()
        ctx['subjects'] = Subject.objects.all()
        ctx['classes'] = Classs.objects.all()
        request = self.request
        if request.GET.get('subject') and request.GET.get('class'):
            ctx['toc'] = get_subject_class_toc(request.GET.get('subject'),request.GET.get('class'))
        return render(request, self.template_name, ctx)
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['subjects'] = Subject.objects.all()
        ctx['classes'] = Classs.objects.all()
        request = self.request
        if request.GET.get('subject') and request.GET.get('class'):
            ctx['toc'] = get_subject_class_toc(request.GET.get('subject'),request.GET.get('class'))
        return ctx


class ContentSMListView(TemplateView):
    template_name = "institutes/content_sm_list.html"
    def get_context_data(self):
        ctx = super().get_context_data()
        toc_id=self.request.GET.get('toc_id')
        t=TOC.objects.get(pk=toc_id)
        content_ids=ContentTOCMapping.objects.filter(ref_id=t.id,level=ContentMappingLevelChoices.get_by_toc_level(t.level)).values_list('content_id')
        ctx['materials'] = StudyMaterial.objects.filter(content_id__in=content_ids)
        return ctx

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        request = self.request
        if request.GET.get('toc_id') and request.GET.get('studymaterial_id'):
            sm = StudyMaterial.objects.get(pk=request.GET.get('studymaterial_id'))
            toc_id=request.GET.get('toc_id')
            toc=TOC.objects.get(pk=toc_id)
            ContentTOCMapping.objects.get_or_create(content=sm.content,ref_id=toc_id,level=ContentMappingLevelChoices.get_by_toc_level(toc.level))
            return redirect(reverse('content') + "?class={}&subject={}&success=true".format(toc.subject.classs_id,toc.subject_id))
        return super().get(request,args,kwargs)

class ContentSMCreateView(TemplateView):
    template_name = "institutes/content_sm_create.html"
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        ctx = super().get_context_data()
        ctx['subjects'] = Subject.objects.all()
        ctx['classes'] = Classs.objects.all()
        request = self.request
        if request.GET.get('toc_id'):
            ctx['toc_id'] = request.GET.get('toc_id')
        if request.POST.get('toc_id'):
            ctx['toc_id'] = request.POST.get('toc_id')
        request = self.request
        if request.GET.get('subject') and request.GET.get('class'):
            ctx['toc'] = get_subject_class_toc(request.GET.get('subject'),request.GET.get('class'))
        return render(request, self.template_name, ctx)


    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['subjects'] = Subject.objects.all()
        ctx['classes'] = Classs.objects.all()
        request = self.request
        if request.GET.get('toc_id'):
            ctx['toc_id'] = request.GET.get('toc_id')
        if request.POST.get('toc_id'):
            ctx['toc_id'] = request.POST.get('toc_id')
        request = self.request
        if request.GET.get('subject') and request.GET.get('class'):
            ctx['toc'] = get_subject_class_toc(request.GET.get('subject'),request.GET.get('class'))
        return ctx

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        type=request.POST.get('type')
        title=request.POST.get('title')
        content_txt = request.POST.get('content')
        duration = request.POST.get('duration')
        language_id = request.POST.get('language_id')
        faculty_only = request.POST.get('faculty_only')
        faculty_releasable = request.POST.get('faculty_releasable')
        print(faculty_releasable,"faculty_releasable")
        if faculty_releasable == 'on':
           faculty_releasable = True
        else:
           faculty_releasable = False
        file = request.FILES['file'] if request.FILES else ''
        content_subtype = 4 if type == '0' else 5 #4 for notes, 5 for video
        content = Content.objects.create(title=title,content_type=ContentTypeChoices.STUDY_MATERIAL,content_subtype=content_subtype,faculty_releasable=faculty_releasable)
        sm=StudyMaterial.objects.create(content=content,duration_mins=duration,title=title,faculty_only=faculty_only,type=type)
        smf=StudyMaterialFile.objects.create(study_material=sm,file=file,content=content_txt,language_id=language_id)
        params = '?success=true'
        toc_id=request.POST.get('toc_id',False)
        if toc_id:
            converted_html=doc_to_html(smf.file.path,content.id,toc_id)
            toc=TOC.objects.get(pk=toc_id)
            params = "?class={}&subject={}&success=true".format(toc.subject_id,toc.subject.classs_id)
        params += '&modified_id=' + str(sm.content.id)
        ContentTOCMapping.objects.get_or_create(content=sm.content,ref_id=toc_id,level=ContentMappingLevelChoices.get_by_toc_level(toc.level))
        return redirect(reverse('content') + params)

class ContentSMEditView(TemplateView):
    template_name = "institutes/content_sm_create.html"

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('id')
        ctx = super().get_context_data()
        sm = StudyMaterial.objects.get(pk=id)
        language_id = self.request.GET.get('language_id',1)
        ctx['language_id'] = language_id
        ctx['sm'] = sm
        request = self.request
        if request.GET.get('toc_id'):
            ctx['toc_id'] = request.GET.get('toc_id')
        if request.POST.get('toc_id'):
            ctx['toc_id'] = request.POST.get('toc_id')
        files = StudyMaterialFile.objects.filter(study_material = sm,language_id=language_id)
        if files.exists():
            ctx['smf'] = files.first()
        return render(request, self.template_name, ctx)


    def get_context_data(self):
        id=self.kwargs.get('id')
        ctx = super().get_context_data()
        sm = StudyMaterial.objects.get(pk=id)
        language_id = self.request.GET.get('language_id',1)
        ctx['language_id'] = language_id
        ctx['sm'] = sm
        request = self.request
        if request.GET.get('toc_id'):
            ctx['toc_id'] = request.GET.get('toc_id')
        if request.POST.get('toc_id'):
            ctx['toc_id'] = request.POST.get('toc_id')
        files = StudyMaterialFile.objects.filter(study_material = sm,language_id=language_id)
        if files.exists():
            ctx['smf'] = files.first()
        return ctx

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('id')
        if request.GET.get('delete'):
            sm=StudyMaterial.objects.get(pk=id)
            sm.content.delete()
            sm.delete()
            return redirect(reverse('content') + "?success=true")
        return super().get(request,args,kwargs)


    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        id=self.kwargs.get('id')
        title=request.POST.get('title')
        content = request.POST.get('content')
        duration = request.POST.get('duration')
        language_id = request.POST.get('language_id')
        file = request.FILES['file']
        sm=StudyMaterial.objects.get(pk=id)
        sm.title= title
        sm.duration_mins = duration
        sm.save()
        smf,created=StudyMaterialFile.objects.get_or_create(study_material=sm,language_id=language_id)
        smf.content = content
        smf.language_id = language_id
        smf.file = file
        smf.save()
        params = '?success=true'
        toc_id=request.POST.get('toc_id',False)
        if toc_id:
            toc=TOC.objects.get(pk=toc_id)
            params = "?class={}&subject={}&success=true".format(toc.subject_id,toc.subject.classs_id)

        params += '&modified_id=' + str(sm.id)
        return redirect(reverse('content') + params)

class ContentSMPreviewView(TemplateView):
    template_name = "institutes/sm_preview.html"
    def get(self,request,sm_id,*args,**kwargs):
        toc_id = request.GET.get("toc_id")
        data={}
        sm=StudyMaterial.objects.get(id=sm_id)
        smf_language = StudyMaterialFile.objects.get(study_material_id=sm_id).language.name
        content = sm.content
        context_data={}
        context_data["link"]="/institute/content/sm/edit/{0}/?toc_id={1}".format(sm_id,toc_id)
        context_data["sm"]=sm
        context_data["content"]=content
        context_data["type"]=sm.get_type_display()
        context_data["smf_language"]=smf_language
        context_data["converted_link"]="http://3.7.9.110:8000/api/v1/student_content?content_id={0}&toc_id={1}&template=yes".format(sm.content.id,toc_id)
        return render(request,self.template_name,context_data)


def get_subject_class_toc(subject_id,classs_id):
    tocs = TOC.objects.filter(subject_id=subject_id, subject__classs__id=classs_id).distinct()
    tocs_serialized = TocSerializer(tocs, many=True)

    contents = ContentTOCMapping.objects.filter(ref_id__in=tocs).exclude(level__in=[ContentMappingLevelChoices.CHAPTER,ContentMappingLevelChoices.SUBJECT])
    lst=[]
    for c in contents:
        o={}
        o['id'] = c.content_id
        o['level'] = c.level
        sm=StudyMaterial.objects.filter(content=c.content)
        at=Assessment.objects.filter(content=c.content)
        if sm.exists():
            sm = sm.first()
            languages = ','.join(sm.files.values_list('language__name',flat=True))
            label = c.content.get_content_subtype_display() + ": {} ({})".format( c.content.title,languages)
            if sm.faculty_only:
                label += "(Faculty Only)"
            o['label'] = label
            o['content_type'] = c.content.content_type
            o['parent_id'] = c.ref_id
            o['link'] = reverse('content_sm_edit',kwargs={'id':sm.id})
            o["preview_link"]=reverse('content_sm_preview',kwargs={'sm_id':sm.id})
            lst.append(o)
        elif at.exists():
            at = at.first()
            label = c.content.get_content_subtype_display() + ": {}".format(c.content.title)
            o['label'] = label
            o['content_type'] = c.content.content_type
            o['parent_id'] = c.ref_id
            o['preview_link'] = reverse('AssessmentSectionQuestionTemplateView',kwargs={'id':at.id})
            lst.append(o)
    return tocs_serialized.data+lst

@login_api_required(login_url='/')
def get_toc_by_subject_and_class(request,*args, **kwargs):
    subject_id = request.POST.get('subject_id')
    classs_id = request.POST.get('classs_id')
    data = get_subject_class_toc(subject_id,classs_id)
    return JsonResponse(data, safe=False)

from common.choices import QuestionCategoryChoices, ContentTypeChoices, ContentSubtypeChoices
from content.models import Content, StudyMaterial, ContentTOCMapping, StudyMaterialFile,ContentMappingLevelChoices, LectureTOCContent

#@login_api_required(login_url='/')
def create_study_material(request):
    CHOICES = {'1': 'Exercise','2': 'Daily Practice Problems','3':'Solved Examples',
        '4':"Notes",'5': "Video"}
    subject_id = request.POST.get('subject_id')
    parent_toc_id = request.POST.get('parent_toc_id')
    type = request.POST.get('type')
    study_material_id = None
    assessment_id = None
    data = {}
    if int(type) in [ContentSubtypeChoices.EXERCISE, ContentSubtypeChoices.DAILY_PRACTICE_PROBLEMS,
        ContentSubtypeChoices.SOLVED_EXAMPLES]:
        content_type = ContentTypeChoices.ASSESSMENT
    else:
        content_type = ContentTypeChoices.STUDY_MATERIAL
    content = Content.objects.create(content_type=content_type, content_subtype=type)
    data['content_id'] = content.id
    data['content_type'] = content_type
    if int(type) in [ContentSubtypeChoices.EXERCISE, ContentSubtypeChoices.DAILY_PRACTICE_PROBLEMS,
        ContentSubtypeChoices.SOLVED_EXAMPLES]:
        assessment = Assessment.objects.create(type=type, content=content)
        data['assessment_id'] = assessment.id
        data['assessment_type'] = type
    else:
        study_material = StudyMaterial.objects.create(type=request.POST.get('type'), content=content)
        data['study_material_id'] = study_material.id
    toc = TOC.objects.get(pk=parent_toc_id)
    level = ContentMappingLevelChoices.get_by_toc_level(toc.level)
    ctm =  ContentTOCMapping.objects.create(content=content, level=level, ref_id=toc.id)
    tocs = TOC.objects.filter(subject_id=subject_id).distinct().order_by('parent_id')
    tocs = TocSerializer(tocs, many=True)
    data['tocs'] = tocs.data
    return JsonResponse(data, safe=False)

#@login_api_required(login_url='/')
def get_study_material(request):
    content_id = request.POST.get('content_id')
    language_id = request.POST.get('language_id')
    study_material_id = None
    assessment_id = None
    data = {}
    sm=StudyMaterial.objects.get(content_id=content_id)
    smf=StudyMaterialFile.objects.filter(study_material=sm,language_id=language_id).first()
    data['file']=smf.file.url
    data['language_id'] = smf.language_id
    data['content'] = smf.content
    data['for'] = 'student' if sm.faculty_only else 'teacher'
    data['duration'] = sm.duration_mins
    data['publish_status'] = smf.publish_status
    data['title'] = sm.title
    data['study_material_file_id'] = smf.id
    return JsonResponse(data, safe=False)


from institute.forms import AssessmentForm
@login_api_required(login_url='/')
def upload_content_data(request):
    content_id = request.POST.get('content')
    if int(request.POST.get('content_type',0)) == 1:
        file = request.FILES['file']
        study_material = StudyMaterial.objects.get(content_id=content_id)

        if request.POST.get('for') == "teacher":
            study_material.faculty_only=True
        study_material.duration_mins=request.POST.get('duration')
        study_material.title=request.POST.get('title')
        study_material.save()
        content=request.POST.get('description')
        if request.POST.get('study_material_file_id'):
            StudyMaterialFile.objects.filter(id=request.POST.get('study_material_file_id')).update(study_material=study_material, content=content,\
                language_id=request.POST.get('language_id'), file=file,publish_status=request.POST.get('publish_status'))
        else:
            StudyMaterialFile.objects.filter(study_material=study_material).delete()
            StudyMaterialFile.objects.create(study_material=study_material, content=content,\
                language_id=request.POST.get('language_id'), file=file,publish_status=request.POST.get('publish_status'))

    else: #its assessment
        form = AssessmentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return JsonResponse({'status':'success'})



class ProgramSessionView(TemplateView):
    template_name = "institutes/program_subject.html"
    @login_required_custom(login_url='/')
    def get(self,request,id=None):
        context_data = {}
        if id == None:
            template_name = self.template_name
        else:
            template_name = "institutes/program_subject.html"
        context_data["status"] = True
        req_count = ProgramClass.objects.all().count()
        target = ProgramClass.objects.all().values()
        subject_class = []
        req_obj = Program.objects.all().values()
        context_data["data"] = req_obj
        return render(request, template_name, context_data)
def session_program(request):
    req_objj = ProgramClass.objects.filter(program_id=request.GET.get('program')).values()
    subject_class = []
    req_count = ProgramClass.objects.filter(program_id=request.GET.get('program')).count()
    if req_count > 0:
        for class_session in req_objj:
            program_id = class_session['program_id']
            class_id = class_session ['classs_id']
            program_ob = {"Program_name":Program.objects.filter(id=program_id).values('label'),"class_name":Classs.objects.filter(id=class_id).values('label'),"Subject_name":Subject.objects.filter(classs=Classs.objects.get(id=class_id)).values('label')}
            subject_class.append(program_ob)
        req_obj = subject_class
        context_data["data"] = req_obj
    else:
        pass
    if req_count > 0:
            paginator = Paginator(req_obj,pagination_ob)
            if id != None:
                paginator = Paginator(req_obj,pagination_ob)
                if request.GET.get('page')==None:
                    page =1
                else:
                    page = int(request.GET.get('page'))
                try:
                    users = paginator.page(page)
                except PageNotAnInteger:
                    users = paginator.page(1)
                except EmptyPage:
                    users = paginator.page(paginator.num_pages)
                program_numpages = paginator.num_pages
                if program_numpages > 0:
                    program_numpage =  program_numpages
                    program_next = users.has_next()
                    program_previous = users.has_previous()
                    program_user_changes = users.has_other_pages()
                    if program_next == True:
                        program_next_page_number = users.next_page_number()
                        program_numpages
                    if page >1:
                        current_page = users.number
                    else:
                        current_page = 1
                    program_index = users.start_index()
                    program_end = users.end_index()
                    if program_next != True:
                        program_record ={"program_numpage":program_numpages,"program_next":program_next,"program_previous":program_previous,"program_user_changes":program_user_changes,"program_index":program_index,"program_end":program_end,"current_page":current_page,"paginator.page_range":paginator.page_range}
                    else:
                        program_next_page_number = users.next_page_number()
                        program_record = {"program_numpage":program_numpages,"program_next":program_next,"program_previous":program_previous,"program_user_changes":program_user_changes,"program_index":program_index,"program_end":program_end,"current_page":current_page,"program_next_page_number":program_next_page_number,"paginator.page_range":paginator.page_range}
                else:
                    program_record = {"program_numpage":program_numpage}
                context_data['data']=users
                context_data['pagination']=program_record
                program_numpages = program_numpage+1
                context_data['PAGINATION_COUNT'] = range(1,program_numpages)
            else:
                context_data['data']=req_obj
    else:
        context_data['data'] = {}
    return HttpResponse(context_data)

from django.contrib.auth import authenticate,login,logout
class LoginViews(TemplateView):
    template_name = "users/login.html"
    def get(self,request):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/dashboard/")
        else:
            return render(request, self.template_name, context_data)
        return render(request, self.template_name, context_data)


    def post(self,request):
        context_data ={}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/dashboard/")
        else:
            context_data['error'] = {"errors" : "Username or Password is not correct"}
            return render(request, self.template_name, context_data)
        return render(request, self.template_name, context_data)



def logout_request(request):
    logout(request)
    #messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect("/institute/login/")

def created_dpps(request):
    subject_id=request.POST.get('subject_id')
    batch_id=request.POST.get('batch_id')
    for assessment in Assessment.objects.filter(type=QuestionCategoryChoices.DAILY_PRACTICE_PROBLEMS,\
        dppplanner__isnull=True):
        DPPPlanner.objects.create(assessment=assessment, subject_id=subject_id, batch_id=batch_id)
    return JsonResponse({'status':'Success'})
