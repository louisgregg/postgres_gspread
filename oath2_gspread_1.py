import gspread
import config #import from local config file. 
from oauth2client.service_account import ServiceAccountCredentials

def gd_login():
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(config.account1_oauth2_credentials_json, scope)
	try:
		gc = gspread.authorize(credentials)
	except Exception, e:
		print "Error with google docs authentication %s" % e
		exit(1)
	return gc    

