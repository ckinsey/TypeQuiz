from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'typequiz.views.home', name='home'),
    # url(r'^typequiz/', include('typequiz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'typequiz.web.views.homepage', name='homepage'),
    url(r'^quiz/(?P<slug>[a-zA-Z-]+)/$', 'typequiz.web.views.quiz', name='quiz_detail'),
    url(r'^test_result/(\d+)/$', 'typequiz.web.views.test_result', name='test_result'),
)
