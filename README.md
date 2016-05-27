# postgres_gspread
Python script to Transfer data from a Postgres table to a Google spreadsheet.

#Setup
Enable the Google Drive api and create service account credentials which gspread will use to connect to your Google Drive. Gspread offer a clear guide on how to do this, located here: http://gspread.readthedocs.io/en/latest/oauth2.html
Fill out the config file.

#Config file format 
The information of the Postgres table (host, database, tablename, etc.) and the information of the Google spreadsheet (location of Oauth2 credentials file, spreadsheet name, etc.) are specified in python dict format in a config file.  This file should be titled config.py. Look at the sample_config.py to see the structure. 

#Limitations. 
This script cannot CREATE Google spreadsheets in YOUR Google Drive account. It's scope is limited to 
'https://spreadsheets.google.com/feeds', which only allows the application to edit documents that already exist. 
...A possible workaround for this is to change the scope to 'https://www.googleapis.com/auth/drive', which 
allows the creation and deletion of files in Google Drive. **However, it can only create files in the Google Drive of the service account created to generate the certificate.** This file must then be shared to people who want to view the spreadsheet, either individually or by domain (e.g. shared to every user@CompanyDomain.com). This issue was addressed by the Github user  **miohtama**, and you can find the script they wrote here: https://gist.github.com/miohtama/f988a5a83a301dd27469

#Future work
 

Expand the config file and alter the script to allow for multiple Postgres and Google sheets configs in the config file, which could be specified as arguments at runtime. 



