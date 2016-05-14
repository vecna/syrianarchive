from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404, HttpResponse

def paginate(request, collection):
  paginator = Paginator(collection, 50)
  page = request.GET.get('page')
  try:
    return paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    return paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    return []
