#!/usr/bin/env python
from GPUDashboard import *
from optparse import OptionParser

def main():
    options = parseArgs()
    ServerName = options.serverName
    interval = options.interval
    firebaseUrl = options.firebaseUrl
    gdb = GPUDashboard()
    session = requests.Session()
    while 1:
        try:
            gdb.update()
            gpuInfosJson = json.dumps(gdb.outputInfo())
            result = session.patch('{firebaseUrl}/Servers/{ServerName}/GPU.json'.format(firebaseUrl=firebaseUrl,ServerName=ServerName),data=gpuInfosJson)
            time.sleep(interval)
        except requests.exceptions.ConnectionError:
            time.sleep(100)
            session = requests.Session()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(repr(e))
            time.sleep(100)
            
def parseArgs():
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="serverName",default="GPU server",
                  help="Server name", metavar="ServerName")
    parser.add_option("-i", "--interval", dest="interval",default=20,type=int,
                  help="time interval", metavar="second")
    parser.add_option("-u", "--url", dest="firebaseUrl",
                  help="your firebase url", metavar="firebase URL")
    options, args = parser.parse_args() 
    return options

if __name__ == '__main__':
    main()