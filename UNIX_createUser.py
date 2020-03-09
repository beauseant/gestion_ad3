
import lib.gestionUsuarios as ad
from lib import sendMail
import configparser
import argparse
import json
import uuid



if __name__ == "__main__":

	parser	= argparse.ArgumentParser ( description='Gestion de un Active Directory desde python. Muestra informacion de usuario y pone caducidad a la cuenta' )

	parser.add_argument('config'  , action = "store", metavar='config', type=str, help='fichero de configuracion')
	parser.add_argument('obectClass'  , action = "store", metavar='config', type=str, help='fichero json con el objectClass')
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


		try:

			with open(args.obectClass) as json_file:
				objectClass = json.load(json_file)


			with open(args.userData) as json_file:
				attributes = json.load(json_file)


			attributes['homeDirectory'] = ( '/export/usuarios01/%s' % attributes['uid'] )
			attributes['cn']  = ('%s %s' % (attributes['givenName'], attributes['sn']))
			attributes['uidNumber'] = str(uidNUmber)
			attributes['gidNumber'] = 100
			attributes['mail'] = ('%s@tsc.uc3m.es' % attributes['uid'] )
			attributes['apple-generateduid'] = str(uuid.uuid1()).upper()
			attributes['krbPrincipalName'] = ('%s@TSC.UC3M.ES'% (attributes['uid']))

			userUid = ('uid=%s,%s' % (attributes['uid'], basedn))


			unixConn.createUser (userUid, objectClass, attributes)

			print ('Usuario %s creado con el id %s' % ( attributes['uid'], uidNUmber ) )

		except Exception as E:
			print ('todo mal: %s' % E)

		#adConn.createUser (attributes)



