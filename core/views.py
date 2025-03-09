from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    template = loader.get_template("core/index.html")
    return HttpResponse(template.render(context={}, request=request))