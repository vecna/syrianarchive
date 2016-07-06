from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
import uuid
from datetime import datetime
import dateutil.parser
from django.utils.decorators import method_decorator

from django.views.generic import View

from database.models import DatabaseEntry as Entry


# "Video ID","Video URL","Title","Description","Publishing Date","Duration","Uploader","Download date"


def not_authorized():
  raise Http404

def api_request_data(request):
  return json.loads(request.body.decode("utf-8"))


allowedIps = ['127.0.0.1', #localhoost
              '176.9.58.142', # media.syrianarchive url
              ]

def ip_authorize(view_func):
  def authorize(view, request, *args, **kwargs):
    user_ip = request.META['HTTP_X_REAL_IP'] if 'HTTP_X_REAL_IP' in request.META else request.META['REMOTE_ADDR']
    if user_ip in allowedIps:
      return view_func(view, request, *args, **kwargs)
    return not_authorized()
  return authorize


class Database(View):

  @method_decorator(csrf_exempt)
  def dispatch(self, *args, **kwargs):
    return super(Database, self).dispatch(*args, **kwargs)

  @ip_authorize
  def get(self, request):
    return JsonResponse( map(lambda x:
        {
          'name':x.name,
        },
        Entry.objects.all()), safe=False )

  @ip_authorize
  def put(self, request):
    bigdata = api_request_data(request)
    ha = hashlib.sha224(str(bigdata)).hexdigest()

    entry, created = Entry.objects.get_or_create( initial_data_hash = ha )

    if not created:
      return HttpResponse("OBJECT ALREADY THERE")

    try:
      entry.validated           = False
      entry.youtube_id          = bigdata["Video ID"]
      entry.reference_code      = ha
      entry.online_link         = bigdata["Video URL"]
      entry.online_title        = bigdata["Title"]
      entry.description         = bigdata["Title"] + bigdata["Description"]
      entry.video_source        = bigdata["Uploader"]
      entry.recording_date      = dateutil.parser.parse(bigdata["Publishing Date"])
      entry.added_date          = datetime.now()
      entry.date_of_acquisition = dateutil.parser.parse(bigdata["Download Date"])
      entry.acquired_from        = "littlefork"
      entry.staff_id            = "littlefork"
      entry.video_url           = bigdata["link"]


      entry.name = entry.reference_code

      entry.save()
    except:
      entry.delete()
      return HttpResponse("MALFORMED DATA -- NOTHING ADDED")

    return JsonResponse({"success":"entry added successfully"})

