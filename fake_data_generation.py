import datetime
import json
import random

def check_city(city, data):
    for data_city in data:
        if city.lower() == data_city.lower():
            return True
    return False

# Use to generate coherent fake data, in prodcution env, this would be an API call to a booking API
def create_fake_data(city='', number_of_person=0, place='', date='', duration=0):
    data = None
    with open('data.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    number_of_result = random.randint(3, 8)

    travel_results = []

    for i in range(number_of_result):
        travel = {}

        # SETUP CITY, if not exist, then take a random one from data
        if city and check_city(city, data['city']):
            travel['city'] = city.capitalize()
        else:
            travel['city'] = random.choice(data['city'])

        # SETUP PLACE, if not exist, then take a random one from data
        if place and place.lower() in data['place']:
            travel['place'] = place
        else:
            travel['place'] = random.choice(data['place'])

        # SETUP NUMBER OF PERSON, if equal 0, then generate a random number of person
        if number_of_person != 0:
            travel['numberOfPerson'] = random.randint(number_of_person - 1, number_of_person + 1)
        else:
            travel['numberOfPerson'] = random.randint(1, 5)

        # SETUP DURATION, if equal 0, then generate a random one
        # Unit : day
        if duration != 0 and duration != '':
            travel['duration'] = duration
        else:
            travel['duration'] = random.randint(7, 30)

        # SETUP DATE, if not exist, then generate a random one

        if date:
            date = date.split('T')[0]
            date_infos = date.split('-')
            final_date = datetime.datetime(int(date_infos[0]), int(date_infos[1]), int(date_infos[2]))
            final_date += datetime.timedelta(days=random.randint(-5, 5))
            travel['date'] = final_date.strftime('%d-%m-%Y')
        else:
            final_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(0, 30))
            travel['date'] = final_date.strftime('%d-%m-%Y')

        travel_results.append(travel)

    return travel_results