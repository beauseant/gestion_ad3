
import lib.gestionUsuarios as ad
from lib import sendMail
import configparser
import argparse
import json
import uuid



if __name__ == "__main__":

	parser	= argparse.ArgumentParser ( description='Gestion de un Active Directory desde python. Muestra informacion de usuario y pone caducidad a la cuenta' )

	parser.add_argument('config'  , action = "store", metavar='config', type=str, help='fichero de configuracion')
	parser.add_argument('userData'  , action = "store", metavar='config', type=str, help='fichero json con datos de usuario')



	args	 =	parser.parse_args()


	cfg = configparser.ConfigParser()

	if not cfg.read([ args.config ]):
		print ('Archivo de configuracion no encontrado :(')
	else:
		try:
			nombre 		= cfg.get ( 'UNIX','nombre')
			passwd 		= cfg.get ( 'UNIX','passwd')
			basedn		= cfg.get ( 'UNIX','basedn')
			servidor	= cfg.get ( 'UNIX','servidor')

		except Exception as E:
			print (E)
			exit ()

		with open(args.userData) as json_file:
			attributes = json.load(json_file)


		unixConn 	= ad.gestionUsuariosUnix ( nombre, passwd, basedn, servidor )

		uidNUmber =  (unixConn.getLasId () +1)

		objectClass = [
			"inetOrgPerson",
			"posixAccount",
			"Person",
			"OrganizationalPerson",
			"shadowAccount",
			"mailrecipient",
			"inetmailuser",
			"inetlocalmailrecipient",
			"inetUser",
			"apple-user",
			"userPresenceProfile",
			"DTSCUser",
			"krbPrincipalAux",
			"krbTicketPolicyAux"
		]

		#"ipUser",
		attributes = {
			"givenName": "Luis",
			"sn": "Pérez",
			"uid":"ramona",
			"loginShell":"/bin/bash",
			"employeetype":"otros",
			"userPassword":"patata",
			"mailQuota":10737418240,
			"mailUserStatus":"Active",
			"inetUserStatus":"Active"
		}

		attributes['homeDirectory'] = ( '/export/usuarios01/%s' % attributes['uid'] )
		attributes['cn']  = ('%s, %s' % (attributes['givenName'], attributes['sn']))
		attributes['uidNumber'] = str(uidNUmber)
		attributes['gidNumber'] = 100
		attributes['mail'] = ('%s@tsc.uc3m.es' % attributes['uid'] )
		attributes['apple-generateduid'] = str(uuid.uuid1()).upper()


		userUid = ('uid=%s,%s' % (attributes['uid'], basedn))


		unixConn.createUser (userUid, objectClass, attributes)

		import ipdb ; ipdb.set_trace()

		#adConn.createUser (attributes)



