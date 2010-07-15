from django.contrib import auth
from django.http import HttpResponseRedirect
from archive.webinterface.models import SourceSearch
from archive.datafiller.models import MetadataAttribute
from django.conf import settings
from datetime import date, timedelta
from archive.scans.models import Scan
import math, string

# authentication
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    return HttpResponseRedirect("/tapas/")

def logout(request):
    response = HttpResponseRedirect("/tapas/")
    auth.logout(request)
    return response

# data access control
def datacontrol(request):

    limit = settings.DAYSDATACCESS
    datelimit = date.today() + timedelta(limit)

    sqltime = ""
    sqlproject = ""

    if not request.user.is_staff:
        sqltime = " Scans.startTime < '"+datelimit.strftime("%Y/%m/%d")+"'"
        if request.user.is_active:        
            sqlproject = " OR Projects.PI_id = "+str(request.user.id)
    
    sql = ") AND ("+sqltime+sqlproject+")"
    sql = sql.replace(' AND ()','')
    
    return sql

# FITS access control
def fitscontrol(request, scanid):

    accessFITS = 0
    own_project=0      
    oktime = 0

    limit = settings.DAYSFITACCESS
    datelimit = date.today() + timedelta(limit)

    scan = Scan.objects.get(id=scanid)

    # own project
    try:
        PI_id = scan.project.pi.id
        if PI_id == request.user.id:
            own_project=1
    except:
        own_project=0 

    #
    # get fits link
    # to be done 
    #

    linkfits = "#"

    # rules
    if request.user.is_staff or own_project:
        accessFITS = linkfits

    if scan.project.is_LKP and scan.endTime<datelimit:
        accessFITS = linkfits

    if accessFITS:
        # create symbolic link
        # to be done
        #

        pass
    

    return accessFITS

# cookie control
def cookiecontrol(request):
    if not 'sessionid' in request.COOKIES:
        return 'Please, enable cookies in your browser in order to perform a search.'
    else:
        return ''

# file format control
# no more than 1500 lines
def fileformatcontrol(batchfile):

    ok = ''
    if batchfile.size>150000:
         ok = 'Batchfile may contain no more than 1500 lines.'
   
    lines = 0
    for line in batchfile:
        lines = lines+1   	    
    if lines > 1500:
        ok = 'Batchfile may contain no more than 1500 lines.'
    
    return ok

# coordinates conversion
def ra2radians(ra):

    arr=string.split(ra, ":")
    hh=float(arr[0])*15
    mm=(float(arr[1])/60.)*15
    ss=(float(arr[2])/3600.)*15

    deg = hh+mm+ss
    rad=deg*2*math.pi/360.
    return rad

def radians2ra(rad):

    deg=(180/math.pi)*float(rad)
    if deg < 0:
        deg=deg+360
    if deg > 360:
        deg=deg-360
    
    hh=int(deg/15.)
    mm=int((deg-15*hh)*4)
    ss=int((4*deg-60*hh-mm)*60)

    if len(str(hh))<2:
        hh="0"+str(hh)
    if len(str(mm))<2:
        mm="0"+str(mm)
    if len(str(ss))<2:
        ss="0"+str(ss)
       
    ra=str(hh)+":"+str(mm)+":"+str(ss)
    return ra

def dec2radians(dec):

    arr=string.split(dec, ":")
    hh=float(arr[0])
    mm=float(arr[1])/60.
    ss=float(arr[2])/3600.

    if dec.startswith('-'):
        deg=hh-mm-ss
    else:
        deg=hh+mm+ss

    rad=deg*2*math.pi/360.

    return rad

def radians2dec(rad):

    deg=(180/math.pi)*float(rad)
    if deg > 360:
        deg=deg-360

    hh=int(deg)
    absdeg=abs(deg)
    mm=int((absdeg-int(absdeg))*60)
    ss=int(((absdeg-int(absdeg))*60-mm)*60)
  
    strhh=str(abs(hh))
    if len(strhh)<2:
        strhh="0"+strhh
    if rad<0:
        strhh="-"+strhh
    if len(str(mm))<2:
        mm="0"+str(mm)
    if len(str(ss))<2:
        ss="0"+str(ss)
    
    dec=str(strhh)+":"+str(mm)+":"+str(ss)
    return dec

def size2radians(radius):

    rad=radius*2*math.pi/360.
    return rad

def lst2time(lst):

    tim=float(lst)
    hh=int(tim/3600.)
    mm=int((tim/3600.-hh)*60)
    ss=int((((tim/3600.-hh)*60)-mm)*60)
    
    strhh = str(hh)
    strmm = str(mm)
    strss = str(ss)

    if len(strhh)<2:
        strhh="0"+str(hh)
    if len(strmm)<2:
        strmm="0"+str(mm)
    if len(strss)<2:
        strss="0"+str(ss)

    timelst = strhh+":"+strmm+":"+strss
    return timelst

def radians2sec(rad):

    deg=(180/math.pi)*float(rad)
    if deg > 360:
        deg=deg-360

    sec = deg*3600
    return sec

# search criteria reminder
def criteria(request):

    if not 'sessionid' in request.COOKIES:
        return ''
    else:
        try:
            resolver = {1:'IRAM Name', 2:'SIMBAD/NED Name'}
            matchline = {0:'Including', 1:'Exact'}

            searchcriteria = SourceSearch.objects.get(session_id=request.COOKIES['sessionid'])
            searchcriteria.resolvername = resolver[searchcriteria.resolver]
            searchcriteria.matchline = matchline[searchcriteria.exact_line]

            return searchcriteria
        except:
            return ''


# votable ucd and descriptors
def votable():
	
    dico = {
        'sourcename':MetadataAttribute.objects.get(attributeName='sourceName',metadataEntity__name='ObservedSource'),
        'velocity':MetadataAttribute.objects.get(attributeName='velocity',metadataEntity__name='SourceRadialVelocity'),
        'lambdaField':MetadataAttribute.objects.get(attributeName='lambdaField',metadataEntity__name='ObservedSource'),
        'beta':MetadataAttribute.objects.get(attributeName='beta',metadataEntity__name='ObservedSource'),
        'rxName':MetadataAttribute.objects.get(attributeName='rxName',metadataEntity__name='Receiver'),
        'tau':MetadataAttribute.objects.get(attributeName='tau',metadataEntity__name='Scan'),
        'startTime':MetadataAttribute.objects.get(attributeName='startTime',metadataEntity__name='Scan'),
        'endTime':MetadataAttribute.objects.get(attributeName='endTime',metadataEntity__name='Scan'),
        'ncsId':MetadataAttribute.objects.get(attributeName='ncsId',metadataEntity__name='Scan'),
        'frequency':MetadataAttribute.objects.get(attributeName='frequency',metadataEntity__name='RxReceiverCfg'),
        'lineName':MetadataAttribute.objects.get(attributeName='lineName',metadataEntity__name='RxReceiverCfg'),
        'actualAz':MetadataAttribute.objects.get(attributeName='actualAz',metadataEntity__name='Antenna'),
        'actualEl':MetadataAttribute.objects.get(attributeName='actualEl',metadataEntity__name='Antenna'),
        'p2':MetadataAttribute.objects.get(attributeName='p2',metadataEntity__name='Antenna'),
        'p7':MetadataAttribute.objects.get(attributeName='p7',metadataEntity__name='Antenna'),
        'focusCorrectionZ':MetadataAttribute.objects.get(attributeName='focusCorrectionZ',metadataEntity__name='Secondary'),
    }

    return dico
