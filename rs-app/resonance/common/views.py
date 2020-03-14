from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from functools import wraps


def login_required_custom(login_url=None):
    def function(func):
        def wrapper(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseRedirect("/institute/login/")
            return func(self, request, *args, **kwargs)
        return wrapper
    return function

def login_api_required(login_url=None):
    def function(func):
        def wrapper(request):
            if  not request.user.is_authenticated:
                return HttpResponseRedirect("/institute/login/")

            return func(request)
        return wrapper
    return function



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
    return users,context_data
