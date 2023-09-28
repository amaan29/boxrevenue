from django.shortcuts import render
from BORevenuePred import *
# Create your views here.


def base(request):
    dist = request.GET.get('dist')
    return render(request, 'base.html')
