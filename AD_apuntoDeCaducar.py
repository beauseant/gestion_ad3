
import lib.gestionUsuarios as ad
from lib import sendMail
import configparser
import argparse

if __name__ == "__main__":

	parser	= argparse.ArgumentParser ( description='Gestion de un Active Directory desde python. Muestra informacion de usuario y pone caducidad a la cuenta' )

	parser.add_argument('config'  , action = "store", metavar='config', type=str, help='fichero de configuracion')
	



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


		adConn 	= ad.gestionUsuariosAD ( nombre, domain, passwd, basedn, servidor )
		#users = adConn.listAllUsers ( attributes = ['cn','whenChanged', 'whenCreated', 'sAMAccountName', 'sn', 'name', 'lastLogon', 'accountExpires'] )

		#usersExpired = adConn.listExpired (  )

		days = 90

		usersExpired 	= adConn.listExpiredIn ( days=days, attributes = ['cn','sAMAccountName','accountExpires'] )
		usersExpired2 	= [ '%s,(%s),%s' % (user['cn'],user['sAMAccountName'], user['accountExpires']) for user in usersExpired ]



		try:
			username = cfg.get('CORREO', 'usuario')
			pwd = cfg.get ('CORREO','passwd')
			server = cfg.get ('CORREO','servidor')


			sm = sendMail.sender ( username=username, host=server, pwd = pwd)

			subject = ('Listado de cuentas a punto de caducar en %s días' % days)

			#import ipdb ; ipdb.set_trace()

			body = '\n'.join(usersExpired2)

			
			from_addr 		= cfg.get ('CORREO','from')
			to_addr_list 	=  [cfg.get ('CORREO','from')]

			errors = sm.sent (subject=subject, body=body, from_addr=from_addr, to_addr_list = to_addr_list,cc_addr_list=[])
			

			if errors:
				print ('Sending mail problems, %s' % errors)


			subject = ('Su cuenta caducará en %s días' % days)

			errors = []

			
			for user in usersExpired:
				to_addr_list = [ user['sAMAccountName'] ]

				body = cfg.get ('CORREO', 'texto').replace ('--login--', user['cn']).replace('--salto--','\n')

				error = sm.sent (subject=subject, body=body, from_addr=from_addr, to_addr_list = to_addr_list,cc_addr_list=[])
				errors.append(error)
			
		except Exception as E:
			print ('Error sending mail: %s' % E)
			exit()