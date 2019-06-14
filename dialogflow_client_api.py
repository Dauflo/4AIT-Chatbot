import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict
import os
import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'e4ait-xetqjb-2e38d957b618.json'

PROJECT_ID = 'e4ait-xetqjb'
SESSION_ID = 'test'
LANGUAGE_CODE = 'fr-FR'

# Convert all api return to day duration
def day_conversion(amount, unit):
    if unit == 'jour':
        return amount
    elif unit == 'mois':
        return amount * 30
    elif unit == 'semaine':
        return amount * 7
    elif unit == 'heure':
        return int(amount / 24)
    return 0

def data_processing(data):

    final_data = {}

    final_data['duration'] = day_conversion(data['Duration']['amount'], data['Duration']['unit']) if data['Duration'] != '' else ''

    final_data['city'] = data['geo-city'] if data['geo-city'] != '' else ''

    final_data['numberOfPerson'] = data['NumberOfPerson'] if data['NumberOfPerson'] != '' else ''

    final_data['date'] = data['Date'] if data['Date'] != '' else ''

    final_data['place'] = data['VacationPlaces'] if data['VacationPlaces'] != '' else ''

    return final_data

def request(text):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(PROJECT_ID, SESSION_ID)

        text_input = dialogflow.types.TextInput(text=text, language_code=LANGUAGE_CODE)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)

        response = MessageToDict(response.query_result)

        if response['parameters']:
            data = data_processing(response['parameters'])
            return data

        return
    except Exception:
        print("Error with Dialogflow, service probably down, please wait a few minutes and retry. If still returning error, please contact me at 284994@supinfo.com")
        sys.exit()