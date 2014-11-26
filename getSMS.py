#!/usr/bin/python
#
# gammu python docu op http://wammu.eu/docs/manual/python/#api-documentation

import gammu
import os
import time
import logging
import xml.etree.ElementTree as ET
homedir="/root/dev/portier"

# setup things
timeslot = 10 # tijdsslot waarbinnen niet wordt gereageerd op bijkomende requests om deur open te doen

logging.basicConfig(filename='/var/log/portier.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

#########################
def checkPhoneList(smsnumber):

    isValid=False
    callerID=''
    tree = ET.parse(homedir+'/phones.xml')
    root = tree.getroot()
    for item in root:
    
        #print item[5].text
        if smsnumber == item[5].text[2:]:
           isValid=True
           callerID = item[0].text

    return isValid, callerID
##########################

def check4Sms():
	
    validPhoneNumber = False
    validMessage = False

    sm = gammu.StateMachine()
    sm.ReadConfig(0,0,homedir+"/.gammurc") # ~./gammurc

    try:
        sm.Init()
	
        status = sm.GetSMSStatus()

        remain = status['SIMUsed'] + status['PhoneUsed'] + status['TemplatesUsed']
	
        sms = []
        start = True

        while remain > 0:
            if start:
                cursms = sm.GetNextSMS(Start = True, Folder = 0)
                start = False
            else:
                cursms = sm.GetNextSMS(Location = cursms[0]['Location'], Folder = 0)
            remain = remain - len(cursms)
            sms.append(cursms)

        data = gammu.LinkSMS(sms)

        for x in data:
            v = gammu.DecodeSMS(x)

            m = x[0]
            print
            #print '%-15s: %s' % ('Number', m['Number'])
            if m['Text'] == "404#":
                validMessage = True
            smsnumber = m['Number']
            validPhoneNumber, callerID = checkPhoneList(smsnumber[3:]);
            logging.warning("Got sms from %s (%s), %s, %s" % (smsnumber, str(m['DateTime']), m['Text'], callerID ))

            if validMessage == True:
                
                logging.warning("___ Valid message!")

                if validPhoneNumber == True:
                
                    logging.warning("___ Valid number, opening doors....")
                    os.system("i2cset -y 2 0x21 0x40 0x03")
                    time.sleep(1)
                    os.system("i2cset -y 2 0x21 0x40 0x00")
            else:
                logging.warning("___ Message NOT valid")
            
            logging.warning("*** Deleting message")
            sm.DeleteSMS(0,cursms[0]['Location'])
            #print test
            #print '%-15s: %s' % ('Date', str(m['DateTime']))
            #print '%-15s: %s' % ('State', m['State'])
            #print '%-15s: %s' % ('Folder', m['Folder'])
            #print '%-15s: %s' % ('Validity', m['SMSC']['Validity'])
    except Exception as e:
	logging.error("__ERROR__ %s" % (e,))
    #except gammu.ERR_TIMEOUT as e:
    #    logging.error("__ERROR__ %s" % (e,))
    #sm.DeleteSMS(0,x)

logging.debug("Script started...")
while (1):
    check4Sms();
    time.sleep(10)
