from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views import generic
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
import time
from haystack.query import SearchQuerySet
from djgeojson.views import GeoJSONLayerView
from .helpers import *

from django.db.models.query import Q


def index(request):
    current_path = request.get_full_path()
    form = DatabaseFilterForm(request.GET, request.FILES)
    entries = DatabaseEntry.public_objects.all().order_by('-recording_date')

    if request.method == "GET" and request.GET.items():
        if form.is_valid():
            type_of_violation = form.cleaned_data['type_of_violation']
            location = form.cleaned_data['location']
            start_date = form.cleaned_data['startDate']
            end_date = form.cleaned_data['endDate']

            query = Q()
            if type_of_violation:       query &= Q(type_of_violation = type_of_violation)
            if location:                query &= (Q(location = location) | Q(location__region = location))
            if start_date and end_date: query &= Q(recording_date__range = (start_date, end_date))

            entries = entries.filter(query)

    entries = paginate(request, entries)
    return render(request, 'database/index.html', {'entries': entries, 'form':form, "current_path":current_path})

def detail(request, slug):
    incident = get_object_or_404(DatabaseEntry, pk=slug )
    geofield = incident.get_location_field()
    return render(request, 'database/incident.html', {'incident': incident, 'slug':slug,'geofield':geofield})

@login_required
def collections(request):
    collections = Collection.objects.all()
    return render(request, 'database/collections.html', {'collections':collections})

@login_required
def collection(request, id):
    collection = get_object_or_404(Collection, pk=id)
    videos = collection.databaseentry_set.all()
    return render(request, 'database/collection.html', {'collection':collection, 'videos':videos})


class MapLayer(GeoJSONLayerView):
  def get_queryset(self):
      vtype =   self.request.session['violation_type'] if 'violation_type' in self.request.session else None
      if not vtype:
        context = DatabaseEntry.public_objects.all()
      else:
        context = DatabaseEntry.public_objects.filter(type_of_violation__id=vtype)
      return context

def map(request):
  if "violation_type" in request.GET:
    request.session['violation_type'] = request.GET.get("violation_type")
  else:
    request.session['violation_type'] = None
  violationtypes = ViolationType.objects.all()
  for violation in violationtypes:
    violation.count = violation.databaseentry_set.all().count()
  violationtypes = list(violationtypes)
  violationtypes.sort(key=lambda x: x.count, reverse=True)
  return render(request, 'database/map.html',{'violationtypes':violationtypes,})
