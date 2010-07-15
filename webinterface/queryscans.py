from archive.sources.models import ObservedSource
from archive.webinterface.utils import *
from django.db import connection

# scans list
def scans (request, prjid, page=1, nbitems=50, order='ncsID', desc='down', kind='het', sourceid='', rxid=''):

    result_list = []
    injection_list = []
    numbercount = 0

    # orderparam control
    # kind function dependent
    paramlist = ['ncsID', 'nsubscans', 'startTime', 'endTime', 'obstype', 'tau', 'actualAz', 'actualEl', 'px', 'py', 'fz']
    if sourceid=='':
          paramlist.append('sourceName')
          paramlist.append('velocity')
          paramlist.append('rxname')
    if kind=='het':
          paramlist.append('frequency')
          paramlist.append('lineName')

    if order not in paramlist:
        query = "SELECT * FROM Scans WHERE 0"

    queryselect = """
    SELECT Scans.id, ncsID, nsubscans, startTime, endTime, stObservingModes.name as obstype, tau, actualAz, actualEl, p2, p7, focusCorrectionZ, stRxNames.name as rxname, sourceName, velocity
    """
    queryfrom = """
    FROM Scans, stObservingModes, Antenna, Secondary, Receivers, ObservedSources, stRxNames, SourceRadialVelocities, Projects
    """ 
    queryjoin = """
    WHERE   (
            Scans.observingMode_id = stObservingModes.id
            AND Scans.id = Receivers.scan_id
            AND Antenna.scan_id = Scans.id
            AND Secondary.scan_id = Scans.id
            AND ObservedSources.scan_id = Scans.id
            AND stRxNames.id = Receivers.rxName_id
            AND SourceRadialVelocities.id = ObservedSources.SourceRadialVelocity_id
            AND Scans.project_id = Projects.id
    """

    if kind=='het':
        queryselect += ", lineName, frequency"
        queryfrom += ", RxReceiversCfg"
        queryjoin += " AND RxReceiversCfg.receiver_id = Receivers.id"

    querywhere = " AND Scans.project_id = %s"
    injection_list.append(prjid)

    if kind=='bol':
        querywhere += " AND("
        for boloname in settings.RXBOLONAMES:
           querywhere += " stRxNames.name = %s OR"
           injection_list.append(boloname)
        querywhere += ")"
        querywhere = querywhere.replace(' OR)',')')
        querywhere = querywhere.replace(' AND()','')

    if sourceid!='':
        source = ObservedSource.objects.get(id=sourceid)
        querywhere += " AND ObservedSources.sourcename = %s"
        injection_list.append(source.sourceName)
    if rxid!='':
        querywhere += " AND stRxNames.id = %s"
        injection_list.append(rxid)

    # control policy
    querywhere += datacontrol(request)

    # order
    queryorder = " ORDER BY "+order
    if desc == 'up':
        queryorder += " DESC"
    if order !='SourceName':
        queryorder += ", SourceName"

    # count
    querycount = queryselect+queryfrom+queryjoin+querywhere
    
    totalcount = 0
    cursorcount = connection.cursor()
    cursorcount.execute(querycount, injection_list)
    totalcount = cursorcount.rowcount

    # pagination
    offset = int(page)*int(nbitems)
    querylimit = " LIMIT "+str(offset)+", "+str(nbitems)
    query = queryselect+queryfrom+queryjoin+querywhere+queryorder+querylimit

    nextpage = 0
    cursornext = connection.cursor()
    cursornext.execute(query, injection_list)
    if cursornext.fetchall():
        nextpage = int(page)+1

    # recordlist
    offset = (int(page)-1)*int(nbitems)
    querylimit = " LIMIT "+str(offset)+", "+str(nbitems)

    query = queryselect+queryfrom+queryjoin+querywhere+queryorder+querylimit    
    cursor = connection.cursor()
    cursor.execute(query, injection_list)

    for row in cursor.fetchall():
 
        frequency = ''
        lineName = ''
        if kind=='het':
            lineName = row[15]
            frequency = row[16]

        p2 = (180/math.pi)*float(row[9])*60*60
        p7 = (180/math.pi)*float(row[10])*60*60
        vel = float(row[14])/1000.

        record = {
        'number':numbercount,
        'id':row[0],
        'ncsID':row[1],
        'nsubscans':row[2],
        'startTime':row[3],
        'endTime':row[4],
        'obstype':row[5],
        'tau':row[6],
        'actualAz':row[7],
        'actualEl':row[8],
        'p2':p2,
        'p7':p7,
        'focusCorrectionZ':row[11],
        'rxname':row[12],
        'sourceName':row[13],
        'velocity':vel,
        'lineName':lineName,
        'frequency':frequency
        }
        result_list.append(record)
        numbercount = numbercount + 1

    cursor.close()
    cursornext.close()
    cursorcount.close()

    return result_list, totalcount, nextpage
