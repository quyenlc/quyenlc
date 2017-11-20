#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 3 and compatibility with Python 2
from __future__ import unicode_literals, print_function 

import os
import sys
import re
import logging
import smtplib

from subprocess import Popen, PIPE

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jinja2 import Environment, FileSystemLoader


class EmailNotification(object):
    EMAIL_REGEX = re.compile('([\w\-\.\']+@(\w[\w\-]+\.)+[\w\-]+)')
    HTML_REGEX = re.compile('(^<!DOCTYPE html.*?>)')

    def __init__(self, transport, fromuser, fromemail, envelopefrom, templatedir='templates', logger=None):
        self.logger = logger
        if not logger:
            logging.basicConfig()
            self.logger = logging.getLogger(__name__)
        self.transport = transport
        self.mfrom = "%s <%s>" % (fromuser, fromemail)
        self.reply = fromemail
        self.envelopefrom = envelopefrom
        if os.path.isdir(templatedir):
            self.templatedir = templatedir
        else:
            self.templatedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), templatedir)
        self.env = Environment(loader=FileSystemLoader(self.templatedir))

    def _mail_render(self, data, template):
        template = template + ".tmpl"
        self.logger.debug("Rendering template '%s'" % (template))
        text = self.env.get_template(template)
        msg = text.render(data)
        return msg

    def _smtp_connect(self):
        try:
            smtp = smtplib.SMTP(self.smtp)
        except Exception as e:
            self.logger.error("Cannot connect with '%s': %s" % (self.smtp, e))
            raise
        if self.smtplogin:
            try:
                smtp.login(self.smtplogin, self.smtppass)
            except smtplib.SMTPException as e:
                self.logger.error("Cannot auth with '%s' on %s: %s" % (self.smtplogin, self.smtp, e))
                raise
            finally:
                smtp.quit()
        return smtp

    def _build_mail(self, emails, subject, content):
        if self.HTML_REGEX.match(content) is None:
            self.logger.debug("Sending text mail to '%s'" % (', '.join(emails)))
            msg = MIMEText(content)
        else:
            self.logger.debug("Sending html mail to '%s'" % (', '.join(emails)))
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(content, 'html', 'utf-8'))
        msg['From'] = self.mfrom
        msg['To'] = ', '.join(emails)
        msg['Reply-to'] = self.reply
        msg['Subject'] = subject
        return msg

    def _smtp_send(self, smtp, emails, subject, content):
        msg = self._build_mail(emails, subject, content);
        smtp.sendmail(self.mfrom, emails, msg.as_string())

    def _sendmail_send(self, emails, subject, content):
        msg = self._build_mail(emails, subject, content);
        cmd = ['sendmail', '-oi', '-t', '-f%s' % self.envelopefrom]
        process = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (out,err) = process.communicate(input=msg.as_string())
        if err:
            raise

    def send_bulk_smtp(self, msgs):
        smtp = self._smtp_connect()
        processed = 0
        for (emails, subject, msg) in msgs:
            try:
                self._smtp_send(smtp, emails, subject, msg)
            except smtplib.SMTPException as e:
                self.logger.error("Cannot send mail to '%s': %s" % (', '.join(emails), e))
            else:
                processed += 1
        smtp.quit()
        return processed

    def send_bulk_sendmail(self, msgs):
        processed = 0
        for (emails, subject, msg) in msgs:
            try:
                self._sendmail_send(emails, subject, msg)
            except Exception as e:
                self.logger.error("Cannot send mail to '%s': %s" % (', '.join(emails), e))
            else:
                processed += 1
        return processed

    def mailbulk(self, emaildata, template):
        elist = []
        for edata in emaildata:
            try:
                emails = edata["emails"]
                subject = edata["subject"]
                data = edata["data"]
            except Exception as e:
                continue
            if emails is None:
                error = "Email list is empty!"
                self.logger.error(error)
                continue
            else:
                good_email = True
                for email in emails:
                    if self.EMAIL_REGEX.match(email) is None:
                        error = "Invalid email address: %s" % email
                        self.logger.error(error)
                        good_email = False
                        continue
                if not good_email:
                    continue
            msg = self._mail_render(data, template)
            elist.append((emails, subject, msg))
        if self.transport == 'SMTP':
            return self.send_bulk_smtp(elist)
        elif self.transport == 'SENDMAIL':
            return self.send_bulk_sendmail(elist)
