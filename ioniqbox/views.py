
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse

def homepage_view(request):

    return HttpResponse("")