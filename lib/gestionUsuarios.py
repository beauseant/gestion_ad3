'''
Created on Jan 13, 2012

@author: breakthoven
'''

from ldap3 import Server, Connection, SIMPLE, SYNC, ALL, SASL, NTLM, ALL_ATTRIBUTES, SUBTREE
import datetime
import lib.filetimes as filetimes
import hashlib
import os
import base64


class gestionUsuariosUnix:


	__ldap_con = ''
	__basedn   = '' 


	def __init__ (self,nombre, passwd, basedn, servidor):

		s = Server(servidor,  use_ssl=True, get_info=ALL)

		conn = Connection(s, user= nombre, password=passwd)

		self.__ldap_con 	= conn
		self.__basedn 		= basedn

		if not conn.bind():
			raise Exception("An error occurred %s" % conn.result)

		
		return None



	def listAllUsers (self):
		
		conn = self.__ldap_con
		base = self.__basedn

		conn.search(base, '(&(objectclass=*))', attributes=['*'])

		return conn.entries


	def getLasId (self, minimo=2000, maximo=9000):

		conn = self.__ldap_con
		base = self.__basedn

		conn.search(base, '(&(objectclass=*))', attributes=['uidNumber'])

		listIds=[int(str(id['uidNumber'])) for id in conn.entries if str(id['uidNUmber'])!='[]']

		return max (list((filter(lambda x: (x>minimo and x<maximo), listIds))))



	def makeSecret(self, password):

		'''
		import ipdb ; ipdb.set_trace()
		salt = os.urandom(4)
		h = hashlib.sha1(password.encode('utf-8'))
		h.update(salt)
		return "{SSHA}" + encode(h.digest() + salt).decode('utf-8')
		'''
		#return '{SSHA}%s' % bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt( 12 )).decode('utf-8')

		
		salt = os.urandom(4)
		#h = hashlib.sha1(password)
		hash=hashlib.sha1(password.encode('utf-8')+salt)
		#h.update(salt)
		#return "{SSHA}" + encode(h.digest() + salt).decode('utf-8')
		enc_passwd1=base64.b64encode(hash.digest()+salt)
		return ('{SSHA}%s' % enc_passwd1.decode('utf-8'))

	def createUser (self, usuario, objectClass, attributes):
		conn = self.__ldap_con
		base = self.__basedn


		attributes['userPassword'] = self.makeSecret (attributes['userPassword'])
		conn.add (usuario, objectClass, attributes)		
		#import ipdb ; ipdb.set_trace()
		#conn.passwd_s("cn=Marice McCaugherty,ou=Product Testing,dc=example,dc=com", "ytrehguaCc", "secret")







class gestionUsuariosAD:

	__ldap_con = ''
	__basedn   = '' 


	def __init__ (self,nombre, domain, passwd, basedn, servidor):
		# define the server and the connection
		s = Server(servidor,  use_ssl=True, get_info=ALL)
		userComplete = ('%s\\%s' % (domain, nombre))

		conn = Connection(s, user= userComplete, password=passwd, authentication=NTLM)

		self.__ldap_con 	= conn
		self.__basedn 		= basedn

		if not conn.bind():
			raise Exception("An error occurred %s" % conn.result)

		
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


	def createUser (self, attributes):

        
		#usersOU = 'ou=Users,dc=tsc,dc=uc3m,dc=es'
		#self.__ldap_con.add(usersOU, 'organizationalUnit') # add test-ou for users



		base = ('cn=%s,%s' % (attributes['displayName'], self.__basedn))


		try:
			if 'accountExpires' in attributes:
				attributes['accountExpires'] = filetimes.dt_to_filetime (datetime.datetime.strptime(attributes['accountExpires'], '%d/%m/%Y'))

			self.__ldap_con.add (base, attributes=attributes)		

		except Exception as E:
			print ('Error %s, resultado consulta: %s', (E, self.__ldap_con.result))
				

		#si devuelve un error del tipo description': 'unwillingToPerform', 'dn': '', 'message': '0000001F: SvcErr: DSID-031A1254, problem 5003 (WILL_NOT_PERFORM),
		# es porque la conexión no es ssl, en el init, seccion de server se debe poner use_ssl=True!!!!!!!!!!!!!!!!

		try:
			self.__ldap_con.extend.microsoft.modify_password(base,attributes['userPassword'], controls=None)
		except Exception as E:
			print ('Error %s, resultado consulta: %s', (E, self.__ldap_con.result))