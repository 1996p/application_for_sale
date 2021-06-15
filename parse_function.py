import requests
from bs4 import BeautifulSoup
import json
import sqlite3 as sql
import datetime
import logging


func_log = logging.getLogger('user_func')
func_log.setLevel(logging.INFO)
func_fh = logging.FileHandler('logs/logs.log', 'a', 'utf-8')
func_formatter = logging.Formatter(f"%(asctime)s - %(levelname)s - %(message)s")
func_fh.setFormatter(func_formatter)
func_log.addHandler(func_fh)


def lookup(steam_url):

    r = requests.post('https://steamid.io/lookup', data={'input': steam_url})

    if r.status_code == 200:

        soup = BeautifulSoup(r.text, 'html.parser')
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        data = json.loads(script_tag.string.strip().replace(';', ''))
        steamids = data['keywords'].split(', ')
        return {'steamIDf': steamids[1], 'steamID3': steamids[2], 'steamID64': steamids[3]}


def add_to_db(account_link, login, password):
    now = datetime.datetime.today().strftime("%Y-%m-%d, %H:%M")


    headers = {
        'Accept': '*/*',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56"

    }
    steam_id = lookup(account_link)['steamID64']

    r = requests.get(url=f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=A4504B0054A88C13E967B6C0CFA66E01&steamid={steam_id}&format=json')
    jsonstr = r.text
    data = json.loads(jsonstr)

    if data == {'response': {}}:
        raise NameError
    else:
        list_of_games_url = f"{account_link}games/?tab=all"

        r = requests.get(url=account_link, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        steam_lvl = soup.find('div', class_='friendPlayerLevel').text

        with sql.connect('accounts.db') as con:
            cur = con.cursor()
            cur.execute(f'INSERT INTO info (link) VALUES ("{account_link}")')
            cur.execute(f'UPDATE info SET "login" = "{login}" WHERE link == "{account_link}"')
            cur.execute(f'UPDATE info SET "password" = "{password}" WHERE link == "{account_link}"')
            cur.execute(f'UPDATE info SET "time_of_add" = "{now}" WHERE link == "{account_link}"')


        with sql.connect('accounts.db') as con:
            cur = con.cursor()
            cur.execute(f'UPDATE info SET "level" = "{steam_lvl}" WHERE link == "{account_link}"')

        # steam_id = lookup(account_link)['steamID64']
        with sql.connect('accounts.db') as con:
            cur = con.cursor()
            cur.execute(f'UPDATE info SET "id64" = "{steam_id}" WHERE link == "{account_link}"')


        games_count = data['response']['game_count']
        with sql.connect('accounts.db') as con:
            cur = con.cursor()
            cur.execute(f"UPDATE info SET games == {games_count} WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID
        games_id = []
        for i in range(0, games_count):
            games_id.append(data['response']['games'][i]['appid'])


        if 221100 in games_id:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET dayz == 1 WHERE link == '{account_link}'") #Добавить условие, где будет соответствовать SteamID
        else:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET dayz == 0 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID



        if 578080 in games_id:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET pubg == 1 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID
        else:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET pubg == 0 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID



        if 252490 in games_id:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET rust == 1 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID
        else:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET rust == 0 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID



        if 359550 in games_id:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET r6 == 1 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID
        else:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET r6 == 0 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID



        if 730 in games_id:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET csgo == 1 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID
        else:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET csgo == 0 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID


        get_banned = None
        r = requests.get(url=account_link, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        ban = soup.find('div', class_='profile_ban')


        if ban is not None:
            get_banned = True
        else:
            get_banned = False

        if get_banned is True:
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                cur.execute(f"UPDATE info SET ban == 1 WHERE link == '{account_link}'")  # Добавить условие, где будет соответствовать SteamID

        return True
# add_to_db('https://steamcommunity.com/profiles/76561198158336922', '4eva', 'unkxnom')

def request_to_db(account_link= '', login='', password='', games_count='', lvl = '', dayz=False, rust=False, pubg=False, r6=False, csgo=False, get_banned=False):
    now = datetime.datetime.today().strftime("%Y-%m-%d, %H:%M")
    if account_link != '' and login != '' and password != '':
        return 404
    #elif account_link == '' and login == '' and password == '' and lvl = '' and dayz=False and rust=False, pubg=False, r6=False, csgo=False, get_banned=False


    if account_link != '':
        log_link = account_link
        account_link = f'link == "{account_link}" and '

    if password != '':
        log_password = password
        password = f'password == "{password}" and '

    if login != '':
        log_login = login
        login = f'login == "{login}" and '

    if games_count != '':
        games_count = f'games >= {games_count} and '

    if lvl != '':
        lvl = f'level >= "{lvl}" and '

    if dayz:
        dayz = f'dayz == 1 and '
    else:
        dayz = ''

    if rust:
        rust = f'rust == 1 and '
    else:
        rust = ''

    if pubg:
        pubg = f'pubg == 1 and '
    else:
        pubg =''

    if r6:
        r6 = f'r6 == 1 and '
    else:
        r6 =''

    if csgo:
        csgo = f'csgo == 1 and '
    else:
        csgo = ''

    if get_banned:
        get_banned = f'ban == 1 and '
    else:
        get_banned = ''

    conditions = account_link + login + password + games_count + lvl + dayz + rust + pubg + r6 + csgo + get_banned
    with sql.connect('accounts.db') as con:
        cur = con.cursor()

        if account_link == '' and login == '' and password == '':
            func_log.info(f"""
            Find account without filters!
            """)
            with sql.connect('accounts.db') as con:
                cur = con.cursor()
                for i in range(0, 5000):
                    # print(f'testing rowid = {i}')
                    request = f'''SELECT r6, csgo, pubg, rust, dayz, link, login, password, games, level FROM info WHERE {conditions}sold == 0 and rowid == "{i}" '''
                    cur.execute(request)
                    result = cur.fetchall()
                    if result != []:
                        print(result)
                        cur = con.cursor()
                        cur.execute(f'UPDATE info SET sold = 1, time_of_sale = "{now}" WHERE {conditions}rowid == "{i}"')
                        cur.execute(f'UPDATE time SET last_sale = "{now}"')
                        break
                    if i == 4999:
                        return 405
            return 0, result

        elif account_link != '' and login == '' and password == '':
            func_log.info(f"""
            Find account with link filter!
            link:{log_link}
            """)
            request = f'''SELECT r6, csgo, pubg, rust, dayz, login, password, sold, games, level FROM info WHERE {conditions}'''
            request = request[0:-5]
            cur.execute(request)
            result = cur.fetchall()
            if result != [] and result[0][2] != '1':
                print(result)
                cur = con.cursor()
                sold_request = f'UPDATE info SET sold = 1, time_of_sale = "{now}" WHERE {conditions}'
                sold_request = sold_request[0:-5]
                cur.execute(sold_request)
                cur.execute(f'UPDATE time SET last_sale = "{now}"')
                return 1, result

            elif result[0][2] == 1:
                print('account already sold')

        elif account_link != '' and login != '' and password == '':
            func_log.info(f"""
                Find account with link + login filter!
                link:{log_link},
                login: {log_login}
                """)
            request = f'''SELECT r6, csgo, pubg, rust, dayz, password, sold, games, level FROM info WHERE {conditions}'''
            request = request[0:-5]
            cur.execute(request)
            result = cur.fetchall()
            if result != [] and result[0][1] != '1':
                cur = con.cursor()
                sold_request = f'UPDATE info SET sold = 1, time_of_sale = "{now}" WHERE {conditions}'
                sold_request = sold_request[0:-5]
                cur.execute(sold_request)
                cur.execute(f'UPDATE time SET last_sale = "{now}"')
                return 2, result

            elif result[0][1] == 1:
                print('account already sold')

        elif account_link != '' and login == '' and password != '':
            func_log.info(f"""
                    Find account with link + password filter!
                    link:{log_link},
                    password: {log_password}
                    """)
            request = f'''SELECT r6, csgo, pubg, rust, dayz, login sold, games, level FROM info WHERE {conditions}'''
            request = request[0:-5]
            cur.execute(request)
            result = cur.fetchall()
            if result != [] and result[0][1] != '1':
                print(result)
                cur = con.cursor()
                sold_request = f'UPDATE info SET sold = 1, time_of_sale = "{now}" WHERE {conditions}'
                sold_request = sold_request[0:-5]
                cur.execute(sold_request)
                cur.execute(f'UPDATE time SET last_sale = "{now}"')
                return 3, result

            elif result[0][1] == 1:
                print('account already sold')

        elif account_link == '' and login != '' and password == '':
            func_log.info(f"""
                    Find account with login filter!
                    login: {log_login}
                    """)
            request = f'''SELECT r6, csgo, pubg, rust, dayz, link, password, sold, games, level FROM info WHERE {conditions}'''
            request = request[0:-5]
            cur.execute(request)
            result = cur.fetchall()
            print(result)
            if result != [] and result[0][2] != '1':
                cur = con.cursor()
                sold_request = f'UPDATE info SET sold = 1, time_of_sale = "{now}" WHERE {conditions}'
                sold_request = sold_request[0:-5]
                cur.execute(sold_request)
                cur.execute(f'UPDATE time SET last_sale = "{now}"')
                return 4, result
            elif result[0][2] == 1:
                print('account already sold')

        elif account_link == '' and login != '' and password != '':
            func_log.info(f"""
                    Find account with login + password filter!
                    login: {log_login},
                    password: {log_password}
                    """)
            request = f'''SELECT r6, csgo, pubg, rust, dayz, link, sold, games, level FROM info WHERE {conditions}'''
            request = request[0:-5]
            cur.execute(request)
            result = cur.fetchall()
            if result != [] and result[0][1] != '1':
                print(result)
                cur = con.cursor()
                sold_request = f'UPDATE info SET sold = 1, time_of_sale = "{now}" WHERE {conditions}'
                sold_request = sold_request[0:-5]
                cur.execute(sold_request)
                cur.execute(f'UPDATE time SET last_sale = "{now}"')
                return 5, result
            elif result[0][1] == 1:
                print('account already sold')

def accounts_have():
    with sql.connect('accounts.db') as con:
        cur = con.cursor()
        cur.execute(f'SELECT SUM(accounts_have), SUM(sold) FROM "info"')
        result = cur.fetchone()
        sold = result[1]
        accounts_left = result[0] - sold
        cur.execute('SELECT last_sale FROM "time"')
        last_sale = cur.fetchone()
        print(last_sale)
        return accounts_left, sold, last_sale


print(accounts_have())






