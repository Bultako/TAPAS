import os.path 
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from archive.webinterface.views import *
from archive.webinterface.infos import *
from archive.webinterface.utils import *

from django.contrib import admin
admin.autodiscover()

# urlpatterns
urlpatterns = patterns('',

    # admin:
    (r'^admin/(.*)', admin.site.root),

    # flat pages:
    (r'^$', direct_to_template, {'template':'index.html'}),
    (r'^help/$', direct_to_template, {'template':'help.html'}),
    (r'^news/$', direct_to_template, {'template':'news.html'}),
    (r'^policy/$', direct_to_template, {'template':'policy.html'}),
    (r'^about/$', direct_to_template, {'template':'tech.html'}),

    # help popups:
    (r'^helpcone/$', direct_to_template, {'template':'helpcone.html'}),
    (r'^helprj/$', direct_to_template, {'template':'helprj.html'}),
    (r'^helpdate/$', direct_to_template, {'template':'helpdate.html'}),
    (r'^helpfile/$', direct_to_template, {'template':'helpfile.html'}),
    (r'^helprx/$', direct_to_template, {'template':'helprx.html'}),
    (r'^helplines/$', direct_to_template, {'template':'helplines.html'}),
    (r'^helptau/$', direct_to_template, {'template':'helptau.html'}),

    # authenticate:
    (r'^login/$', login),
    (r'^logout/$', logout),

    # form layout:
    (r'^sources/$', searchform),

    # 
    # source lists query results
    (r'^sourcelist/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', sourcelist, {'template':'sourcelist.html'}),
    (r'^sourcelistprj/(?P<prjid>\d+)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', sourcelist,{'template':'sourcelist.html'}),

    # csv
    (r'^sourcelist/csv/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', sourcelist, {'template':'sourcelist.csv', 'mimetype':'text/plain'}),
    (r'^sourcelistprj/csv/(?P<prjid>\d+)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', sourcelist,{'template':'sourcelist.csv', 'mimetype':'text/plain'}),

    # votable
    (r'^sourcelist/votable/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', sourcelist, {'template':'sourcelist.xml', 'mimetype':'text/xml'}),
    (r'^sourcelistprj/votable/(?P<prjid>\d+)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', sourcelist,{'template':'sourcelist.xml', 'mimetype':'text/xml'}),

    # 
    # scans lists
    (r'^(?P<prjid>\d+)/scanlist/(?P<kind>all)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.html'}),
    (r'^(?P<prjid>\d+)/scanlist/(?P<kind>het)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.html'}),
    (r'^(?P<prjid>\d+)/scanlist/(?P<kind>bol)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.html'}),
    (r'^(?P<prjid>\d+)/scanlist/(?P<kind>het)/sourcerx/(?P<rxid>\d+)/(?P<sourceid>\d+)/(?P<page>\d+)/(?P<nbitems>\d+)/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.html'}),
    (r'^(?P<prjid>\d+)/scanlist/(?P<kind>bol)/sourcerx/(?P<rxid>\d+)/(?P<sourceid>\d+)/(?P<page>\d+)/(?P<nbitems>\d+)/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.html'}),

    # csv
    (r'^(?P<prjid>\d+)/scanlist/csv/(?P<kind>all)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.csv', 'mimetype':'text/plain'}),
    (r'^(?P<prjid>\d+)/scanlist/csv/(?P<kind>het)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.csv', 'mimetype':'text/plain'}),
    (r'^(?P<prjid>\d+)/scanlist/csv/(?P<kind>bol)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.csv', 'mimetype':'text/plain'}),
    (r'^(?P<prjid>\d+)/scanlist/csv/(?P<kind>het)/sourcerx/(?P<rxid>\d+)/(?P<sourceid>\d+)/(?P<page>\d+)/(?P<nbitems>\d+)/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.csv', 'mimetype':'text/plain'}),
    (r'^(?P<prjid>\d+)/scanlist/csv/(?P<kind>bol)/sourcerx/(?P<rxid>\d+)/(?P<sourceid>\d+)/(?P<page>\d+)/(?P<nbitems>\d+)/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.csv', 'mimetype':'text/plain'}),

    # votable
    (r'^(?P<prjid>\d+)/scanlist/votable/(?P<kind>all)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.xml', 'mimetype':'text/xml'}),
    (r'^(?P<prjid>\d+)/scanlist/votable/(?P<kind>het)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.xml', 'mimetype':'text/xml'}),
    (r'^(?P<prjid>\d+)/scanlist/votable/(?P<kind>bol)/(?P<page>\d+)/(?P<nbitems>\d{2,4})/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.xml', 'mimetype':'text/xml'}),
    (r'^(?P<prjid>\d+)/scanlist/votable/(?P<kind>het)/sourcerx/(?P<rxid>\d+)/(?P<sourceid>\d+)/(?P<page>\d+)/(?P<nbitems>\d+)/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.xml', 'mimetype':'text/xml'}),
    (r'^(?P<prjid>\d+)/scanlist/votable/(?P<kind>bol)/sourcerx/(?P<rxid>\d+)/(?P<sourceid>\d+)/(?P<page>\d+)/(?P<nbitems>\d+)/(?P<order>\w+)/(?P<desc>\w+)/$', scanlist, {'template':'scanlist.xml', 'mimetype':'text/xml'}),

    # 
    # project info details
    (r'^project/(?P<prjid>\d+)/$', project_info),

    # 
    # scan info details
    (r'^scan/(?P<scanid>\d+)/$', scan_info),


    # 
    # VO Conesearch
    (r'^conesearch$', conesearch, {'template':'conesearch.xml', 'mimetype':'text/xml'}),


)
 
