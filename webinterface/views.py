from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from archive.webinterface.forms import *
from archive.webinterface.models import *
from archive.webinterface.querysources import *
from archive.webinterface.queryscans import *
from archive.webinterface.querycone import *
from archive.webinterface.utils import *
from archive.scans.models import Project
from archive.sources.models import ObservedSource, SourceRadialVelocity
from archive.static.models import stRxNames
from django.db import connection
from django.conf import settings
import re

# search form
def searchform(request):

    # cookie control
    messagecookie = cookiecontrol(request)
    if messagecookie!='':
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form, 'other_errors':messagecookie}, context_instance=RequestContext(request))

    # data processing
    if request.method == 'POST':

        if request.POST['axe'] == 'clear':
            form = SourceSearchForm()
            return render_to_response('sourceform.html', {'form':form}, context_instance=RequestContext(request))

        if request.POST['axe'] == 'edit':
            instancesearch = SourceSearch.objects.get(session_id=request.COOKIES["sessionid"])
            form = SourceSearchForm(instance=instancesearch)
            return render_to_response('sourceform.html', {'form':form}, context_instance=RequestContext(request))

        if request.FILES:
            request.POST['source_name'] = ''
            request.POST['ra'] = ''
            request.POST['dec'] = ''
            request.POST['size'] = ''
            request.POST['opacity'] = ''
            request.POST['frequency_from'] = ''
            request.POST['frequency_to'] = ''
            request.POST['velocity_from'] = ''
            request.POST['velocity_to'] = ''
            request.POST['line_name'] = ''
            request.POST['date_from'] = ''
            request.POST['date_to'] = ''
            request.POST['project_id'] = ''
            if 'receivers' in request.POST:
                del request.POST['receivers']

        try:
            instancesearch = SourceSearch.objects.get(session_id=request.COOKIES['sessionid'])
            request.POST['session_id'] = instancesearch.session_id
            form = SourceSearchForm(request.POST.copy(), request.FILES, instance=instancesearch)
        except:
            request.POST['session_id'] = request.COOKIES['sessionid']
            form = SourceSearchForm(request.POST.copy(), request.FILES)
     
        if form.is_valid():
          
            # validation: not empty form
            vide = True
            if request.POST['source_name']:
                vide = False
            if request.POST['ra']:
                vide = False
            if request.POST['dec']:
                vide = False
            if request.POST['size']:
                vide = False
            if request.POST['opacity']:
                vide = False
            if request.POST['frequency_from']:
                vide = False
            if request.POST['frequency_to']:
                vide = False
            if request.POST['velocity_from']:
                vide = False
            if request.POST['velocity_to']:
                vide = False
            if request.POST['line_name']:
                vide = False
            if request.POST['date_from']:
                vide = False
            if request.POST['date_to']:
                vide = False
            if request.POST['project_id']:
                vide = False
            if 'receivers' in request.POST:
                vide = False
            if request.FILES:
                vide = False

            # Ok !
            if not vide:
                form.save()
                # redirection to list results 
                return HttpResponseRedirect("/tapas/sourcelist/1/50/sourceName/down/")

            else:
                # empty form 
                return render_to_response('sourceform.html', {'form':form, 'empty':'Please, enter some data'}, context_instance=RequestContext(request))
        else:
            # errors in form
            other_errors = form.non_field_errors()
            return render_to_response('sourceform.html', {'form':form, 'other_errors':other_errors}, context_instance=RequestContext(request))

    else:
    # form display
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form}, context_instance=RequestContext(request))

# wrapping for source list
def sourcelist(request, prjid='', page=1, nbitems=50, order='sourceName', desc='down', template='sourcelist.html', mimetype='text/html'):

    projectId = ''
    previouspage = int(page) - 1

    # cookie browser control
    messagecookie = cookiecontrol(request)
    if messagecookie!='':
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form, 'other_errors':messagecookie}, context_instance=RequestContext(request))
    
    if prjid!='':
        HTMLURL = '/tapas/sourcelistprj/'+prjid
        csvURL = '/tapas/sourcelistprj/csv/'+prjid+'/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'
        VOTableURL = '/tapas/sourcelistprj/votable/'+prjid+'/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'

        projectrecord = Project.objects.get(id=prjid)
        projectId = projectrecord.projectId
        
        queryset, totalcount, nextpage = sources(request, page=page, nbitems=nbitems, order=order, desc=desc, prjid=prjid)

    else:
        HTMLURL = '/tapas/sourcelist'
        csvURL = '/tapas/sourcelist/csv/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'
        VOTableURL = '/tapas/sourcelist/votable/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'

        # only search saved
        try:
            searchrecord = SourceSearch.objects.get(session_id=request.COOKIES['sessionid'])

        except:
            form = SourceSearchForm()
            return render_to_response('sourceform.html', {'form':form, 'other_errors':'Please, select search criteria.'}, context_instance=RequestContext(request))

        # control file format
        if searchrecord.batchfile:
            errormesg = fileformatcontrol(searchrecord.batchfile)
            if errormesg:
                form = SourceSearchForm()
                return render_to_response('sourceform.html', {'form':form, 'other_errors':errormesg}, context_instance=RequestContext(request))               
            queryset, totalcount = batchfilesearch(request, searchrecord.batchfile)
            nextpage = ''
        else:
            queryset, totalcount, nextpage = sources(request, page=page, nbitems=nbitems, order=order, desc=desc, prjid=prjid)

 
    criteriatable = criteria(request)


    # no records found
    if not queryset:
        instancesearch = SourceSearch.objects.get(session_id=request.COOKIES["sessionid"])
        form = SourceSearchForm(instance=instancesearch)
        other_errors = 'No records found. '
        return render_to_response('sourceform.html', {'form':form, 'other_errors':other_errors}, context_instance=RequestContext(request))

    if desc == 'down':
        updesc = 'up'
    else:
        updesc = 'down'

    dico = {
        'queryset':queryset,
        'votable':votable(),
        'criteriatable':criteriatable,
        'page':page,
        'nbitems':nbitems,
        'order':order,
        'projectId':projectId,
        'HTMLURL':HTMLURL,
        'VOTableURL':VOTableURL,
        'csvURL':csvURL,
        'previouspage':previouspage,
        'nextpage':nextpage,
        'prjid':prjid,
        'totalcount':totalcount,
        'settings':settings,
        'desc':desc,
        'updesc':updesc,
        }

    return render_to_response(template, dico, context_instance=RequestContext(request), mimetype=mimetype)

# wrapping for scan list
def scanlist(request, kind, prjid, rxid='', sourceid='', page=1, nbitems=50, order='ncsID', desc='down', template='scanlist.html', mimetype='text/html'):

    projectrecord = ''
    sourcerecord = ''
    rxrecord = ''
    previouspage = int(page) - 1

    # cookie browser control
    messagecookie = cookiecontrol(request)
    if messagecookie!='':
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form, 'other_errors':messagecookie}, context_instance=RequestContext(request))

    HTMLURL = '/tapas/'+prjid+'/scanlist/'+kind
    csvURL = '/tapas/'+prjid+'/scanlist/csv/'+kind+'/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'
    VOTableURL = '/tapas/'+prjid+'/scanlist/votable/'+kind+'/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'

    if rxid!='' and sourceid!='':
        HTMLURL = '/tapas/'+prjid+'/scanlist/'+kind+'/sourcerx/'+rxid+'/'+sourceid
        csvURL = '/tapas/'+prjid+'/scanlist/csv/'+kind+'/sourcerx/'+rxid+'/'+sourceid+'/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'
        VOTableURL = '/tapas/'+prjid+'/scanlist/votable/'+kind+'/sourcerx/'+rxid+'/'+sourceid+'/'+page+'/'+nbitems+'/'+order+'/'+desc+'/'

    projectrecord = Project.objects.get(id=prjid)

    if  sourceid!='':
        source = ObservedSource.objects.get(id=sourceid)
        try:
            ra=radians2ra(source.lambdaField)
        except:
            ra=source.lambdaField
        try:
            dec=radians2dec(source.beta)
        except:
            dec=source.beta

        sourcerecord = {
            'sourcename':source.sourceName,
            'velocity':source.sourceRadialVelocity.velocity/1000.,
            'ra':ra,
            'dec':dec,
        }

    if  rxid!='':
        rxrecord = stRxNames.objects.get(id=rxid)

    criteriatable = criteria(request)
    queryset, totalcount, nextpage = scans(request, prjid=prjid, page=page, nbitems=nbitems, order=order, desc=desc, kind=kind, sourceid=sourceid, rxid=rxid)

    if desc == 'down':
        updesc = 'up'
    else:
        updesc = 'down'

    dico = {
        'queryset':queryset,
        'votable':votable(),
        'criteriatable':criteriatable,
        'page':page,
        'nbitems':nbitems,
        'order':order,
        'kind':kind,
        'projectrecord':projectrecord,
        'sourcerecord':sourcerecord,
        'rxrecord':rxrecord,
        'HTMLURL':HTMLURL,
        'VOTableURL':VOTableURL,
        'csvURL':csvURL,
        'previouspage':previouspage,
        'nextpage':nextpage,
        'totalcount':totalcount,
        'desc':desc,
        'updesc':updesc,
    }

    return render_to_response(template, dico, context_instance=RequestContext(request), mimetype=mimetype)

# wrapping for conesearch
def conesearch(request, template='conesearch.xml', mimetype='text/html'):

    ra = ''
    dec = ''
    radius = ''
    errormsg = ''

    # parameters control
    try:
        ra = request.GET['RA']
    except:        
        template = 'error.xml'
        errormsg = 'RA parameter missing'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)   
    if ra == '':
        template = 'error.xml'
        errormsg = 'RA parameter missing'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
    try:
        if float(ra)>360:
            template = 'error.xml'
            errormsg = 'RA parameter has to be no greater than 360'
            return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
        if float(ra)<0:
            template = 'error.xml'
            errormsg = 'RA parameter has to be greater than 0'
            return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
    except:
        template = 'error.xml'
        errormsg = 'RA parameter is not in the right format'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)

    try:
        dec = request.GET['DEC']
    except:        
        template = 'error.xml'
        errormsg = 'DEC parameter missing'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)   
    if dec == '':
        template = 'error.xml'
        errormsg = 'DEC parameter missing'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
    try:
        if float(dec)>90:
            template = 'error.xml'
            errormsg = 'DEC parameter has to be no greater than 90'
            return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
        if float(dec)<-90:
            template = 'error.xml'
            errormsg = 'DEC parameter has to be no lower than -90'
            return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
    except:
        template = 'error.xml'
        errormsg = 'DEC parameter is not in the right format'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
    try:
        radius = request.GET['SR']
    except:        
        template = 'error.xml'
        errormsg = 'SR parameter missing'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)   
    if radius == '':
        template = 'error.xml'
        errormsg = 'SR parameter missing'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)   
    try:
        if float(radius)>30:
            template = 'error.xml'
            errormsg = 'SR parameter has to be no greater than 30'
            return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
        if float(radius)<0:
            template = 'error.xml'
            errormsg = 'SR parameter has to be greater than 0'
            return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
    except:
        template = 'error.xml'
        errormsg = 'SR parameter is not in the right format'
        return render_to_response(template, {'errormsg':errormsg}, context_instance=RequestContext(request), mimetype=mimetype)
   
    queryset, totalcount = cone(request)

    dico = {
        'votable':votable(),
        'queryset':queryset,
        'totalcount':totalcount,
    }

    return render_to_response(template, dico, context_instance=RequestContext(request), mimetype=mimetype)
