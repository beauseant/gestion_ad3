
import lib.gestionUsuarios as ad
from lib import sendMail
import configparser
import argparse
import json


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
			nombre 		= cfg.get ( 'AD','nombre')
			passwd 		= cfg.get ( 'AD','passwd')
			basedn		= cfg.get ( 'AD','basedn')
			servidor	= cfg.get ( 'AD','servidor')
			domain		= cfg.get ( 'AD','domain')

		except Exception as E:
			print (E)
			exit ()

		with open(args.userData) as json_file:
			attributes = json.load(json_file)


		adConn 	= ad.gestionUsuariosAD ( nombre, domain, passwd, basedn, servidor )

		adConn.createUser (attributes)



