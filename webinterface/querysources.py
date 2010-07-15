from archive.webinterface.models import *
from archive.webinterface.utils import *
from django.conf import settings
from django.db import connection
from archive.webinterface.Sesame import Sesame
import re

# sources list
def sources (request, page=1, nbitems=50, order='SourceName', desc='down',  prjid=''):

    result_list = []
    injection_list = []
    numbercount = 0

    # orderparam control
    paramlist = ['SourceName', 'velocity', 'cscans', 'lambda', 'projectID', 'rxname', 'avgtau', 'mintime', 'maxtime']
    if order not in paramlist:
        query = "SELECT * FROM Scans WHERE 0"

    queryselect = """
    SELECT 
    SourceName, lambda, beta, name as rxname, count(Scans.id) as cscans, min(startTime) as mintime, max(endTime) as maxtime, AVG(tau) as avgtau, velocity, projectID, title, ObservedSources.id as sourceid, rxName_id as rxid, Projects.id as prjid
    """
    queryfrom = """
    FROM
    stRxNames, Receivers, Scans, Projects, ObservedSources, SourceRadialVelocities
    """
    queryjoin = """
    WHERE   (
            SourceRadialVelocities.id = ObservedSources.SourceRadialVelocity_id
            AND ObservedSources.scan_id = Scans.id
            AND Scans.project_id = Projects.id
            AND Scans.id = Receivers.scan_id
            AND stRxNames.id = Receivers.rxName_id
    """
    querywhere = ""

    if prjid == '':
        
        searchrecord = SourceSearch.objects.get(session_id=request.COOKIES['sessionid'])

        if searchrecord.source_name:
            if searchrecord.resolver == 1:
                querywhere += " AND ObservedSources.sourceName = %s"
                injection_list.append(searchrecord.source_name)
            else:
            # sesame resolver
            #
                try:
                    sesame = Sesame()
                    ra, dec = sesame.resolve(searchrecord.source_name)
                    rarad = ra*math.pi/180.
                    decrad = dec*math.pi/180.
                    sizerad=size2radians(settings.RESANGSIZE)
                    lambdamin = rarad-sizerad
                    betamin = decrad-sizerad
                    lambdamax = rarad+sizerad
                    betamax = decrad+sizerad

                    ANDOR = "AND"
                    if lambdamin<0:
                        lambdamin = lambdamin + 2*math.pi
                        ANDOR = "OR"
                    if lambdamax>2*math.pi:
                        lambdamax = lambdamax - 2*math.pi
                        ANDOR = "OR"

                    querywhere += " AND (ObservedSources.lambda >= %s "+ANDOR+" ObservedSources.lambda <= %s)"
                    injection_list.append(lambdamin)
                    injection_list.append(lambdamax)
                    querywhere += " AND (ObservedSources.beta >= %s AND ObservedSources.beta <= %s)"
                    injection_list.append(betamin)
                    injection_list.append(betamax)
                except:
                    querywhere += " AND ObservedSources.sourceName = '0000000000'"


        if searchrecord.ra:
            rarad=ra2radians(searchrecord.ra)
            decrad=dec2radians(searchrecord.dec)
            sizerad=size2radians(searchrecord.size)
            lambdamin = rarad-sizerad
            betamin = decrad-sizerad
            lambdamax = rarad+sizerad
            betamax = decrad+sizerad

            ANDOR = "AND"
            if lambdamin<0:
                lambdamin = lambdamin + 2*math.pi
                ANDOR = "OR"
            if lambdamax>2*math.pi:
                lambdamax = lambdamax - 2*math.pi
                ANDOR = "OR"

            querywhere += " AND (ObservedSources.lambda >= %s "+ANDOR+" ObservedSources.lambda <= %s)"
            injection_list.append(lambdamin)
            injection_list.append(lambdamax)
            querywhere += " AND (ObservedSources.beta >= %s AND ObservedSources.beta <= %s)"
            injection_list.append(betamin)
            injection_list.append(betamax)

        if searchrecord.opacity !='' and searchrecord.opacity:
            querywhere += " AND Scans.tau < %s"
            injection_list.append(searchrecord.opacity)

        if searchrecord.project_id:
            querywhere += " AND Projects.projectID = %s"
            injection_list.append(searchrecord.project_id)

        if searchrecord.date_from:
            querywhere += """
            AND Scans.startTime >= %s
            AND Scans.endTime <= %s
            """
            searchrecord.date_to = searchrecord.date_to + timedelta(1)
            injection_list.append(searchrecord.date_from)
            injection_list.append(searchrecord.date_to)

        sql = """
        SELECT 
            strxnames_id
        FROM 
            SourceSearch_has_Receivers, SourceSearch_Receivers_Rx
        WHERE
            SourceSearch_has_Receivers.SourceSearch_Receivers_id = SourceSearch_Receivers_Rx.SourceSearch_Receivers_id
            AND SourceSearch_has_Receivers.SourceSearch_id = """+str(searchrecord.id)
        cursor = connection.cursor()
        cursor.execute(sql)
        intraquery = " AND ("
        for row in cursor.fetchall():
            intraquery += "stRxNames.id = %s OR "
            injection_list.append(row[0])
        intraquery += ")"
        intraquery = intraquery.replace(' OR )',')')
        intraquery = intraquery.replace('AND ()','')
        querywhere += intraquery
        cursor.close()

        if searchrecord.frequency_from or searchrecord.line_name:
            queryfrom += ", RxReceiversCfg"
            queryjoin += " AND RxReceiversCfg.Receiver_id = Receivers.id"

        if searchrecord.frequency_from !='' and searchrecord.frequency_from:
            querywhere += " AND RxReceiversCfg.frequency >=%s AND RxReceiversCfg.frequency <=%s"
            injection_list.append(searchrecord.frequency_from)
            injection_list.append(searchrecord.frequency_to)

        # linename
        if searchrecord.line_name:
            
            if searchrecord.exact_line>0:
                querywhere += """
                AND RxReceiversCfg.lineName = %s
                """
                injection_list.append(searchrecord.line_name)
            else:
                querywhere += """
                AND (RxReceiversCfg.lineName LIKE %s
                OR RxReceiversCfg.lineName LIKE %s
                OR RxReceiversCfg.lineName LIKE %s
                )
                """
                linestart = searchrecord.line_name+"%"
                linemiddle = "%"+searchrecord.line_name+"%"
                lineend = "%"+searchrecord.line_name
                injection_list.append(linestart)
                injection_list.append(linemiddle)
                injection_list.append(lineend)

        if searchrecord.velocity_from !='' and searchrecord.velocity_from:
            querywhere += " AND SourceRadialVelocities.velocity >=%s AND SourceRadialVelocities.velocity <=%s"
            velocity_from_km = int(searchrecord.velocity_from)*1000
            velocity_to_km = int(searchrecord.velocity_to)*1000
            injection_list.append(velocity_from_km)
            injection_list.append(velocity_to_km)

    else:

        querywhere = " AND Projects.id = %s"
        injection_list.append(prjid)

    # control policy
    querywhere += datacontrol(request)

    querygroup = """
    GROUP BY SourceName, rxname, projectID
    """

    # order
    queryorder = " ORDER BY "+order
    if desc == 'up':
        queryorder += " DESC"
    if order !='SourceName':
        queryorder += ", SourceName"


    # count
    querycount = queryselect+queryfrom+queryjoin+querywhere+querygroup
    
    totalcount = 0
    cursorcount = connection.cursor()
    cursorcount.execute(querycount, injection_list)
    totalcount = cursorcount.rowcount

    # pagination
    offset = int(page)*int(nbitems)
    querylimit = " LIMIT "+str(offset)+", "+str(nbitems)
    query = queryselect+queryfrom+queryjoin+querywhere+querygroup+queryorder+querylimit

    nextpage = 0
    cursornext = connection.cursor()
    cursornext.execute(query, injection_list)
    if cursornext.fetchall():
        nextpage = int(page)+1

    # recordlist
    offset = (int(page)-1)*int(nbitems)
    querylimit = " LIMIT "+str(offset)+", "+str(nbitems)
    query = queryselect+queryfrom+queryjoin+querywhere+querygroup+queryorder+querylimit

    cursor = connection.cursor()
    cursor.execute(query, injection_list)

    for row in cursor.fetchall():

        try:
            ra=radians2ra(row[1])
        except:
            ra = ''
        try:
            dec=radians2dec(row[2])
        except:
            dec = ''

        kind='bol'
        if row[3] not in settings.RXBOLONAMES:
            kind='het'
        
        record = {
        'number':numbercount,
        'SourceName':row[0],
        'lambda':ra,
        'beta':dec,
        'rxname':row[3],
        'cscans':row[4],
        'mintime':row[5],
        'maxtime':row[6],
        'avgtau':row[7],
        'velocity':row[8]/1000.,
        'projectID':row[9],
        'title':row[10],
        'sourceid':row[11],
        'rxid':row[12],
        'prjid':row[13],
        'kind':kind
        }
        result_list.append(record)
        numbercount = numbercount+1

    cursor.close()
    cursornext.close()
    cursorcount.close()
    
    return result_list, totalcount, nextpage

# sources list from batch file
def batchfilesearch (request, batchfile):

    uniques_list = []
    result_list = []
    totalcount = 0

    queryselect = """
    SELECT 
    SourceName, lambda, beta, name as rxname, count(Scans.id) as cscans, min(startTime) as mintime, max(endTime) as maxtime, AVG(tau) as avgtau, velocity, projectID, title, ObservedSources.id as sourceid, rxName_id as rxid, Projects.id as prjid
    """
    queryfrom = """
    FROM
    stRxNames, Receivers, Scans, Projects, ObservedSources, SourceRadialVelocities
    """
    queryjoin = """
    WHERE   (
            SourceRadialVelocities.id = ObservedSources.SourceRadialVelocity_id
            AND ObservedSources.scan_id = Scans.id
            AND Scans.project_id = Projects.id
            AND Scans.id = Receivers.scan_id
            AND stRxNames.id = Receivers.rxName_id
    """

    # control policy
    querypolicy = datacontrol(request)

    querygroup = """
    GROUP BY SourceName, rxname, projectID
    """

    cursor = connection.cursor()
    separator = re.compile(r'\|')

    for line in batchfile:

        querywhere = ''
        injection_list = []
        stripline = line.strip()

        mRADEC = re.match("^([0-9]{2}:[0-9]{2}:[0-9]{2}\.?([0-9]+)?)\s+(\-?[0-9]{2}:[0-9]{2}:[0-9]{2}\.?([0-9]+)?)$", line)

        # search by ra/dec 
        if mRADEC:
            try: 
                rarad=ra2radians(mRADEC.group(1))
                decrad=dec2radians(mRADEC.group(3))
                sizerad=size2radians(settings.ANGSIZE)
                lambdamin = rarad-sizerad
                betamin = decrad-sizerad
                lambdamax = rarad+sizerad
                betamax = decrad+sizerad

                ANDOR = "AND"
                if lambdamin<0:
                    lambdamin = lambdamin + 2*math.pi
                    ANDOR = "OR"
                if lambdamax>2*math.pi:
                    lambdamax = lambdamax - 2*math.pi
                    ANDOR = "OR"

                querywhere += " AND (ObservedSources.lambda >= %s "+ANDOR+" ObservedSources.lambda <= %s)"
                injection_list.append(lambdamin)
                injection_list.append(lambdamax)
                querywhere += " AND (ObservedSources.beta >= %s AND ObservedSources.beta <= %s)"
                injection_list.append(betamin)
                injection_list.append(betamax)
            except:
                continue

        # search by name
        else:
            mIRAM = re.match("^\*(.*)\*$", line)
            if mIRAM:
                source_name = mIRAM.group(1)
                querywhere += " AND ObservedSources.sourceName = %s"
                injection_list.append(source_name)
                    
            else:
                # simbad/name resolver
                try:
                    sesame = Sesame()
                    ra, dec = sesame.resolve(line)
                    rarad = ra*math.pi/180.
                    decrad = dec*math.pi/180.
                    sizerad=size2radians(settings.RESANGSIZE)
                    lambdamin = rarad-sizerad
                    betamin = decrad-sizerad
                    lambdamax = rarad+sizerad
                    betamax = decrad+sizerad

                    ANDOR = "AND"
                    if lambdamin<0:
                        lambdamin = lambdamin + 2*math.pi
                        ANDOR = "OR"
                    if lambdamax>2*math.pi:
                        lambdamax = lambdamax - 2*math.pi
                        ANDOR = "OR"

                    querywhere += " AND (ObservedSources.lambda >= %s "+ANDOR+" ObservedSources.lambda <= %s)"
                    injection_list.append(lambdamin)
                    injection_list.append(lambdamax)
                    querywhere += " AND (ObservedSources.beta >= %s AND ObservedSources.beta <= %s)"
                    injection_list.append(betamin)
                    injection_list.append(betamax)
                except:
                    continue

        
    	if querywhere:
            
            query = queryselect+queryfrom+queryjoin+querywhere+querypolicy+querygroup

            try:
                cursor.execute(query, injection_list)
                for row in cursor.fetchall():

                    try:
                        ra=radians2ra(row[1])
                    except:
                        ra=row[1]
                    try:
                        dec=radians2dec(row[2])
                    except:
                        dec=row[2]

                    kind='bol'
                    if row[3] not in settings.RXBOLONAMES:
                        kind='het'
                    
                    record = {
                    'number':totalcount,
                    'SourceName':row[0],
                    'lambda':ra,
                    'beta':dec,
                    'rxname':row[3],
                    'cscans':row[4],
                    'mintime':row[5],
                    'maxtime':row[6],
                    'avgtau':row[7],
                    'velocity':row[8]/1000.,
                    'projectID':row[9],
                    'title':row[10],
                    'sourceid':row[11],
                    'rxid':row[12],
                    'prjid':row[13],
                    'kind':kind
                    }

                    uniquerecord = str(row[0])+"_"+str(row[9])+"_"+str(row[3])
                    if uniquerecord not in uniques_list:
                       uniques_list.append(uniquerecord)
                       result_list.append(record)
                       totalcount = totalcount+1
            except:
                continue

    cursor.close()
    return result_list, totalcount
