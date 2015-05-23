from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _

from page.views import blog

from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'homepage.views.index', name='home'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^blog/', 'page.views.blog', name='blog'),
    url(r'^home/', include('homepage.urls')),
    url(r'^p/', include('page.urls')),
    url(_(r'^database/'), include('database.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),

)
