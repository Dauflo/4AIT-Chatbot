import random
import dialogflow_client_api

PHRASE_DIR = 'dialog/'

BOT_NAME = 'Traves Lers'
INTRODUCTION = 'introduction.txt'
INTRODUCTION_QUESTION = 'introduction_question.txt'
SPECIFIC_QUESTION = 'specific_'

def specific_question_ask(action):
    print('%s : %s' % (BOT_NAME, display_file_content('%s%s.txt' % (SPECIFIC_QUESTION, action))))
    return

def process_specific_ask(data):
    for k, v in data.items():
        if not v:
            specific_question_ask(k)
    return

def update_travel_data(data):
    return data

def user_input():
    user_entry = input('Dites à Traves ce dont vous avez besoin : ')
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

    # phrase = user_input()
    phrase = 'Je cherche une villa pour 1 mois et demi'
    travel_data = None
    print()

    while(not travel_data):
        travel_data = dialogflow_client_api.request(phrase)
        print(travel_data)
        
    process_specific_ask(travel_data)
    return

main()