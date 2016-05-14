from django.template import Library, Node, resolve_variable, TemplateSyntaxError, Variable
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, para, var):
  dict_ = context['request'].GET.copy()
  dict_[para] = var
  return "?" + dict_.urlencode()

@register.simple_tag(takes_context=True)
def back_view_url(context):
  return "/".join(context['request'].path.split('/')[:4]) + "/"
