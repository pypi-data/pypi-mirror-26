#!/usr/bin/python3
doc = """tosheets, send stdin to your google sheets

Usage:
  tosheets -c <cell>  [-s <sheet>] [--spreadsheet=<spreadsheet>] [-d <delimiter>]
  tosheets (-h | --help)
  tosheets --version

Options:
  -h --help                     Prints help.
  --version                     Show version.
  -c CELL                       Start appending to CELL.
  -s SHEET                      Use sheet name SHEET, otherwise tries to use 
                                TOSHEETS_SHEET (default: first visible sheet). 
  -d DELIMITER                  Use DELIMITER to split each line (default: whitespace).
  --spreadsheet=<spreadsheet>   Send to the spreadsheet identified by spreadshetId 
                                (ie. docs.google.com/spreadsheets/d/<spreadsheetId>/...), 
                                if empty uses TOSHEETS_SPREADSHEET enviroment variable.
"""
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from docopt import docopt

import pkg_resources

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = pkg_resources.resource_filename(__name__, "client.json")
APPLICATION_NAME = 'tosheets'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-tosheets.json')

    store = Storage(credential_path)
    credentials = store.get()
    sys.argv = ['']
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def appendToSheet(values, spreadsheetId, rangeName):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

#    values = [[1,2,3],
#              [4,5,6]]
#    spreadsheetId = '1xF8oFP-QYgPV0AF0dzYSQe9PYj6BWlLanh_0Vc33JFc'
#    rangeName = 'Sheet3!C5'
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range=rangeName,
            valueInputOption='RAW', body = {'values': values}).execute()
    except Exception as e:
        print(e)
        exit(1)
    exit(0)

def tryToConvert(x):
  try:
     return int(x)
  except ValueError:
    try:
      return float(x)
    except ValueError:
      return x.strip()
def main():
    arguments = docopt(doc, version='tosheets 0.1')
    spreadsheetId = arguments['--spreadsheet']
    if spreadsheetId is None:
        if not "TOSHEETS_SPREADSHEET" in os.environ:
            print("TOSHEETS_SPREADSHEET is not set and --spreadsheet was not given")
            exit(1)
        spreadsheetId = os.environ['TOSHEETS_SPREADSHEET']
    cell = arguments['-c'] 
    sheet = arguments['-s']
    if sheet is None:
        if not "TOSHEETS_SHEET" in os.environ:
          sheet = ""
        else:
          sheet = os.environ['TOSHEETS_SHEET'] + "!"
    else:
        sheet += "!"
    seperator = arguments['-d']
    values = []
    for line in sys.stdin:
        values.append(list(map(tryToConvert, line.split(seperator))));

    appendToSheet(values, spreadsheetId, sheet + cell)

if __name__ == '__main__':
    main()

