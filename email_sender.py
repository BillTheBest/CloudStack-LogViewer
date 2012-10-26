#!/usr/bin/python
#coding:utf-8


import sys
import datetime
import smtplib
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


reload(sys) 
sys.setdefaultencoding('utf8')

class email_sender:
	def send_html_email_no_encode(self , smtp ,  send_from , send_pass , send_tos , plain_txt,html_content , title ):
		'''
		'''
		now = datetime.datetime.now()
		today = datetime.date.today()
		msg = MIMEMultipart( )
		body = MIMEMultipart('alternative')
		msg['Subject'] =  Header(title ,"utf-8")
		msg['From'] = send_from
		text = plain_txt 
		html = html_content
		part_text = MIMEText(text, 'plain', 'utf-8')
		body.attach(part_text)		
		try:
			part_html = MIMEText(html, 'html', 'utf-8')
			part_html.set_charset('utf-8')
			body.attach(part_html)
		except:
			print 'error html format'
		msg.attach(body)
		try:
			smtp_server = smtplib.SMTP()
			smtp_server.connect(  smtp  )
			smtp_server.login( send_from  , send_pass )
			smtp_server.sendmail( send_from , send_tos , msg.as_string())
			smtp_server.close()
		except Exception, e:
			print "send error:",e	
		pass	
	def send_html_email(self , smtp ,  send_from , send_pass , send_tos , plain_txt,html_content , title ):
		'''
		'''
		now = datetime.datetime.now()
		today = datetime.date.today()
		msg = MIMEMultipart( )
		body = MIMEMultipart('alternative')
		msg['Subject'] =  Header(title ,"utf-8")
		msg['From'] = send_from
		text = plain_txt 
		html = """\
		<html>
		  <head></head>
		  <body>
		  </body>
		</html>
		"""
		html = html_content
		try:
			try:
				#text = text
				text=text.decode("GB2312").encode("UTF-8")#
			except UnicodeDecodeError:
				print "error:" + text
			except:
				print "error:" + text		
			part_text = MIMEText(text, 'plain', 'utf-8')
			#msg.attach(part_text)
			body.attach(part_text)
		except:
			print 'error text format'
			print text
			text = text
		try:
			part_html = MIMEText(html, 'html', 'utf-8')
			part_html.set_charset('utf-8')
			body.attach(part_html)
		except:
			print 'error html format'
		msg.attach(body)
		try:
			smtp_server = smtplib.SMTP()
			smtp_server.connect(  smtp  )
			smtp_server.login( send_from  , send_pass )
			smtp_server.sendmail( send_from , send_tos , msg.as_string())
			smtp_server.close()
		except Exception, e:
			print "send error:",e	
		pass

		
if "__main__" == __name__:
	print "begin test ..."
	es = email_sender()
	module_name = "chain_mail_config"
	dyna_module = __import__( module_name )
	plain_content=""
	html_content= ""
	title="email send test"
	es.send_html_email( dyna_module.config_mail_smtp,   dyna_module.config_mail_from ,  dyna_module.config_mail_from_password , dyna_module.config_mail_send_to , plain_content , html_content   , title  )		
	
	