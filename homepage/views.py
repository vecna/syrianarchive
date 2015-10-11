from homepage.models import *
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from page.models import *
from database.models import *

def index(request):
    sections = Section.objects.all()
    blog_posts = Post.objects.all()
    incidents = DatabaseEntry.objects.all()[:5]

    return render(request, 'homepage/index.html', {'sections' : sections, 'blog_posts':blog_posts,'incidents':incidents,})