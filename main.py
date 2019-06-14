import random
import dialogflow_client_api
import fake_data_generation

PHRASE_DIR = 'dialog/'

BOT_NAME = 'Traves Lers'
INTRODUCTION = 'introduction.txt'
INTRODUCTION_QUESTION = 'introduction_question.txt'
SPECIFIC_QUESTION = 'specific_'

FAKE_PHRASE = 'Je veux une maison '

# Function used to convert duration (day) to metric like : mounth, week, day
def duration_converteur(duration):
    mounth = 0
    week = 0
    day = 0

    while duration >= 30:
        mounth += 1
        duration -= 30

    while duration >= 7:
        week += 1
        duration -= 7
    
    day = duration

    final_duration = ''
    if mounth > 0:
        final_duration += '%i mois ' % mounth
    if week > 0:
        final_duration += '%i semaine(s) ' % week
    if day > 0:
        final_duration += '%i jour(s)' % day
    return final_duration

def show_possibilities(travels):
    for travel in travels:
        print('=' * 20)
        print('Ville : %s' % travel['city'])
        print('Type de résidence (villa, hôtel...) : %s' % travel['place'])
        print('Nombre de personnes possible : %i' % travel['numberOfPerson'])
        print('Date de début %s' % travel['date'])
        print('Durée de la réservation : %s' % duration_converteur(travel['duration']))
        print("=" * 20)
    return

def specific_question_ask(action):
    print('%s : %s' % (BOT_NAME, display_file_content('%s%s.txt' % (SPECIFIC_QUESTION, action))))

def process_specific_ask(data):
    for k, v in data.items():
        if not v:
            specific_question_ask(k)
            data[k] = user_input(k)
    print(data)
    travels = fake_data_generation.create_fake_data(data['city'], data['numberOfPerson'], data['place'], data['date'], data['duration'])
    show_possibilities(travels)

def user_input(option='none'):
    user_entry = input('Vous : ')
    
    if option == 'numberOfPerson':
        try:
            if not user_entry:
                return 0
            user_entry = int(user_entry)
            return user_entry
        except Exception:
            print('Merci de donner un nombre valide de personnes')
            return user_input(option)
    elif option == 'date':
        data = dialogflow_client_api.request(FAKE_PHRASE + user_entry)
        return data['date']
    elif option == 'duration':
        data = dialogflow_client_api.request(FAKE_PHRASE + user_entry)
        return data['duration']
    else:
        return user_entry

def display_file_content(file_name):
    f = open(PHRASE_DIR + file_name, 'r', encoding='utf-8')
    data = f.readlines()
    return random.choice(data).strip()

def introduction():
    print('%s : %s' % (BOT_NAME, display_file_content(INTRODUCTION)))
    return

def introduction_question():
    print('%s : %s' % (BOT_NAME, display_file_content(INTRODUCTION_QUESTION)))
    return

def main():
    # Say hello to user and ask if he can help
    introduction()
    introduction_question()

    phrase = user_input()
    travel_data = None
    print()

    while(not travel_data):
        travel_data = dialogflow_client_api.request(phrase)
        print(travel_data)
        
    process_specific_ask(travel_data)

main()