"""Previously it gives link to authorization in vk app to get your permissions. Then you confirm and give received link
from address bar, program will start get your vk friends and next theirs friends. All friends with theirs id,
first name, last name will be saved on itogdata.txt file."""

import requests
import time
from urllib.parse import urlencode, urlparse

start_time = time.time()

AUTORIZE_URL = 'https://oauth.vk.com/authorize'
APP_ID = '7366895'
VERSION = '5.103'

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends,status',
    'v': VERSION,
}
"""получение ключа доступа - токена."""
print('перейдите по ссылке и разрешите доступ приложению к данным вашего аккаунта,\nзатем скопируйте ссылку из адресной строки:')
print('?'.join((AUTORIZE_URL, urlencode(auth_data))))
print('введите ссылку из адресной строки вашего браузера: ')
TOKENvk = input('')

"""получение списка друзей"""
parse_URL = urlparse(TOKENvk)
chapters = dict((a.split('=') for a in parse_URL.fragment.split('&')))
access_token = chapters['access_token']
USER_ID = chapters['user_id']
params = {'access_token': access_token,
          'user_id': USER_ID,
          'v': VERSION}
response = requests.get('https://api.vk.com/method/friends.get', params)

"""получение информации о людях из списка друзей и запись их в промежуточный файл 'vivod.txt'"""
x = response.json()['response']
dlina = 0
for y in x.get('items'):
    params = {'access_token': access_token,
              'user_id': y,
              'v': VERSION}
    response = requests.get('https://api.vk.com/method/users.get', params)
    dlina += 1
    print('записываю друга №', dlina)
    zx = response.json()['response']
    with open('vivod.txt', 'a', encoding='utf-8') as za:
        for nutr in zx:
            for data in nutr:
                za.write(data)
                za.write(' ===> ')
                za.write(str(nutr[data]))
                za.write(', ')
            za.write('\n')
    time.sleep(0.33)
print('Закончил запись в текстовый файл')

"""получение из 'vivod.txt' айди друзей с открытыми профилями"""
aydi = []
try:
    with open('vivod.txt', 'r', encoding='utf-8') as f:
        for line in f:
            d = line
            d = d.rstrip()
            s = d.split(',')
            filtr = s[3]
            c = filtr.split(' ===> ')[1]
            c = str(c)
            if c == 'False':
                o = s[0]
                i = o.split(' ===> ')[1]
                aydi.append(i)
            else:
                continue
except ImportError:
    pass
print(aydi)
print('Закончил обработку данных. Айди с открытыми профилями получено:', len(aydi))


"""получение списка друзей друзей, получение информации о них и запись их в промежуточный файл 'vivod.txt'"""
for aydis in aydi:
    print('получение списка друзей для друга с айди:', aydis)
    params = {'access_token': access_token,
              'user_id': aydis,
              'v': VERSION}
    response = requests.get('https://api.vk.com/method/friends.get', params)
    x = response.json()['response']
    time.sleep(0.33)
    dlina = 0
    for y in x.get('items'):
        params = {'access_token': access_token,
                  'user_id': y,
                  'v': VERSION}
        response = requests.get('https://api.vk.com/method/users.get', params)
        dlina += 1
        print('записываю друга №', dlina)
        zx = response.json()['response']
        with open('vivod.txt', 'a', encoding='utf-8') as za:
            for nutr in zx:
                for data in nutr:
                    za.write(data)
                    za.write(' ===> ')
                    za.write(str(nutr[data]))
                    za.write(', ')
                za.write('\n')
        time.sleep(0.33)
print('Закончил запись друзей "Х2" в промежуточный файл')

"""Фильтрация на повторения во временном файле и запись уникальных данных в конечный файл 'itogdata.txt'"""
sohraydi = []
with open('vivod.txt', 'r', encoding='utf-8') as ch:
    for line in ch:
        s = line.split(',')
        filtr = s[0]
        c = filtr.split(' ===> ')[1]
        if c not in sohraydi:
            sohraydi.append(c)
            with open('itogdata.txt', 'a', encoding='utf-8') as zz:
                zz.write(line)
        else:
            continue

print('Парсинг друзей твоих друзей завершён, было найдено: ', len(sohraydi), 'уникальных профилей ВК.\n На это было затрачено:', "--- %s seconds ---" % (time.time() - start_time))
