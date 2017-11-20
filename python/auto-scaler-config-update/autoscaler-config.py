#!/usr/bin/python
import os
import subprocess
import time
import json
import smtplib
import datetime
import re
import logging
import argparse
import sys

from datetime import date
from email.mime.text import MIMEText
from smtplib import SMTPException


# Default values
DEBUG = False
PROD = True # Update to True before commit

CONFIG_DIR = 'config_dir/'; 
RUNNING_DIR = 'running_dir/';
AUTOSCALER_LOG_DIR = 'log_autoscaler/';
LOG_FILE = 'auto-scaler-config-update.log'

# Parse arguments 
parser = argparse.ArgumentParser(prog='Autoscaler driver', description='')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
parser.add_argument('-s', '--sandbox', action='store_true', help='Define sandbox environment')
parser.add_argument('-l', '--log', nargs=1, help='Specify autoscaler log location')
parser.add_argument('-c', '--configdir', nargs=1, help='Specify configurations directory location')
parser.add_argument('-r', '--runningdir', nargs=1, help='Specify real autoscaler configuration file location')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = vars(parser.parse_args(sys.argv[1:]))

if args['debug']:
    DEBUG = True

if args['sandbox']:
    PROD = False

# Environment
if PROD:
    logging.basicConfig(level=logging.INFO, format = ' %(asctime)s [%(levelname)s] : %(message)s', filename=LOG_FILE)
    CONFIG_DIR = '/home/hieu.du/';
    RUNNING_DIR = '/usr/dena/lib/perl/DeNA/Conf/jp_aws/'; 
    AUTOSCALER_LOG_DIR = '/data/system/log/';
else:
    logging.basicConfig(level=logging.DEBUG, format = ' %(asctime)s [%(levelname)s] : %(message)s', filename=LOG_FILE)


if args['log'] != None:
    AUTOSCALER_LOG_DIR = args['log'][0] + "/";

if args['configdir'] != None:
    CONFIG_DIR = args['configdir'][0] + "/";

if args['runningdir'] != None:
    RUNNING_DIR = args['runningdir'][0] + "/";

# Verify arguments
logging.debug('Enable debug mode  : ' + str(DEBUG))
logging.debug('Production environment: ' + str(PROD))
logging.debug('CONFIG_DIR         : ' + CONFIG_DIR)
logging.debug('RUNNING_DIR        : ' + RUNNING_DIR)
logging.debug('AUTOSCALER_LOG_DIR : ' + AUTOSCALER_LOG_DIR)

year = '17'; # Default for 2017
today = date.today();
state_info = '';

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
        'Start': '0526',
        'End': '0601',
        'Event': 'GVG'
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
    {
        'Start': '0523',
        'End': '0525',
        'Event': 'NoEvent'
    },
];

def getEvent(scheduleEvent, date_check = None):
    todayTS = int(str(today.year)[2:4] + str(today.month).zfill(2) + str(today.day).zfill(2));
    if date_check != None:
        todayTS = date_check
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
        if (start<=todayTS) and (end>=todayTS):
            event_name = x['Event']
            if (event_name == 'MTWupdate') or (event_name == 'NoEvent'):
                return event_name
            if (start == todayTS) and (end >= todayTS):
                return "Before_" + x['Event']; 
            else:
                return x['Event']
    return 'UNKNOWN'

def copyConfigFile(CONFIG_DIR, RUNNING_DIR, event):
    logging.info("Copy File " + event +" Configuration ...")
    try:
        subprocess.check_call(['cp', '-f', CONFIG_DIR + "AutoScaling." + event + ".pm", RUNNING_DIR + "AutoScaling.pm"])
    except subprocess.CalledProcessError:
        logging.error("Could not copy new configuration file")
        return 0
    return 1

def restartAutoScaler():
    logging.info("Restarting Autoscaler ...")
    if PROD :
        try:
            subprocess.check_call(['sudo', 'svc', '-t', '/service/auto-scaler-cotk_jp']) # Comment on Dev
            time.sleep(10)
        except subprocess.CalledProcessError:
            logging.error("Could not run restart autoscaler command")
            return 0
    return 1

def isRestarted():
    logging.info("Checking restart result ...")
    if PROD :
        try:
            p = subprocess.Popen(['sudo', 'svstat', '/service/auto-scaler-cotk_jp'], stdout=subprocess.PIPE)
            stdout_value = p.communicate()[0]
            logging.debug("Result" + stdout_value)
            regex = re.compile(r'(\d+) second')
            result = regex.search(stdout_value)
            if result == None:
                return 0
            else:
                life_time = result.group(1)
                if int(life_time) > 10 :
                    return 0
                else:
                    return 1
        except ValueError as e:
            logging.error("Checking status of autoscaler after restart was fail")
            return 0
    else:
        return 1

def ptail(f, n):
    if os.path.isfile(f):
        p = subprocess.Popen(['tail', '-n', str(n), f], stdout=subprocess.PIPE)
        lines = p.communicate()[0].split("\n")
        lines.reverse()
        # logging.debug(lines)
        return lines
    else:
        logging.error("Could not read file " + f)
        return 0

def isStable():
    # Return 1 if stable, else return last status
    state_info = ''
    state_pattern = "[DEBUG] Main: stat = {'After' =>"
    log_file = AUTOSCALER_LOG_DIR + "auto-scaler.log." + str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2);
    lines = ptail(log_file, 1000)
    if lines == 0:
        return 'Could not read autoscaler log !!!'
    for line in lines:
        if state_pattern in line:
            # print line
            state_info = line[line.index("{'After'"):]
            break
    state_info = state_info.replace("=>", ":")
    # logging.info("State info: "+ state_info)
    data  = eval(state_info)
    diff = data['Diff']
    if diff == 0:
        return 1
    else:
        return state_info

def notify(message, subject = "Configuration file could not be replaced"):
    sender = 'infra_hanoi_my@dena.jp'
    receivers = ['infra-fatal@jp.denagames-asia.com']
    header = """From: Infra Hanoi <infra_hanoi_my@dena.jp>
To: Fatal <infra-fatal@jp.denagames-asia.com>
MIME-Version: 1.0
Content-type: text/html
Subject: """ + subject + """

""";
    full_message = header + message
    if PROD :
        try:
            smtpObj = smtplib.SMTP('mail.denagames-asia.local')
            smtpObj.sendmail(sender, receivers, full_message)         
            logging.info("Successfully sent email")
        except SMTPException:
            logging.error("Unable to send email")

# *****************************************************************************************************************************
# MAIN
# *****************************************************************************************************************************

# Check status of Autoscaler
logging.info("***************************************************************************")
logging.info('Start')
count = 0
restart_error = ''
while count < 5:
    status = isStable()
    if (status ==1):
        event = getEvent(scheduleEvent)
        # event = getEventDB()
        if event == 'UNKNOWN' :
            logging.error("Cannot determine event on today")
            logging.info("Send email about failed to determine event")
            notify("Could not determine event. Please update schedule right now", "Could not determine event")
        else :
            logging.info("Event is detected: " + event)

            if not DEBUG :
                copy_result = copyConfigFile(CONFIG_DIR, RUNNING_DIR, event)
                if copy_result == 1 :
                    restartAutoScaler()

                    # Check restart
                    is_restart = isRestarted()
                    if is_restart == 0 :
                        count += 1
                        restart_error = 'Fail to run restart command'
                        logging.error("Fail to restart. Try again ...")
                        continue
            else:
                logging.info("Debug mode is enable. Terminated!")

        break    
    elif status == 'Could not read autoscaler log !!!':
        restart_error = status
        logging.warning(status)
    else:
        restart_error = 'Autoscaler is running'
        logging.warning("Stop update configuration. Autoscaler is running. Detail: " + status)
    count += 1
    logging.info("Sleep for 5 minutes")
    time.sleep(300)

if count == 5:
    logging.error("Could not restart Autoscaler. " + restart_error + ". Notifying ...")
    if PROD :
        notify("Could not restart Autoscaler. Detail:" + restart_error)
# Check nextweek event
next_week = date.today() + datetime.timedelta(days=7)
next_week_ts = int(str(next_week.year)[2:4] + str(next_week.month).zfill(2) + str(next_week.day).zfill(2));
next_week_event = getEvent(scheduleEvent, next_week_ts)  
# logging.debug("Event on " + str(tomorrowTS) + ": " + next_event)
if next_week_event == 'UNKNOWN':
    logging.error("Could not detect event for next 7 days")
    logging.info("Send email about failed to determine event for next 7 days")
    notify("Could not determine event for next week. Please update schedule for next event", "Could not determine event for next 7 days")

logging.info("End")