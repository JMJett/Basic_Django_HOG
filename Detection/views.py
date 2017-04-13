from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from .models import Video

# Create your views here.

class IndexView(generic.ListView):
    template_name = "Detection/index.html"
    context_object_name = "human_list"

    def get_queryset(self):
        return Video.objects.filter(human=True)