import serial
import datetime
import time
import sys


ozonePort                = '/dev/tty.usbserial-2130'
firstReset              = True
firstResolutionSetup     = True
firstMetricSystemSetup   = True
loopInterval  = 10;

baudRate = 9600


def delayMints(timeSpent,loopIntervalIn):
    loopIntervalReal = loopIntervalIn ;
    if(loopIntervalReal>timeSpent):
        waitTime = loopIntervalReal - timeSpent;
        time.sleep(waitTime);
    return time.time();

def readLine(lineIn,sleepTime):
    dataString     = (''.join(lineIn)).replace("\n","").replace("\r","")
    print(dataString)
    time.sleep(sleepTime)
    return;      

def sendChars(printStr,serIn,charsIn,sleepTime):
    print(printStr)
    serIn.write(str.encode(charsIn))
    time.sleep(sleepTime)
    return ;


def main(firstReset,firstResolutionSetup,firstMetricSystemSetup,loopInterval):

    time.sleep(30)

    ser = serial.Serial(
    port= ozonePort,\
    baudrate=baudRate,\
	parity  =serial.PARITY_NONE,\
	stopbits=serial.STOPBITS_ONE,\
	bytesize=serial.EIGHTBITS,\
    timeout=0)

    print(" ")
    print("Connected to: " + ser.portstr)
    print(" ")
    line = []

    
    print("First Data Read")
    ser.write(str.encode('R\r\n'))
    time.sleep(1)

    while True:
        try:
            for c in ser.read():
                line.append(chr(c))
                
                if chr(c) == '\n' and (firstReset):
                    readLine(line,5)
                    sendChars("Reset Sensor",ser,'O\r\n',2)
                    sendChars("Second Data Read",ser,'R\r\n',2)
                    line = []
                    firstReset = False
                    break;
                    
                if chr(c) == '\n' and (firstResolutionSetup):
                    readLine(line,5)
                    sendChars("Force High Resolution",ser,'H\r\n',2)        
                    line = []
                    firstResolutionSetup = False
                    break;
                    
                if chr(c) == '\n' and (firstMetricSystemSetup):
                    readLine(line,5)
                    sendChars("Force Metric System",ser,'M\r\n',2)                    
                    line = []
                    firstMetricSystemSetup= False;
                    startTime = time.time()
                    break;

                     

                if chr(c) == '\n':
                    readLine(line,1)
                    dateTime = datetime.datetime.now()
                    print(dateTime)
                    time.sleep(5)
                    line = []
                    sendChars("Read Command Sent",ser,'R\r\n',1)   
                    startTime = delayMints(time.time() - startTime,loopInterval)

        except OSError as e:
            time.sleep(1)
            print ("Error: %s - %s." % (e.filename, e.strerror))
            time.sleep(1)

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    # print("Monitoring Ozone Sensor on port: {0}".format(ozonePort[0])+ " with baudrate " + str(baudRate))
    main(firstReset,firstResolutionSetup,firstMetricSystemSetup,loopInterval)