from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^about$', views.about, name='about'),
    url(r'^submission/new/$', views.submission_new, name='submission_new'),
    url(r'^submission/(?P<pk>\d+)/$', views.submission_detail, name='submission_detail'),
    url(r'^submission/(?P<pk>\d+)/edit/$', views.submission_edit, name='submission_edit'),
    url(r'^submission/thankyou/$', views.submission_thankyou, name='submission_thankyou'),
    url(r'^mapQuery', views.map_query),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)