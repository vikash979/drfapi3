from django.shortcuts import render
from django.views.generic import TemplateView , View

from django.http import HttpResponse ,HttpResponseRedirect

from institute.models import Classs, Program



class ClassViews(TemplateView):
    template_name = "institutes/class.html"
    def get(self, request, id=None):
        print(id)
        if id == None:
            template_name = self.template_name
        else:
            template_name = "institutes/edit_class.html"
        

        context_data = {}
        context_data["status"] = True
        req_count = Classs.objects.all().count()
        if req_count > 0:
            if id == None:
                req_obj = Classs.objects.all().values()
            else:
                req_obj = Classs.objects.get(id=id)
            context_data["data"] = req_obj
        else:
            context_data["data"] = "There is no data"

        print(template_name)
        return render(request, template_name, context_data)

    def post(self,request,id=None):
        context_data = {}
        req_obj = Classs.objects.all().values()
        context_data["data"] = req_obj
        if request.method == "POST":
            label = request.POST.get('title')
            if label:
                label = label.strip()
                if len(label) != 0:
                    description = request.POST.get('description')
                    order = request.POST.get('order')
                    #print(request.POST.get('hidden_id'))
                    print("@@@@@@@@@@@@@@@@@",str(request.POST.get('hidden_id')))
                    if request.POST.get('hidden_id')=='':
                        req_obj = Classs.objects.get_or_create(label=label,description=description,order=order)
                    else:
                        if request.POST.get('hidden_id')=='':
                        #print(label,description,type(int(order)))
                            req_obj = Classs.objects.filter(id=request.POST.get('hidden_id')).update(label=label,description=description,order=request.POST.get('hidden_id'))
                            req_obj = Classs.objects.all().values()
                        else:
                            req_obj = Classs.objects.all().values()
                        
                        
                    if req_obj[1] ==  False:
                        
                        context_data["status"] = False
                        context_data["message"] = "record already exist"
                        context_data["data"] = req_obj
                        
                        #return render(request, self.template_name, context_data)
                    else:
                        
                        context_data["status"] = True
                        #req_obj = Classs.objects.all().values()

                        context_data["data"] = req_obj
                       # return render(request, self.template_name, context_data)
                else:
                    
                    context_data["status"] = False
                    context_data["message"] = "please provide your input"
                    #req_obj = Classs.objects.all().values()

                    context_data["data"] = req_obj
                    #return render(request, self.template_name, context_data)
        else:
            
            context_data["status"] = False
            context_data["message"] = "please provide your input"
            req_obj = Classs.objects.all().values()

            context_data["data"] = req_obj
        
        print("@@@@@@@@@@@@@!!",self.template_name)
        return render(request, self.template_name, context_data)






    