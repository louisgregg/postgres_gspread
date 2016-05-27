#Modules for interacting with Postgres.
import psycopg2 
import petl

#Modules for interacting with Google.
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import time
import numpy
from sys import exit

import config #import connection information from local config file. 


def pgsql_connect():
    """
    This method creates a connection to the postgresql database 
    based on the info supplied in the config file.
    """
    try:
        service = psycopg2.connect(database=config.postgres_info['database'],
                                   user=config.postgres_info['username'],
                                   password=config.postgres_info['password'],
                                   host=config.postgres_info['host'],
                                   port=config.postgres_info['port'])
    except Exception, e:
        print "Error connecting to database: %s " % e
        exit(1)
    return service


def gd_login():
    """
    This method returns a gspread connection to Google Sheets
    based on the info supplied in the config file. 
    """
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.google_info['account1_oauth2_credentials_json'], scope)
    try:
    	gc = gspread.authorize(credentials)
    except Exception, e:
    	print "Error with google docs authentication %s" % e
    	exit(1)
    return gc    

def pg_extract(service):
    """
    Returns the full contents of a postgresql table
    :param service:  object with the pgsql connection service
    :return: data
    """
    schema=config.postgres_info['schema']
    table=config.postgres_info['table']
    try:
        data = petl.fromdb(service, 'SELECT * FROM %s.%s;' %(schema, table))
    except Exception, e:
        print "Error extracting data from postgres %s.%s %s" % (schema, table, e)
        service.rollback()
        exit(1)
    return data

    
def number_to_letter(n):
    """
    This method converts a number >0 and <= 702 to its alphabet equivalent. 
    This is necessary, as in order to define a range of Google spreadsheet 
    worksheet cell values, the number of columns has to be specified in the
    cell reference format of a1 (x=1, y=1), a2(x=2, y=2)...ZZ??(x= 702, y=??).
    """
    if n <= 0:
        print "The number of columns submitted is <= 0"
        exit(1)
    elif n > 702:
        print "The number of columns submitted is > 702 (corresponding to column label ZZ). I should edit the connector code to support more columns - Louis"
        exit(1)
    elif n <= 26:
        C = chr( (n-1) + ord('A') )
    elif n > 26:

        if n%26 == 0:
            c1 = ( n / 26 ) - 1
            c1 = chr( (c1-1) + ord('A') )
            c2 ='Z'
        if n%26 != 0:   
            c1 = ( (n-(n%26)) / 26 )
            c1 = chr( (c1-1) + ord('A') )
            c2 = (n%26)
            c2 = chr((c2-1) +ord('A'))
        C = c1+c2
    return(C)

def gd_upload(gspread_service, postgres_data):
    """
    Attempts to upload the data obtained from the Postgres table to 
    the Google spreadsheet. 
    :param gspread_service: object with the gspread service.
    :param postgres_data:  Python list-of-lists of data from postgres table. 
    :return: data
    """
    spreadsheet_title=config.google_info['spreadsheet_title']
    worksheet_title=config.google_info['worksheet_title']
    try:
    	spreadsheet_object = gspread_service.open(spreadsheet_title)
    except Exception, e:
        print "Error opening the spreadsheet corresponding to the title %s: %s" % (spreadsheet_title, e)
        exit(1)

    #Check if worksheet already exists. 
    #Delete it if it exists or continue if it doesn't. 
    try:
        worksheet_temp = spreadsheet_object.worksheet(worksheet_title)
        spreadsheet_object.del_worksheet(worksheet_temp)
    except gspread.exceptions.WorksheetNotFound:
        pass

        #create the worksheet in the spreadsheet object
    worksheet_object = spreadsheet_object.add_worksheet(title=worksheet_title, rows=str(len(postgres_data)), cols=str(len(postgres_data[0])))

    #Fill the worksheet from the first cell. 
    first_cell_index = "A1"
    
    last_cell_index =  number_to_letter(len(postgres_data[0]))+str(len(postgres_data))
    
    
    #Range of cell values to be filled is defined in 
    #the format displayed on the sheet (e.g. "A1:C9") 
    cell_list = worksheet_object.range(first_cell_index+":"+last_cell_index)
    
    #convert the list-of-lists of postgres data into a 
    #flattened numpy array in order to facilitate easier indexing 
    #when filling the list of cell object values. 
    cell_values = numpy.array(postgres_data)
    cell_values = cell_values.flat
    

    
    i=0
    for i in range(0,len(cell_values)):
        cell_list[i].value = cell_values[i]
        
    worksheet_object.update_cells(cell_list)

def main():
    #connect to the postgresql database.
    pg = pgsql_connect()

    # connect to google docs.
    gd = gd_login()

    #obtains the data from the postgres table. 
    postgres_data = pg_extract(pg)

    #upload the retrieved postgres data to the a worksheet generated in the spreadsheet specified. 
    gd_upload(gd, postgres_data)

if __name__ == '__main__':
    main()