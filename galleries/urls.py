from django.conf.urls import *
from django.contrib.sites.models import Site
from django.views.generic import DetailView, ListView

from galleries.models import Gallery

current_site = Site.objects.get_current()

urlpatterns = patterns('',
  (r'^$', ListView.as_view(
     queryset=Gallery.objects.filter(published=True),
     template_name="galleries/gallery_list.html",
     template_object_name="gallery",
     extra_context={'site': current_site}
  )),
  (r'^(?P<slug>[-\w]+)/$', DetailView.as_view(
     queryset=Gallery.objects.all(),
     slug_field='slug',
     template_name="galleries/gallery_detail.html",
     template_object_name="gallery",
     extra_context={'site': current_site}
  )),
)