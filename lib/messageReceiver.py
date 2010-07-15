#!/usr/bin/env python

"""
"""

#IMPORTS 
import time
import sys
import string
import fcntl
import elvin
from simpleNcsMonitor2 import LogMessage

#SET Debug TO 0 - vem
Debug = 0

if Debug>1: print sys.path

######################################################################################
class ElvinReceiver:
    "This class only receive data from an Elvin host. It does not parse the data or do anything with it, simply receive"
    #Main methods

    def __init__(self,host='mrt-lx1',require=''):
        """Initialize the messageReceiver class. It takes 3 arguments, 
        the elvin host, the deliver function and the require string to filter messages"""
        
        self.elvinHost=host
        
        connectTo = "elvin://%s" % self.elvinHost
        
        self.con = elvin.connect(connectTo)
        
        subscription = 'require(ncs)'
        self.require=require
        if self.require:
            subscription += ' && regex(LogId,"'+self.require+'")'
        if Debug>0: print ". subscription:", subscription
        sub = self.con.subscribe(subscription)
    
        sub.add_listener(self.deliverMsg)
        sub.register()
        
        print 'reading from Elvin, host: '+self.elvinHost

    def deliverMsg(self, sub, msg, insec, rock):
        "Callback to get a message from an elvin host."

        if Debug>0:
            print >> sys.stderr, ".. msg received***", msg

        line=str(msg.get("ncs"))        
	if 1==1:
        #try:
             self.parseMsg(line)
        #except:
        #    print "error self.parseMsg: %s ..." % line[:80]
            
    def parseMsg(self,line):
        "Overrides this to add functionality"
        print >> sys.stderr, ". received:", line
            
    def getMessagesElvin(self):
        """Main loop to get messages from elvin. It starts to get from elvin,
        and the callback parses and views all the messages read""" 
        self.con.run()

class MessageReceiverParser(ElvinReceiver):
    """This class inherits the elvinReceiver to add the functionality of parse the messages received,
    and transform them to LogMessage class"""
    
    def getDictValue(self, dict, key, default):
        """Returns the key from a dict. If the key doesn't exists,
        returns the default value pass"""
        
        if dict.has_key(key):
            return dict[key]
        else:
            return default
    
    def parseMsg(self,line):
        """Override the elvinReceiver.parseMsg method, to allow parse the lines received into a Log message"""
        try:
            lm = self.parseLoglineAux(line)
        except 'ParseError':
            print >> sys.stderr, ". invalid ncs message:", line
            pass
        
        logId = self.getDictValue(lm.attributes,"LogId","unknown")
        self.processMsg(logId,lm)
            
    def parseLoglineAux(self,line):
        """Aux method: Parses a line read"""

        subLine = line[string.find(line,"<"):]
        self.line = subLine
        
        lm = LogMessage()
        try:
            lm.parse(subLine)
            logId = self.getDictValue(lm.attributes,"LogId","unknown")
            timeStamp = self.getDictValue(lm.attributes,"TimeStamp","no time")
            if Debug>1: print ". logId: %s" % logId
            if Debug>1: lm.dump()
        except:
            print >> sys.stderr, ". parse error for: ", subLine
            raise 'ParseError'

        return lm
    
    def processMsg(self,logId,lm):
        """This method allow to work with the log message parsered. Override it
        to add functionality"""
        pass

######################################################################################
class TkElvinReceiver:
    "This class only receive data from an Elvin host. It does not parse the data or do anything with it, simply receive"
    #Main methods

    def __init__(self,root, host='mrt-lx1',require=''):
        """Initialize the messageReceiver class. It takes 3 arguments, 
        the elvin host, the deliver function and the require string to filter messages"""
        
        self.elvinHost=host

        # self.client = elvin.client(loop)
        connectTo = "elvin://%s" % self.elvinHost
        self.client = elvin.client(elvin.TkLoop,root)
        self.con = self.client.connection()
        self.con.set_discovery(0)
        self.con.append_url(connectTo)
        self.con.set_request_timeout(3.0)
        self.con.set_max_retries(5)        
        
        
        self.subscription = 'require(ncs)'
        self.require=require
        if self.require:
            self.subscription += ' && regex(LogId,"'+self.require+'")'
        if Debug>0: print ". subscription:", subscription
        
        self.con.open(self.openConnection)
                
    def sub_add_cb(self, sub, error, sub_id, rock):
        pass
    
    def openConnection(self,connection,error,rock):
        sub = self.con.subscribe(self.subscription)
        sub.add_listener(self.deliverMsg, self.con)
        sub.register(self.sub_add_cb,self.con)
        print 'reading from Elvin, host: '+self.elvinHost

    def deliverMsg(self, sub, msg, insec, rock):
        "Callback to get a message from an elvin host."

        if Debug>0:
            print >> sys.stderr, ".. msg received***", msg

        line=str(msg.get("ncs"))        
        print line
        try:
            self.parseMsg(line)
        except:
            print "error TkElvinReceiver.parseMsg: %s ..." % line[:80]
            
    def parseMsg(self,line):
        "Overrides this to add functionality"
        print >> sys.stderr, ". received:", line
            
#    def getMessagesElvin(self):
#        """Main loop to get messages from elvin. It starts to get from elvin,
#        and the callback parses and views all the messages read""" 
#        self.con.run()
           
######################################################################################
class TkMessageReceiverParser(TkElvinReceiver):
    """This class inherits the elvinReceiver to add the functionality of parse the messages received,
    and transform them to LogMessage class"""
    
    def getDictValue(self, dict, key, default):
        """Returns the key from a dict. If the key doesn't exists,
        returns the default value pass"""
        
        if dict.has_key(key):
            return dict[key]
        else:
            return default
    
    def parseMsg(self,line):
        """Override the elvinReceiver.parseMsg method, to allow parse the lines received into a Log message"""
        try:
            lm = self.parseLoglineAux(line)
        except 'ParseError':
            print >> sys.stderr, ". invalid ncs message:", line
            pass
        
        logId = self.getDictValue(lm.attributes,"LogId","unknown")
        self.processMsg(logId,lm)
            
    def parseLoglineAux(self,line):
        """Aux method: Parses a line read"""

        subLine = line[string.find(line,"<"):]
        self.line = subLine
        
        lm = LogMessage()
        try:
            lm.parse(subLine)
            logId = self.getDictValue(lm.attributes,"LogId","unknown")
            timeStamp = self.getDictValue(lm.attributes,"TimeStamp","no time")
            if Debug>1: print ". logId: %s" % logId
            if Debug>1: lm.dump()
        except:
            print >> sys.stderr, ". parse error for: ", subLine
            raise 'ParseError'

        return lm
    
    def processMsg(self,logId,lm):
        """This method allow to work with the log message parsered. Override it
        to add functionality"""
        pass
    
######################################################################################
class MessageReaderSimple:
    """This class only read messages from an input stream (maybe a pipe, a file, the standard input...)
    and parses them to logMessage class, allowing to work with them"""
    
    #Main methods
    def __init__(self, input=''):
        """Open the stream to read"""        
        if input == 'sys.stdin' or input == 'stdin':
            self.input = sys.stdin
        else:
            try:
                self.input = open(input,'r')        
            except:
                print >> sys.stderr, 'Error opening input stream'
                sys.exit(0)  
        
        print 'reading from '+input
        
    def getDictValue(self, dict, key, default):
        """Returns the key from a dict. If the key doesn't exists,
        returns the default value pass"""
        
        if dict.has_key(key):
            return dict[key]
        else:
            return default            

    def parseLogline(self,line):
        """Parses a line read from the input choosen and returns a logMessage class"""
    
        subLine = line[string.find(line,"<"):]
        subLine = subLine[:string.rfind(subLine,">")+1]
        
        lm = LogMessage()
        try:
            lm.parse(subLine)
            logId = self.getDictValue(lm.attributes,"LogId","unknown")
            timeStamp = self.getDictValue(lm.attributes,"TimeStamp","no time")
            if Debug>1: print ". logId: %s" % logId
            if Debug>1: lm.dump()
        except:
            print ". parse error for: ", subLine
            raise 'ParseError'
    
        return lm

    def getMessages(self):
        """Main function to get messages. It parses and process all the messages read.
        This class supports multiple messages in only one line, due to the pipe effect."""

        printed=0
        while 1:            
            if Debug>1 and printed==0:
                print '. waiting for input'
                printed = 1

            line=self.input.readline()
            if not line: continue
            
            try:
                lm = self.parseLogline(line)
            except 'ParseError':
                print ". invalid ncs message:",line
                #line = self.input.readline()
                continue

            logId = self.getDictValue(lm.attributes,"LogId","unknown")
            
            if logId == 'Multiple':
                for logmsg in lm.messages:
                    logIdMsg = self.getDictValue(logmsg.attributes,"LogId","unknown")
                    self.processMsg(logIdMsg,logmsg)                    
            else:
                self.processMsg(logId,lm)
        
    def processMsg(self,logId,lm):
        """This method allow to work with the log message parsered. Override it
        to add functionality"""
        print logId
        #pass
        
############################################################################

if __name__ == "__main__":
    import Tkinter
    tk = Tkinter.Tk()
    widget = Tkinter.Label(tk,text="No message")
    widget.pack()
    
    test = TkElvinReceiver(tk, host='mrt-lx1')
    widget.mainloop()
    #test.getMessagesElvin();
