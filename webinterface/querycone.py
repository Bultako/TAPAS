from archive.webinterface.models import *
from archive.webinterface.utils import *
from archive.receivers.models import *
from archive.scans.models import Project, Scan
from django.db import connection

# conesearch sources list
def cone (request):

    result_list = []
    injection_list = []
    totalcount = 0
    
    queryselect = """
    SELECT 
    ObservedSources.id, SourceName, lambda, beta, velocity, count(Scans.id) as cscans, AVG(tau) as avgtau, min(startTime) as mintime, max(endTime) as maxtime
    """
    queryfrom = """
    FROM
    Scans, ObservedSources, SourceRadialVelocities
    """
    queryjoin = """
    WHERE   (
            SourceRadialVelocities.id = ObservedSources.SourceRadialVelocity_id
            AND ObservedSources.scan_id = Scans.id
    """
    
    ra = float(request.GET['RA'])
    radRA = ra*math.pi/180.
    dec = float(request.GET['DEC'])
    radDEC = dec*math.pi/180.
    radius = float(request.GET['SR'])
    radSR = radius*math.pi/180.

    lambdamin = radRA-radSR
    betamin = radDEC-radSR
    lambdamax = radRA+radSR
    betamax = radDEC+radSR

    ANDOR = "AND"
    if lambdamin<0:
        lambdamin = lambdamin + 2*math.pi
        ANDOR = "OR"
    if lambdamax>2*math.pi:
        lambdamax = lambdamax - 2*math.pi
        ANDOR = "OR"

    querywhere = " AND (ObservedSources.lambda >= %s "+ANDOR+" ObservedSources.lambda <= %s)"
    injection_list.append(lambdamin)
    injection_list.append(lambdamax)
    querywhere += " AND (ObservedSources.beta >= %s AND ObservedSources.beta <= %s)"
    injection_list.append(betamin)
    injection_list.append(betamax)

    # control policy
    querywhere += datacontrol(request)

    querygroup = """
    GROUP BY SourceName
    """

    # recordlist
    query = queryselect+queryfrom+queryjoin+querywhere+querygroup

    cursor = connection.cursor()
    cursor.execute(query, injection_list)
    totalcount = cursor.rowcount

    for row in cursor.fetchall():

        ra=(180./math.pi)*float(row[2])
        dec=(180./math.pi)*float(row[3])

        record = {
        'sourceid':row[0],
        'SourceName':row[1],
        'ra':ra,
        'dec':dec,
        'velocity':row[4]/1000.,
        'cscans':row[5],
        'avgtau':row[6],
        'mintime':row[7],
        'maxtime':row[8],
        }
        result_list.append(record)

    cursor.close()
    return result_list, totalcount
