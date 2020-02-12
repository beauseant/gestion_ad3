'''
Created on Jan 13, 2012

@author: breakthoven
'''

from ldap3 import Server, Connection, SIMPLE, SYNC, ALL, SASL, NTLM, ALL_ATTRIBUTES, SUBTREE

import datetime

class gestionUsuariosAD:

	ACCOUNT_NO_EXPIRE 	= "-150901";
	ACCOUNT_NO_USE	= "150899";

	__usuarios = {}
	__db	   = ''
	__ldap_con = ''
	__basedn   = '' 


	def __init__ (self,nombre, domain, passwd, basedn, servidor):
		# define the server and the connection
		s = Server(servidor, get_info=ALL)
		userComplete = ('%s\\%s' % (domain, nombre))

		conn = Connection(s, user= userComplete, password=passwd, authentication=NTLM)

		self.__ldap_con 	= conn
		self.__basedn 		= basedn

		if not conn.bind():
			raise CustomError("An error occurred %s" % c.result)

		
		return None


	def listAllUsers (self, attributes = ['cn','whenChanged', 'whenCreated', 'sAMAccountName', 'sn', 'name', 'lastLogon', 'accountExpires']):

		conn = self.__ldap_con

		filter = "(&(objectClass=user)(name=" + '*' + "))"
		

		result = conn.search(search_base=self.__basedn, search_filter=filter, attributes=attributes)

		listUsers = []
		for e in conn.entries:
			user = {}
			for attr in attributes:
				user[attr] = str(e[attr])
			listUsers.append (user)		

		return listUsers


	def __checkDate__ ( self, user ):

		date_time_str = user['accountExpires'][:10]
		date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')

		if self.__days == 0:
			salida = (datetime.datetime.now()>date_time_obj and (date_time_str != '1601-01-01'))
		else:
			
			salida = (
					datetime.datetime.now()<date_time_obj and
					(date_time_str != '1601-01-01') and
					datetime.datetime.now() > date_time_obj - datetime.timedelta(days=self.__days)
			)
		return salida



	def listExpired (self, attributes = ['sAMAccountName'], days=0):

		expired = 'accountExpires'

		self.__days = days

		if not expired in attributes:
			attributes.append (expired)



		return  list(filter (self.__checkDate__, self.listAllUsers ( attributes ) ))

	def listExpiredIn (self, days, attributes = []):

		return self.listExpired (attributes, days )
