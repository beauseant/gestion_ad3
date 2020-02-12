import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class sender:

	def __init__ ( self, username, host, pwd ):
		self.__username = username
		self.__host = host
		self.__pwd = pwd

	def sent (self, subject, body, from_addr, to_addr_list,cc_addr_list=[] ):


		msg = MIMEMultipart()
		msg['From'] = from_addr
		msg['To'] = to_addr_list[0]
		msg['Subject'] = subject
		msg.attach(MIMEText(body, 'plain'))

		server = smtplib.SMTP_SSL (self.__host,465)
		server.login(self.__username,self.__pwd)

		text = msg.as_string()		
		problems = server.sendmail(from_addr, to_addr_list, text)
		server.quit()	

		return problems
