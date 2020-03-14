from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from os import chdir, getcwd, listdir, path
from win32com import client
from .models import ConvertedHtml
import base64
import os
from django.utils.encoding import smart_bytes,smart_str
import pythoncom
pythoncom.CoInitialize()

class ContentSaver(View):

    def get(self,request,*args,**kwargs):
        content_id = request.GET.get("content_id")
        content_type = request.GET.get("toc_id")
        if content_id!=None and content_type!=None:
            content_id=content_id.strip()
            content_type=content_type.strip()
            try:
                content_id,content_type=int(content_id),int(content_type)
            except:
                return HttpResponse("content_id and content_type must be integer")
            #try:
            req_obj = ConvertedHtml.objects.get(contentid=content_id, content_type = content_type)
            return HttpResponse(req_obj.html_str,content_type='html')
            #return render(request,path_location)
            #except:
            return HttpResponse("No record found on content_id and content_type")
        else:
            return HttpResponse("content_id and content_type are mandatory")


    def post(self,request,*args,**kwargs):
        content_id = request.POST.get("content_id")
        content_type = request.POST.get("content_type")
        content_file = request.FILES.get("content_file")
        if content_file :
            try:
                req_obj = ConvertedHtml.objects.get(contentid=content_id, content_type = content_type)
                return HttpResponse("record already exists")
            except:
                req_obj = ConvertedHtml.objects.create(contentid=content_id, content_type = content_type,content_file=content_file )
            req_url = req_obj.content_file.path
            file_name = str(req_obj.content_file).split(".")[0]
            print(file_name)
            pythoncom.CoInitialize()
            print("it reached here1")
            word = client.Dispatch("Word.Application")
            print("reached here2")
            doc = word.Documents.Open(req_url)
            print("reached here3")
            doc.SaveAs(r"C:\Users\Administrator\Desktop\doctohtml\doc2html\templates\content_html\{0}-{1}".format(file_name, content_id), FileFormat =10,Encoding="msoEncodingUTF8")
            doc.Close()
            word.Quit()
            req_obj = ConvertedHtml.objects.get(contentid=content_id, content_type = content_type)
            file_name = str(req_obj.content_file).split(".")[0]
            path_location = r"C:\Users\Administrator\Desktop\doctohtml\doc2html\templates\content_html\{0}-{1}.htm".format(file_name, content_id)
            file = open(path_location,'r')
            html_str = ""
            for each in file:
                html_str+=each
            directory = r"C:\Users\Administrator\Desktop\doctohtml\doc2html\templates\content_html\{0}-{1}_files".format(file_name, content_id)
            for filename in os.listdir(directory):
                if filename in html_str:
                    with open(r"C:\Users\Administrator\Desktop\doctohtml\doc2html\templates\content_html\{0}-{1}_files\{2}".format(file_name, content_id,filename), "rb") as img_file:
                        my_string = base64.b64encode(img_file.read())
                    if filename.endswith(".jpg"):
                        my_string = "data:image/jpg;base64,"+str(my_string).split("'")[1]
                        html_str=html_str.replace("{0}-{1}_files/{2}".format(file_name, content_id,filename), str(my_string) )  
                    elif filename.endswith(".png"):
                        my_string = "data:image/png;base64,"+str(my_string).split("'")[1]
                        html_str=html_str.replace("{0}-{1}_files/{2}".format(file_name, content_id,filename), str(my_string) ) 
                    elif filename.endswith(".gif"):
                        my_string =  "data:image/gif;base64,"+str(my_string).split("'")[1] 
                        html_str=html_str.replace("{0}-{1}_files/{2}".format(file_name, content_id,filename), str(my_string) )
                    elif filename.endswith(".wmz"):  
                        my_string = "data:image/wmz;base64,"+str(my_string).split("'")[1]  
                        html_str=html_str.replace("{0}-{1}_files/{2}".format(file_name, content_id,filename), str(my_string) )  
            html_str=html_str.replace("windows-1252","utf-8") 
            req_obj.html_str= html_str
            req_obj.save()
            return "your doc file is parsed"
        else:
            return "please provide file to be parsed"


 
        
       
        
