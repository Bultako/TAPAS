#!/usr/bin/python
"""simpleNcsMonitor.py: monitor NCS log and monitor messages
   wb 2003-09-16

   usage:
     ./simpleNcsMonitor.py logIds [host]
       logIds: logIds to receiver, can be a regular expression
       host: complete Internet name, default: mrt-lx1.iram.es

   example:
     ./simpleNcsMonitor.py hera
       get all hera messages

"""

__AUTHOR__ = "wb"
__VERSION__ = "0.1"
__DATE__ = "2003-09-16"

import elvin
import sys
import xml.sax
import string
#import myUtil

Debug = 0

def deliver(sub, msg, insec, rock):
    """process delivered messages:

    for parameters see documentation of elvin.

    Received log messages are parsed and the information is kept in
    a LogMessage object. The contents of the LogMessage object
    is printed.  
    The routine prints additional information to sys.stderr.
    """

    # print ".. msg received, params", msg, insec, rock
    for key in msg.keys():
        if Debug>1:
            print >> sys.stderr, ". %s: %s" % (key, msg.get(key)) 

    # next two lines are needed
    lm = LogMessage()
    lm.parse(str(msg.get("ncs")))
    #if Debug>1:
    #    print >> sys.stderr, myUtil.tcsTimeMS()
    # lm.dump()
    preName = string.replace(lm.attributes["LogId"],":","_")
    if Debug>1:
        print >> sys.stderr, "entryType,%s" % lm.entryType
        print >> sys.stderr, "value,%s" % lm.value
        for attr in lm.attributes.keys():
            print >> sys.stderr, "%s,%s" % (attr, lm.attributes[attr])
        for data in lm.data:
            for name in data["nameValue"].keys():
                print >> sys.stderr, "%s_%s,%s" % \
                      (preName, name, data["nameValue"][name])
        sys.stdout.flush()
    return

def firstToUpper(x):
    return string.upper(x[0]) + x[1:]

class LogMessageParser(xml.sax.ContentHandler):

    def __init__(self, parent):
        self.content = ""
        self.parent = parent
        self.parent.attributes = {}

        self.parent.data = []
        if Debug>1:
            print >> sys.stderr, \
                  ". __init__ LogMessageParser, parent:", dir(parent)

    def startElement(self, name, attrs):
        if Debug>1: print >> sys.stderr, ". startElement:", name
        if name != "Data":
            self.parent.entryType = str(name)
            for attr in attrs.keys():
                self.parent.attributes[attr] = str(attrs.getValue(attr))
        else:
            self.contentSave = self.content
            self.content = ""
            self.name = str(attrs.getValue("Name"))

    def characters(self, content):
        self.content += str(content)

    def unpack(self):
        result = {}
        try:
            if Debug>1:
                print >> sys.stderr, ". unpack:", repr(self.name),\
                      repr(self.content)
            names = string.split(self.name,",")
            values = string.split(self.content,",")
            for name in names:
                result[name] = values.pop(0)
        except:
            print >> sys.stderr, "! unpack error, length mismatch: ",\
                  repr(names), repr(values)
        if Debug>1:
            print >> sys.stderr, ". result: ", repr(result)
        return result
    
    def endElement(self, name):
        if Debug>1:
            print >> sys.stderr, ". endElement:", name
        if name != "Data":
            self.parent.value = self.content
        else:
            data = {"value": self.content,
                    "nameValue": self.unpack(),
                    "name": self.name}
            self.parent.data.append(data)
            self.content = self.contentSave
            
    def endDocument(self):
        if Debug>1:
            print >>sys.stderr, ". endDocument"

#*****
class LmAuxiliar:
    def __init__(self):
        self.entryType = ''
        self.attributes = {}
        self.data = []

class LogMessageParserMultiple(xml.sax.ContentHandler):

    def __init__(self, parent):        
        self.content = ""
        self.parent = parent
        self.parent.attributes = {}
        self.parent.messages = []              
     
        if Debug>1:
            print >> sys.stderr, \
                  ". __init__ LogMessageParser, parent:", dir(parent)

    def startElement(self, name, attrs):
        if Debug>1: print >> sys.stderr, ". startElement:", name
        
        if name == "DoubleMsg":            
            self.parent.entryType = ''
            self.parent.attributes['LogId']='Multiple'
            self.intoMsg = 0
            
        elif name != "Data": #Info, Notice, Warning...      
            self.intoMsg = 1
            self.temp = LmAuxiliar()
            self.temp.entryType=str(name)
            
            for attr in attrs.keys():
                self.temp.attributes[attr] = str(attrs.getValue(attr))            
                
        else:            
            self.contentSave = self.content
            self.content = ""
            self.name = str(attrs.getValue("Name"))

    def characters(self, content):
        if self.intoMsg:
            self.content += str(content)

    def unpack(self):
        result = {}
        try:
            if Debug>1:
                print >> sys.stderr, ". unpack:", repr(self.name),\
                      repr(self.content)
            names = string.split(self.name,",")
            values = string.split(self.content,",")
            for name in names:
                result[name] = values.pop(0)
        except:
            print >> sys.stderr, "! unpack error, length mismatch: ",\
                  repr(names), repr(values)
        if Debug>1:
            print >> sys.stderr, ". result: ", repr(result)
        return result
    
    def endElement(self, name):
        if Debug>1:
            print >> sys.stderr, ". endElement:", name
            
        if name == "DoubleMsg":
            pass
            
        elif name != "Data":
            self.temp.value = self.content
            self.parent.messages.append(self.temp)            
            self.intoMsg = 0
            
        else:
            data = {"value": self.content,
                    "nameValue": self.unpack(),
                    "name": self.name}
            self.temp.data.append(data)
            self.content = self.contentSave
            
    def endDocument(self):
        if Debug>1:
            print >>sys.stderr, ". endDocument"

class LogMessage:

    def dump(self):
        for key in self.__dict__.keys():
            print key, ":\t", self.__dict__[key]
            
    def parse(self, message=""):
        """Parses a log message and produces:
        (in () results of message:
         <Info LogId='a'>abc<Data Name='n1,n2'>d1,d2</Data></Info>)
        self.entryType: top tag ('Info')
        self.content: content of top tag ('abc')
        self.attributes: attributes of top tag ({'LogId':'a'})
        self.data: a list of dictionaries, one per data-tag, with entries
          content: content of data tag ('d1,d2')
          name: value of Name atribute ('n1,n2')
          nameValue: a dictionary name:data ({'n1':'d1', 'n2':'d2'})
        """
        
        if Debug>0:
            print >> sys.stderr, ". LogMessage.parse:", message
        parser = LogMessageParser(self)
        
        try:            
            xml.sax.parseString(message, parser)
        except:
            #We try again, maybe the line are two messages, not an parse error
            message = '<DoubleMsg>'+message+'</DoubleMsg>'
            if Debug>0:
                print >> sys.stderr, ". LogMessage.parse:", message
            new_parser = LogMessageParserMultiple(self)
            xml.sax.parseString(message, new_parser)
        
class SimpleNcsMonitor:
    
    def __init__(self,host="mrt-lx1.iram.es",
                 require=['ncs'], regex=['""'],
                 filter = "",
                 callback=deliver):
        if filter == "":
            oper = ''
            for req in require:
                filter = filter + " %s require(%s)"%(oper,req)
                oper = "&&"
            for expression in regex:
                filter = filter + " && regex(%s)"%expression
                oper = "&&"
        if Debug>1:
            print >> sys.stderr, \
                  "SimpleNcsMonitor for %s from %s: call %s" % \
                  (filter, host, repr(callback))
        self.client(host=host ,filter=filter, callback=callback)

    def client(self, host="mrt-lx1.iram.es", filter='require(ncs)',
               callback = deliver):
        if Debug>0:
            print >> sys.stderr, ".. connecting to ", host, ":",
        con = elvin.connect("elvin://" + host)
        if Debug>0:
            print >> sys.stderr, ".. connected"
        sub = con.subscribe(filter)
        sub.add_listener(callback)
        sub.register()
        con.run()

def usage():
    print __doc__
    sys.exit(0)
    
if __name__=="__main__":

    if len(sys.argv) <=1 :
        usage()
    if len(sys.argv) > 1:
        logId = sys.argv[1]
    if len(sys.argv) > 2:
        host = sys.argv[2]
    else:
        host="mrt-lx1.iram.es"
        
    filter='require(ncs) && regex(LogId,"'+logId+'")'
    printUsage = "y"
    
    if 1==1:
        SimpleNcsMonitor(host=host, filter=filter)
        printUsage = "n"
    else:
        if printUsage != "n":
            usage()
        
