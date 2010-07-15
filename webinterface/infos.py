from django.shortcuts import render_to_response
from django.template import RequestContext
from archive.webinterface.forms import *
from archive.webinterface.querysources import *
from archive.webinterface.queryscans import *
from archive.webinterface.utils import *
from archive.antenna.models import Antenna, Secondary
from archive.backends.models import Backend
from archive.observationSettings.models import *
from archive.observationResults.models import *
from archive.receivers.models import *
from archive.scans.models import Project, Scan
from archive.sources.models import ObservedSource, SourceRadialVelocity
from archive.switchingSettings.models import FrequencySwitching
from django.db.models import Q
from django.db import connection
from datetime import date, timedelta

# project info
def project_info(request, prjid):

    # cookie browser control
    messagecookie = cookiecontrol(request)
    if messagecookie!='':
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form, 'other_errors':messagecookie}, context_instance=RequestContext(request))

    allset, numberallscans, nextpage = scans(request, prjid=prjid, kind='all',nbitems=5000)
    queryset, numberhetscans, nextpage = scans(request, prjid=prjid, kind='het')
    queryset, numberboloscans, nextpage = scans(request, prjid=prjid, kind='bol')
    queryset, numberobsources, nextpage = sources(request, prjid=prjid)

    # data access control
    if numberallscans == 0:
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form}, context_instance=RequestContext(request))

    projectrecord = Project.objects.get(id=prjid)

    # opacity curve
    step=1
    counter=0
    taulist=[]
    datelist=[]
    querystring=''
    if numberallscans>150:
        step=int(numberallscans/150)

    for record in allset :
        if counter==step:
            counter=0
            querystring+="%.3f,"%record['tau']
            taulist.append(record['tau'])
        counter=counter+1
        datelist.append(record['startTime'])
    querystring = querystring[0:len(querystring)-1]
    maxtau=max(taulist)
    mindate=min(datelist)
    maxdate=max(datelist)

    mark=0.
    labels="|0|"
    labelstep=maxtau/10.
    for ilab in range(10):
        mark=mark+labelstep
        labels+="%.3f|"%mark    
    maxtau+=labelstep
        
    criteriatable = criteria(request)

    dico = {
        'projectrecord':projectrecord,
        'allscans':numberallscans,
        'hetscans':numberhetscans,
        'boloscans':numberboloscans,
        'obsources':numberobsources,
        'querystring':querystring,
        'maxtau':maxtau,
        'mindate':mindate,
        'maxdate':maxdate,
        'labels':labels,
        'criteriatable':criteriatable,
    }

    return render_to_response('project_info.html', dico, context_instance=RequestContext(request))

# scan info
def scan_info(request, scanid):

    # cookie browser control
    messagecookie = cookiecontrol(request)
    if messagecookie!='':
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form, 'other_errors':messagecookie}, context_instance=RequestContext(request))

    # data access control
    ok = scanaccess(request, scanid)
    if ok == 0:
        form = SourceSearchForm()
        return render_to_response('sourceform.html', {'form':form}, context_instance=RequestContext(request))

    scanrecord = Scan.objects.get(id=scanid)
    
    # FITS Link
    linkfits = fitscontrol(request, scanid)

    # LST
    try:
        lst=lst2time(scanrecord.LST)
    except:
        lst=scanrecord.LST

    # duration
    timeduration=scanrecord.endTime-scanrecord.startTime
    duration=timeduration.seconds/60.

    # source
    source = ObservedSource.objects.get(scan=scanrecord)
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

    # weather
    weatherrecord = weather(scanrecord.startTime, scanrecord.endTime)

    # antenna
    antenna = Antenna.objects.get(scan=scanrecord)
    secondary = Secondary.objects.get(scan=scanrecord)
    p2 = (180/math.pi)*float(antenna.p2)*60*60
    p7 = (180/math.pi)*float(antenna.p7)*60*60
    antennarecord = {
        'azimuth':antenna.actualAz,
        'elevation':antenna.actualEl,
        'p2':p2,
        'p7':p7,
        'fZ':secondary.focusCorrectionZ,
    }

    # settings
    try:
        focusrecord = FocusSettings.objects.get(scan=scanrecord)
    except:
        focusrecord = ''
    try:
        tiprecord = TipSettings.objects.get(scan=scanrecord)
    except:
        tiprecord = ''
    try:
        pointing = PointingSettings.objects.get(scan=scanrecord)
        pointinglenght = radians2sec(pointing.len)
    except:
        pointinglenght = ''
    try:
        calibrationrecord = CalibrationSettings.objects.get(scan=scanrecord)
    except:
        calibrationrecord = ''
    try:
        otfrecord = OTFMapSettings.objects.get(scan=scanrecord)
        otfrecord.xStart = radians2sec(otfrecord.xStart)
        otfrecord.yStart = radians2sec(otfrecord.yStart)
        otfrecord.xEnd = radians2sec(otfrecord.xEnd)
        otfrecord.yEnd = radians2sec(otfrecord.yEnd)
        otfrecord.xStep = radians2sec(otfrecord.xStep)
        otfrecord.yStep = radians2sec(otfrecord.yStep)
        otfrecord.speedStart = radians2sec(otfrecord.speedStart)
        otfrecord.speedEnd = radians2sec(otfrecord.speedEnd)
    except:
        otfrecord = ''
    try:
        onoffrecord = OnOffSettings.objects.get(scan=scanrecord)
        onoffrecord.xOffset = radians2sec(onoffrecord.xOffset)
        onoffrecord.yOffset = radians2sec(onoffrecord.yOffset)

    except:
        onoffrecord = ''

    # offsets
    offsetlist = []
    for offsetrec in scanrecord.offsets.all():
        dico ={
        'xOffset':radians2sec(offsetrec.xOffset),
        'yOffset':radians2sec(offsetrec.yOffset),
        'system':offsetrec.system,
        }
        offsetlist.append(dico)

    # receivers
    receiverslist = []
    receiversrecord = Receiver.objects.filter(scan=scanrecord)

    for rx in receiversrecord:

        # frequency/linename
        try:
            heterodyne = RxReceiverCfg.objects.get(receiver=rx)
            frequency = heterodyne.frequency
            linename = heterodyne.lineName
            okheterodyne = 1
        except:
            frequency = ''
            linename = ''
            okheterodyne = 0


        # backends
        q1=Q(receiver=rx)
        q2=Q(receiver2=rx)
        backendsrecord = Backend.objects.filter(q1|q2)
        backlist = []

        for backend in backendsrecord:

            okpointing=0
            correctionAz=''
            correctionAzErr=''
            widthAz=''
            widthAzErr=''
            correctionEl=''
            correctionElErr=''
            widthEl=''
            widthElErr=''
            okfocus=0
            focus=''
            focusErr=''

            # pointing
            pointingresults = PointingResults.objects.filter(backend=backend)
            for point in pointingresults:
                if point.direction == 'azimuth':
                    correctionAz = point.correction
                    correctionAzErr = point.correctionError
                    widthAz = point.width
                    widthAzErr = point.widthError
                if point.direction == 'elevation':
                    correctionEl = point.correction
                    correctionElErr = point.correctionError
                    widthEl = point.width
                    widthElErr = point.widthError
                okpointing=1

            # focus
            focusresults = FocusResults.objects.filter(backend=backend)
            for foc in focusresults:
                focus = foc.focus
                focusErr = foc.focusError
                okfocus=1

            dico ={
            'name':backend.bkName,
            'okpointing':okpointing,
            'correctionAz':correctionAz,
            'correctionEl':correctionEl,
            'correctionAzErr':correctionAzErr,
            'correctionElErr':correctionElErr,
            'widthAz':widthAz,
            'widthEl':widthEl,
            'widthAzErr':widthAzErr,
            'widthElErr':widthElErr,
            'okfocus':okfocus,
            'focus':focus,
            'focusErr':focusErr,
            }
            backlist.append(dico)

        # calibration
        try:
            calibration = CalibrationResults.objects.get(scan=scanrecord, receiver=rx.rxName)
        except:
            calibration = ''

        # switching
        try:
            switching = FrequencySwitching.objects.get(receiver=rx)
        except:
            switching = ''
        
        dico ={
        'rxname':rx.rxName.name,
        'okheterodyne':okheterodyne,
        'frequency':frequency,
        'linename':linename,
        'backlist':backlist,
        'calibration':calibration,
        'switching':switching,
        }
        receiverslist.append(dico)

    criteriatable = criteria(request)

    dico = {
        'scanrecord':scanrecord,
        'linkfits':linkfits,
        'lst':lst,
        'duration':duration,
        'sourcerecord':sourcerecord,
        'weatherrecord':weatherrecord,
        'antennarecord':antennarecord,
        'focusrecord':focusrecord,
        'tiprecord':tiprecord,
        'pointinglenght':pointinglenght,
        'calibrationrecord':calibrationrecord,
        'otfrecord':otfrecord,
        'onoffrecord':onoffrecord,
        'offsetlist':offsetlist,
        'receiverslist':receiverslist,
        'criteriatable':criteriatable,
    }

    return render_to_response('detailscan.html', dico, context_instance=RequestContext(request))

def weather (starttime, endtime):
	
    injection_list = []
    query = """
    SELECT MIN(tau) AS mintau, MAX(tau) AS maxtau FROM WeatherTau WHERE timeStamp >= %s AND timeStamp<= %s
    """
    starttime = starttime+timedelta(minutes=-2)
    endtime = endtime+timedelta(minutes=2)

    injection_list.append(starttime)
    injection_list.append(endtime)
    cursor = connection.cursor()
    cursor.execute(query, injection_list)
    rowtau = cursor.fetchone()
    cursor.close()

    injection_list = []
    query = """
    SELECT MIN(windVel), MAX(windVelMax), MIN(humidity), MAX(humidity), MIN(pressure), MAX(pressure), MIN(temperature), MAX(temperature)
    FROM WeatherStation WHERE timeStamp >= %s AND timeStamp<= %s
    """
    injection_list.append(starttime)
    injection_list.append(endtime)
    cursor = connection.cursor()
    cursor.execute(query, injection_list)
    rowstation = cursor.fetchone()
    cursor.close()

    record ={
    'mintau':rowtau[0],
    'maxtau':rowtau[1],
    'minwind':rowstation[0],
    'maxwind':rowstation[1],
    'minhumidity':rowstation[2],
    'maxhumidity':rowstation[3],
    'minpressure':rowstation[4],
    'maxpressure':rowstation[5],
    'mintemperature':rowstation[6],
    'maxtemperature':rowstation[7],
    }
    
    return record

def scanaccess (request, scanid):

    injection_list=[scanid]
    query = """
    SELECT 
        COUNT(ncsId)
    FROM 
        Scans, Projects
    WHERE (
         Scans.project_id = Projects.id
         AND Scans.id = %s
    """
    query += datacontrol(request)
    cursor = connection.cursor()
    cursor.execute(query, injection_list)
    row = cursor.fetchone()
    cursor.close()
    granted = row[0]

    return granted
	
