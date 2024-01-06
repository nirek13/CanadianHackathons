#Import all of the libaries
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask_bootstrap import Bootstrap4, Bootstrap5
from flask import Flask, render_template

#Get the Data from Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

ID = "14idxG2e0n9WdDR35Ae-0APELlpl3sSNZvhRK_r1UR90"



def main():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()


    result = (
        sheet.values()
        .get(spreadsheetId=ID, range='hackathons',
      majorDimension='ROWS', valueRenderOption = 'FORMATTED_VALUE').execute()
    )
    values = result.get("values", [])


    if not values:
      values = ""
  except HttpError as err:
    print(err)

  return values[4:]


sheet_data = main()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

@app.route("/")
def hello_world():
    return render_template("home.html", list = sheet_data)



if __name__ == '__main__':
    app.run(debug=False)