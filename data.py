import json
from random import randint

def get_channel():
    with open("Stock.json", "r+") as file:
        data = json.load(file)
    return data['channel']

def add_channel(id):
    with open("Stock.json", "r+") as file:
        data = json.load(file)
        if not id in data['channel']:
            data['channel'].append(id)
            file.seek(0)
            json.dump(data, file, indent=4)
        else:
            return True

def _tclient():
    with open("Stock.json", "r+") as file:
        data = json.load(file)

    return data['bot_token']

def add_people(user: int):
    with open("Stock.json", "r+") as file:
        data = json.load(file)
        if not user in data['data']['user']:
            data['data']['user'].append(user)
            file.seek(0)
            json.dump(data, file, indent=4)
        else:
            return True


def get_people():
    with open("Stock.json", "r+") as file:
        data = json.load(file)

    return data['data']['user']


def remove_people(user):
    with open('Stock.json', 'r+') as files:
        data = json.load(files)
    with open('Stock.json', 'w') as file:
        x = data['data']['user']
        if user in x:
            x.remove(user)

        data['data']['user'] = x
        # file.seek(0)
        json.dump(data, file, indent=4)


def add_token(token):
    identifiant = randint(10000, 1000000000)
    with open("Stock.json", "r+") as file:
        data = json.load(file)
        data['token'][identifiant] = token
        file.seek(0)
        json.dump(data, file, indent=4)

        return identifiant


def get_id():
    with open("Stock.json", "r+") as file:
        data = json.load(file)
    return data['token']


def id_to_token(id):
    with open("Stock.json", "r+") as file:
        data = json.load(file)
    return data['token'][id]
