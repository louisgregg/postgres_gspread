"""
Sample config file for the postgres_gspread connector.
Fill out the  google_info and postgres_info dict objects below with your info and save
the file as config.py in the same directory as the postgres_gspread_1.py file.
"""
#Here is the information of the Google spreadsheet and worksheet to which we wish to transfer data. 
google_info=dict(
	#Point to service_account json file contraining the credentials for your Google Drive account. 
	account1_oauth2_credentials_json='path/to/service_credentials_file.json', 
	spreadsheet_title='my_spreadsheet',
	worksheet_title='my_worksheet'
	)

#Here is the info related to the POSTGRES table. 
postgres_info=dict(
	database='my_database',
	username='my_username',
	password='my_password',
	host='my_postgres_servers_ip', #127.0.0.1 maybe?
	port='5432', #default port for postgres
	schema='public', #postgres schema for our table. This might be private. 
	table='table_name') #Postgres table from which we wish to extract data. 	

