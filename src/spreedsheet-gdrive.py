import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("juegostmybl-465eb052fdb8.json", scope)
client=gspread.authorize(creds)

sheet = client.open("JuegosTMyBL").sheet1

sheet.update_acell('B1', 'Bingo2!')
