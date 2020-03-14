from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from subject.models import MasterSubject, Subject
from django.views.generic import TemplateView, View
from institute.models import Classs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import TOC
from common.views import login_required_custom,login_api_required

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

def render_statement_subject(reques_args,status,message,template,model,class_model,master_model):
    context_data["status"]=status
    context_data["message"]=message
    context_data["data"]=model
    context_data["class"]=class_model
    context_data["master_subject"]=master_model
    return render(reques_args, template, context_data)

def get_for_mastersubject(request,model,template):
    context_data["status"]=""
    req_obj = model.objects.all().filter(object_status=0).order_by("-id")
    req_obj = paginator_maker(request,req_obj)
    context_data["data"]=req_obj
    return render(request, template, context_data)

def post_for_mastersubject(request,model,template):
    req_obj_all = model.objects.all().filter(object_status=0).order_by("-id")
    req_obj_all = paginator_maker(request,req_obj_all)
    label= request.POST.get("label")
    short_code = request.POST.get("short_code")
    description = request.POST.get("description")
    id=request.POST.get("id")
    action=request.POST.get("action")
    id=id.strip()
    if action==None:
        if len(id)==0:
            if label and short_code:
                label=label.strip()
                short_code=short_code.strip()
                short_code_model = MasterSubject.objects.filter(short_code=short_code,object_status=0)
                description=description.strip()
                if len(short_code_model)==0:
                    if len(label)!=0 and len(short_code)!=0:
                        try:
                            req_master = model.objects.get(label=label,object_status=0)
                            return render_statement(request,False,"Record Already Exists On Name",template,req_obj_all)
                        except:
                            req_obj,created = model.objects.get_or_create(label=label,short_code=short_code,object_status=0)
                            req_obj.description = description
                            req_obj.save()
                            if created:
                                return render_statement(request,True,"Successfully Created",template,req_obj_all)
                            else:
                                return render_statement(request,False,"Record Already Exist",template,req_obj_all)
                        
                    else:
                        return render_statement(request,False,"please provide your input",template,req_obj_all)
                else:
                    return render_statement(request,False,"Master Subject Already Exists On Short Code",template,req_obj_all)
            else:
                return render_statement(request,False,"please provide your input",template,req_obj_all)
        else:
            id=id.strip()
            id=int(id)
            label = label.strip()
            short_code=short_code.strip() 
            description=description.strip()
            req_data = request.POST
            if len(label) != 0 and len(short_code) != 0:
                try:
                    req_update_object = model.objects.get(id=id,label= label,short_code=short_code,object_status=0)
                    req_update_object.description=description
                    req_update_object.save()
                    return render_statement(request,True,"Successfully Updated",template,req_obj_all) 
                except:
                    try:
                        req_update_object = model.objects.get(label= label,short_code=short_code,object_status=0)
                        return render_statement(request,False,"Record Already Exist On Name and Short Code",template,req_obj_all)
                    except:
                        try:
                            req_update_object = model.objects.get(label= label,object_status=0)
                            return render_statement(request,False,"Record Already Exist On Name",template,req_obj_all)
                        except:
                            updatable = ["label","short_code","description"]
                            try:
                                req_obj = model.objects.get(id=id,object_status=0)
                            except:
                                return render_statement(request,False,"no record found",template,req_obj_all)
                            if req_obj.short_code==short_code:
                                req_obj.label,req_obj.short_code,req_obj.description=label,short_code,description
                                req_obj.save()
                                return render_statement(request,True,"Successfully Updated",template,req_obj_all)
                            else:
                                return render_statement(request,False,"Short Code Cannot be updated",template,req_obj_all)
            else:
                return render_statement(request,False,"Please provide valid input",template,req_obj_all)
    else:
        if action=="delete":
            id = request.POST.get("id")
            if id!=None:
                id=id.strip()
                req_obj = model.objects.filter(id=id).update(object_status=1)
                return render_statement(request,"Deleted","Successfully Deleted",template,req_obj_all)

def get_for_subject(request,model,template):
    context_data["status"]=""
    class_filter = request.GET.get("class")
    if class_filter == None:
        req_obj = model.objects.all().filter(object_status=0).order_by("-id")
    else:
        class_filter = int(class_filter)
        req_obj = model.objects.filter(classs_id=class_filter,object_status=0).order_by("-id")
    req_obj = paginator_maker(request,req_obj)
    req_class_obj = Classs.objects.all().filter(object_status=0)
    req_master_obj=MasterSubject.objects.all().filter(object_status=0)
    context_data["data"]=req_obj
    context_data["class"]=req_class_obj
    context_data["master_subject"]=req_master_obj
    return render(request, template, context_data)

@login_api_required(login_url='/')
def get_class_subject_id(request):
    class_filter = request.GET.get('class')
    print(class_filter)
    subject = Subject.objects.filter(classs_id=class_filter,object_status=0).order_by('id')
    #tocs = TocSerializer(tocs, many=True)
    sub_ob =(subject.values('label','id'))
    sub_data =[subject_class for subject_class in sub_ob ]
    
    return JsonResponse({"sub_data":sub_data}, safe=False)



def post_for_subject(request,model,template):
    req_obj_all = model.objects.all().filter(object_status=0).order_by("-id")
    req_obj_all = paginator_maker(request,req_obj_all)
    req_class_obj = Classs.objects.all().filter(object_status=0)
    req_master_obj=MasterSubject.objects.all().filter(object_status=0)
    label= request.POST.get("label")
    code = request.POST.get("code")
    description = request.POST.get("description")
    classs_id = request.POST.get("classs_id")
    master_subject_id = request.POST.get("master_subject_id")
    id=request.POST.get("id")
    action=request.POST.get("action")
    id=id.strip()
    if action==None:
        if len(id)==0:
            if label and code and classs_id and master_subject_id:
                code_model = Subject.objects.filter(code=code,object_status=0)
                label=label.strip()
                code=code.strip()
                description=description.strip()
                classs_id=classs_id.strip()
                master_subject_id=master_subject_id.strip()
                if len(code_model)==0:
                    if len(label)!=0 and len(code)!=0 and len(classs_id)!=0 and len(master_subject_id)!=0:
                        try:
                            req_master = MasterSubject.objects.get(id=master_subject_id)
                        except:
                            return render_statement_subject(request,False,"no record found",template,req_obj_all,req_class_obj,req_master_obj)
                        try:
                            req_obj = model.objects.get(label=label,classs_id=classs_id,object_status=0)
                            return render_statement_subject(request,False,"Record Already Exist",template,req_obj_all,req_class_obj,req_master_obj)
                        except:
                            req_obj = model.objects.get_or_create(label=label,code=code,description=description,classs_id=classs_id,master_subject_id=master_subject_id,object_status=0)
                            if req_obj[1]==False:
                                return render_statement_subject(request,False,"Record Already Exist",template,req_obj_all,req_class_obj,req_master_obj)
                            elif req_obj[1]==True:
                                return render_statement_subject(request,True,"Successfully Created",template,req_obj_all,req_class_obj,req_master_obj)
                    else:
                        return render_statement_subject(request,False,"please provide your input",template,req_obj_all,req_class_obj,req_master_obj)
                else:
                    return render_statement_subject(request,False,"Subject Already Exists On Code",template,req_obj_all,req_class_obj,req_master_obj)
            else:
                return render_statement_subject(request,False,"please provide your input",template,req_obj_all,req_class_obj,req_master_obj)
        else:
            id=id.strip()
            id=int(id)
            label = label.strip()
            code=code.strip() 
            description=description.strip()
            classs_id=classs_id.strip()
            master_subject_id=master_subject_id.strip()
            req_data = request.POST
            if len(label) != 0 and len(code) != 0 and len(classs_id) != 0 and len(master_subject_id) != 0:
                try:
                    req_update_object = model.objects.get(id=id,label= label,code=code,object_status=0)
                    req_update_object.description=description
                    req_update_object.save()
                    return render_statement(request,True,"Successfully Updated",template,req_obj_all) 
                except:
                    try:
                        req_update_object = model.objects.get(label= label,code=code,description=description,classs_id=classs_id,master_subject_id=master_subject_id,object_status=0)
                        return render_statement_subject(request,False,"Record Already Exist",template,req_obj_all,req_class_obj,req_master_obj)
                    except:
                        updatable = ["label","code","description","classs_id","master_subject_id"]
                        try:
                            req_obj = model.objects.get(id=id,object_status=0)
                            req_objmaster = MasterSubject.objects.get(id=master_subject_id)
                        except:
                            return render_statement_subject(request,False,"no record found",template,req_obj_all,req_class_obj,req_master_obj)
                        if req_obj.code==code:
                            for attr in updatable :
                                if attr in req_data :
                                    setattr(req_obj,attr,req_data[attr])
                            req_obj.save()
                            return render_statement_subject(request,True,"Successfully Updated",template,req_obj_all,req_class_obj,req_master_obj)
                        else:
                            return render_statement_subject(request,False,"Code cannot be updated",template,req_obj_all,req_class_obj,req_master_obj)
            else:
                return render_statement_subject(request,False,"Please provide valid input",template,req_obj_all,req_class_obj,req_master_obj)
    else:
        if action=="delete":
            id = request.POST.get("id")
            if id!=None:
                id=id.strip()
                req_obj = model.objects.filter(id=id).update(object_status=1)
                return render_statement_subject(request,"Deleted","Successfully Deleted",template,req_obj_all,req_class_obj,req_master_obj)

class MasterSubjectViews(TemplateView):
    template_name = "subjects/master-subject.html"
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_mastersubject(request,MasterSubject,self.template_name)
    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_mastersubject(request,MasterSubject,self.template_name)

class SubjectViews(TemplateView):
    template_name = "subjects/subjects.html"
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_subject(request,Subject,self.template_name)
    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_subject(request,Subject,self.template_name)


class ClassSubjectViews(TemplateView):
    template_name = "subjects/class-subjects.html"
    
    def get(self, request, *args, **kwargs):
        context_data["status"]=""
        class_filter = request.GET.get("class")
        if class_filter == None:
            req_obj = None
        else:
            class_filter = int(class_filter)
            req_obj = Subject.objects.filter(classs_id=class_filter,object_status=0).order_by("-id")
        req_obj = paginator_maker(request,req_obj)
        req_master_obj=MasterSubject.objects.all().filter(object_status=0)
        context_data["data"]=req_obj
        context_data["class_id"]=class_filter
        context_data["master_subject"]=req_master_obj
        return render(request, self.template_name, context_data)
         
    def post(self, request, *args, **kwargs):
        return post_for_subject(request,Subject,self.template_name)

def render_statement_toc(reques_args,status,message,template,model=None):
    context_data["data"]=model
    context_data["status"]=status
    context_data["message"]=message
    return render(reques_args, template, context_data)

def get_for_toc(request):
    req_html = "subjects/"+request.path.split("/")[-2]+".html"
    toc = request.GET.get("toc")
    subject=request.GET.get("subject")
    if subject==None and toc==None:
        return render(request,req_html)
    elif subject!=None and toc==None:
        subject=int(subject)
        req_obj  = TOC.objects.filter(subject_id = subject,level=0).order_by('-id')
        req_obj=paginator_maker(request,req_obj)
        context_data["data"]=req_obj
        context_data["status"]=""
        context_data["message"]=""
        context_data["subject_id"]=subject
        context_data["subject_name"]=Subject.objects.filter(id=subject)[0].label
        return render(request,req_html,context_data)
    elif subject==None and toc!=None:
        toc=int(toc)
        subject = TOC.objects.get(id=toc).subject_id
        req_obj  = TOC.objects.filter(parent_id = toc).order_by('-id')
        req_obj=paginator_maker(request,req_obj)
        context_data["status"]=""
        context_data["message"]=""
        context_data["data"]=req_obj
        context_data["subject_id"]=subject
        context_data["toc"]=toc
        context_data["toc_name"]=TOC.objects.filter(id=toc)[0].label
        return render(request,req_html,context_data)
    elif subject!=None and toc!=None:
        return render(request,req_html)


def post_for_toc(request):
    req_obj_all = Subject.objects.all().filter(object_status=0).order_by("-id")
    req_obj_all = paginator_maker(request,req_obj_all)
    req_class_obj = Classs.objects.all().filter(object_status=0)
    req_master_obj=MasterSubject.objects.all().filter(object_status=0)
    parent_id,subject_id,level = request.POST.get("parent_id"),request.POST.get("subject_id"),request.POST.get("level")
    label,order=request.POST.get("label"),request.POST.get("order")
    id=request.POST.get("id")
    action = request.POST.get("action")
    if action==None:
        if label and order :
            label,order = label.strip(),order.strip()
            if len(label)!=0 and len(order)!=0:
                parent_id,subject_id,level,order=int(parent_id),int(subject_id),int(level),int(order)
                if len(id)==0:
                    if parent_id==0:
                        TOC.objects.create(label=label,order=order,level=level,subject_id=subject_id)
                        return render_statement_subject(request,True,"Unit Successfully Created","subjects/unit.html",req_obj_all,req_class_obj,req_master_obj)
                    else:
                        TOC.objects.create(label=label,order=order,level=level,subject_id=subject_id,parent_id=parent_id)
                        if level==1:
                            context_data["id"]=parent_id
                            return render_statement_toc(request,True,"Chapter Successfully Created","subjects/chapter.html")
                        elif level==2:
                            context_data["id"]=parent_id
                            return render_statement_toc(request,True,"Topic Successfully Created","subjects/topic.html")
                        elif level==3:
                            context_data["id"]=parent_id
                            return render_statement_toc(request,True,"Sub-Topic Successfully Created","subjects/sub_topic.html")
                else:
                    TOC.objects.filter(id=id).update(label=label,order=order)
                    if level==0:
                        return render_statement_subject(request,True,"Unit Successfully Updated","subjects/unit.html",req_obj_all,req_class_obj,req_master_obj)
                    if level==1:
                        context_data["id"]=parent_id
                        return render_statement_toc(request,True,"Chapter Successfully Updated","subjects/chapter.html")
                    elif level==2:
                        context_data["id"]=parent_id
                        return render_statement_toc(request,True,"Topic Successfully Updated","subjects/topic.html")
                    elif level==3:
                        context_data["id"]=parent_id
                        return render_statement_toc(request,True,"Sub-Topic Successfully Updated","subjects/sub_topic.html")
            else:
                level=int(level)
                if level==0:
                    return render_statement_subject(request,False,"Please Check Your input","subjects/subjects.html",req_obj_all,req_class_obj,req_master_obj)
                elif level ==1:
                    req_obj  = TOC.objects.filter(subject_id = subject_id,level=0)
                    return render_statement_toc(request,False,"Please Check Your input","subjects/unit.html",req_obj)
                elif level ==2:
                    req_obj  = TOC.objects.filter(parent_id = parent_id)
                    return render_statement_toc(request,False,"Please Check Your input","subjects/chapter.html")
                elif level ==3:
                    req_obj  = TOC.objects.filter(parent_id = parent_id)
                    return render_statement_toc(request,False,"Please Check Your input","subjects/topic.html")
        else:
            level=int(level)
            if level==0:
                return render_statement_subject(request,False,"Name and Order Are Mandatory","subjects/subjects.html",req_obj_all,req_class_obj,req_master_obj)
            elif level ==1:
                req_obj  = TOC.objects.filter(subject_id = subject_id,level=0)
                return render_statement_toc(request,False,"Name and Order Are Mandatory","subjects/unit.html",req_obj)
            elif level ==2:
                req_obj  = TOC.objects.filter(parent_id = parent_id)
                return render_statement_toc(request,False,"Name and Order Are Mandatory","subjects/chapter.html")
            elif level ==3:
                req_obj  = TOC.objects.filter(parent_id = parent_id)
                return render_statement_toc(request,False,"Name and Order Are Mandatory","subjects/topic.html")
    else:
        if action=="delete":
            id = request.POST.get("id")
            req_html = "subjects/"+request.path.split("/")[-2]+".html"
            print("req_html",req_html)
            if id!=None:
                id=id.strip()
                req_obj = TOC.objects.filter(id=id)
                subject=req_obj[0].subject_id
                parent = req_obj[0].parent_id
                context_data["subject_id"]=subject
                context_data["toc"]=parent
                req_obj.update(object_status=1)
                return render_statement_toc(request,"Deleted","Successfully Deleted",req_html)
        


class UnitCreationView(View):
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_toc(request)
    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_toc(request)
       
class ChapterCreationView(View):
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_toc(request)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_toc(request)

class TopicCreationView(View):
    
    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_toc(request)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_toc(request)

class SubTopicCreationView(View):

    @login_required_custom(login_url='/')
    def get(self, request, *args, **kwargs):
        return get_for_toc(request)

    @login_required_custom(login_url='/')
    def post(self, request, *args, **kwargs):
        return post_for_toc(request)