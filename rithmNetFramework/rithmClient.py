import socket
import sys, getopt

class RiTHMCliException(Exception):
    def __init__(self, arg):
        self.arg = arg
        
class RiTHMCli:
    
    def __init__(self):
        self.isSpecSet=False
        self.isOutputSet=False
        self.isTraceSet=False
        self.sock=None
        self.cmdOut=''
    def connectServer(self,ip,port): 
        self.ip=ip
        self.port=port   
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port)) 
        
    def sendCommand(self,command):
        try:
            self.sock.send(command)
            while 1:
                self.response = self.sock.recv(1024)
                if not self.response:
                    break
                self.cmdOut.append(self.response)
        finally:
            self.sock.close()
    
    def sendSetSpecCommand(self,specfile):    
        self.cmdOut=''
        try:
            self.sendCommand('send_spec')
            if self.cmdOut != 'ok':
                raise RiTHMCliException("send_spec failed")
            self.cmdOut=''
            specFileFd = open(specfile,'r')
            sendData=''
            for line in specFileFd:
                sendData.append(line)
            self.sendCommand(sendData)
            if self.cmdOut != 'ok':
                raise RiTHMCliException("send_spec contents failed")
        except IOError:
            pass     
    
    def sendSetTraceCommand(self,traceFile):    
        self.cmdOut=''
        try:
            self.sendCommand('send_trace')
            if self.cmdOut != 'ok':
                raise RiTHMCliException("send_trace failed")
            self.cmdOut=''

            traceFileFd = open(traceFile,'r')
            sendData=''
            for line in traceFileFd:
                sendData.append(line)
            self.sendCommand(sendData)
            if self.cmdOut != 'ok':
                raise RiTHMCliException("send_trace contents failed")
        except IOError:
            pass    
        
    def sendRunMonitorCommand(self,outputFile):    
        self.cmdOut=''
        try:
            self.sendCommand('run_monitor')
            outputFileFd = open(outputFile,'w')
            outputFileFd.write(self.cmdOut)
        except IOError:
            pass
        except RiTHMCliException:    
            pass 
             
if __name__ == "__main__":
    argv=sys.argv[1:]
    specFile=''
    traceFile=''
    outputfile=''
    try:
        opts, args = getopt.getopt(argv,"hs:t:o:a:p",["specfile=","tracefile=","outputfile=","ip=","port="])
    except getopt.GetoptError:
        print 'rithmClient.py -s <specfile> -t <tracefile> -o <outputfile>'
        sys.exit(2)       
    for opt, arg in opts:
        if opt == '-h':
            print 'rithmClient.py -s <specfile> -t <tracefile> -o <outputfile>'
            sys.exit()
        elif opt in ("-s", "--specfile"):
            specFile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg  
        elif opt in ("-s", "--specfile"):
            specFile = arg
        elif opt in ("-t", "--tracefile"):
            traceFile = arg    
