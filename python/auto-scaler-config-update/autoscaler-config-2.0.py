import os
import subprocess
import time
import json
import smtplib
import MySQLdb

from datetime import date
from email.mime.text import MIMEText
from smtplib import SMTPException

# * Dev
CONFIG_DIR = 'config_dir/'; 
RUNNING_DIR = 'running_dir/';
AUTOSCALER_LOG_DIR = 'autoscaler_log/';
# AUTOSCALER_LOG_DIR = '/data/system/log/';

PROD = False # Do not update this variable on DEV environment

if PROD :
    # * Production
    CONFIG_DIR = '/home/hieu.du/';
    RUNNING_DIR = '/usr/dena/lib/perl/DeNA/Conf/jp_aws/'; 
    AUTOSCALER_LOG_DIR = '/data/system/log/';

year = '17';
today = date.today();
state_info = '';

# print getTime()

# Event List: 
# * GVG
# * LeagueBattle
# * MTWupdate
# * NoEvent
# * RankingPVP
# * SPD
# * TKwar

scheduleEvent = [
    {   
        'Start': '0407',
        'End': '0413',
        'Event': 'LeagueBattle'
    },
    {   
        'Start': '0414',
        'End': '0416',
        'Event': 'NoEvent'
    },
    {   
        'Start': '0417',
        'End': '0423',
        'Event': 'SPD'
    },
    {   
        'Start': '0424',
        'End': '0426',
        'Event': 'NoEvent'
    },
    {   
        'Start':'0427',
        'End': '0503',
        'Event': 'GVG'
    },
    {   
        'Start':'0504',
        'End': '0507',
        'Event': 'NoEvent'
    },
    {   
        'Start':'0508',
        'End': '0513',
        'Event': 'RankingPVP'
    },
    {   
        'Start':'0514',
        'End': '0515',
        'Event': 'NoEvent'
    },
    {   
        'Start':'0516',
        'End': '0522',
        'Event': 'SPD'
    },
];

def getTime() :
    current = time.localtime()
    return str(current.tm_year) + "-" + str(current.tm_mon).zfill(2) + "-" + str(current.tm_mday).zfill(2) + " " + str(current.tm_hour).zfill(2) + ":" + str(current.tm_min).zfill(2) + ":" + str(current.tm_sec).zfill(2)
def getEvent(scheduleEvent):
    todayTS = int(str(today.year)[2:4] + str(today.month).zfill(2) + str(today.day).zfill(2));
    for x in scheduleEvent:
        if len(x['Start']) < 5:
            start = int(year+ x['Start']);
        else:
            start = int(x['Start']);
        if len(x['End']) < 5:
            end = int(year + x['End']);
        else:
            end = int(x['End']);

        # print "Start: " + str(start) + " - End: " + str(end) + " - Today: " + str(todayTS);
        if (start == todayTS) and (end >= todayTS):
            return "Before_" + x['Event']; 
        if (start<todayTS) and (end>=todayTS):
            return  x['Event']; 
    return 'UNKNOWN'

def getEventDB():
    # DB Connection
    db = MySQLdb.connect("localhost","root","123456a@A","demo")
    cursor = db.cursor()
    event_name ='UNKNOWN'

    # Get Event ID
    query = "SELECT event FROM schedules where `start` <= '" + str(today) + " 00:00:00' and `end` >= '"+ str(today) + " 23:59:59'"
    # print query
    cursor.execute(query);
    events = cursor.fetchall()
    event_id = 0
    if 1== len(events):
        event_id = events[0][0]
    else:
        print "Duplicated config"
        db.close()
        return event_name

    #Get Event name
    query = "SELECT `name` FROM events WHERE `id` = " + str(event_id)
    # print query
    cursor.execute(query);
    event = cursor.fetchone()
    if event is None:
        print "Event with id: " + event_id + "not exist"
    else:
        event_name =  event[0]
    return event_name
    db.close()

def copyConfigFile(CONFIG_DIR, RUNNING_DIR, event):
    print getTime() + " : Copy File " + event +" Configuration ...";
    subprocess.call(['cp', '-f', CONFIG_DIR + "AutoScaling." + event + ".pm", RUNNING_DIR + "AutoScaling.pm"])

def restartAutoScaler():
    print getTime() + " : Restarting Autoscaler ...";
    # subprocess.call(['sudo', 'svc', '-t', 'auto-scaler-cotk_jp']) # Comment on Dev

def tail(f, n, offset=0):
  stdin,stdout = os.popen2("tail -n "+ str(n) + str(offset) + " " + f)
  stdin.close()
  lines = stdout.readlines(); stdout.close()
  lines.reverse()
  return lines

def isStable():
    # Return 1 if stable, else return last status
    log_file = AUTOSCALER_LOG_DIR + "auto-scaler.log." + str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2);
    # print log_file; exit();
    lines = tail(log_file, 1000)
    for line in lines:
        if "[DEBUG] Main: stat = {'After' =>" in line:
            # print line
            state_info = line[line.index("{'After'"):]
            break
    state_info = state_info.replace("=>", ":")
    # print getTime() + " : " + state_info
    data  = eval(state_info)
    diff = data['Diff']
    if diff == 0:
        return 1
    else:
        return state_info

def notify(message):
    sender = 'infra_hanoi_my@dena.jp'
    receivers = ['infra-fatal@jp.denagames-asia.com']
    header = """From: Infra Hanoi <infra_hanoi_my@dena.jp>
To: Fatal <infra-fatal@jp.denagames-asia.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Configuration file could not be replaced

"""
    full_message = header + message
    try:
        smtpObj = smtplib.SMTP('mail.denagames-asia.local')
        smtpObj.sendmail(sender, receivers, full_message)         
        # print getTime() + " : Successfully sent email"
    except SMTPException:
        print getTime() + " : Error: unable to send email"

# *****************************************************************************************************************************
# MAIN
# *****************************************************************************************************************************

# Check status of Autoscaler
print "\n"
print "***************************************************************************"
print getTime() + " : Start"
count = 0
while count < 5:
    status = isStable()
    if (status ==1):
        event = getEvent(scheduleEvent)
        # event = getEventDB()
        if event == 'UNKNOWN' :
            print "Send email about failed to determine event"
            notify("Can not determine event")
        else :
            print getTime() + " : Event is detected: " + event
            copyConfigFile(CONFIG_DIR, RUNNING_DIR, event)
            restartAutoScaler()

        # break    
    else:
        count += 1
        print getTime() + "Stop update configuration. Autoscaler is running. Detail:" + status
        print getTime() + "Sleep for 5 minutes"
    time.sleep(10)
if count == 5:
    print "Send email"
    # notify("Autoscaler is running. Detail:" + status)
print getTime() + " : End"
print "***************************************************************************"