#!/usr/local/bin/python3
import requests
import json
import argparse
from pathlib import Path
from getpass import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

main_url="https://URL_OF_THE_SITE/"
dis_url="https://URL_OF_THE_SITE/api/discussions"
post_url="https://URL_OF_THE_SITE/api/posts"
login_url="https://URL_OF_THE_SITE/login"

headers = {
    'Host': 'URL_OF_THE_SITE',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
}
session_cookies=""
session_token=""
user=""
password=""
logged=0
pagefetch=0
bot=requests.session()
credentials={}
session_cookies=""
session_token=""

def read_session():
    global session_token
    global session_cookies
    global pagefetch
    with open('config.json', 'r') as f:
        config = json.load(f)
        pagefetch=1
        logged=1
        print("Using previous session")
    session_token=config.get("X-CSRF-Token")
    session_cookies=config.get("Set-Cookie")
    
    
def get_session():
    global pagefetch
    global bot
    global credentials
    global session_token
    global session_cookies
    bot.headers.update(headers)
    page=bot.get(main_url, verify=False)
    if(page.status_code == 200):
        print("Succefully created session ID")
        session_cookies=page.headers.get("Set-Cookie")
        session_token=page.headers.get("X-CSRF-Token")
        config={"Set-Cookie":session_cookies,"X-CSRF-Token":session_token}
        pagefetch=1
    else:
        print("Unable to load webpage")
        pagefetch=0


def login():
    global bot
    global logged
    global session_token
    global session_cookies
    login_header={
        'Host': 'URL_OF_THE_SITE',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'DNT': '1',
        'X-CSRF-Token': session_token,
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://URL_OF_THE_SITE',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://URL_OF_THE_SITE/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': session_cookies[:55]
        }
    bot.headers.update(login_header)
    login_data=bot.post(login_url, json=credentials, verify=False)
    if(login_data.status_code == 200):
        print("Successfully logged in")
        session_token=login_data.headers.get("X-CSRF-Token")
        session_cookies=login_data.headers.get("Set-Cookie")
        config={"Set-Cookie":login_data.headers.get("Set-Cookie"),"X-CSRF-Token":login_data.headers.get("X-CSRF-Token")}
        with open('config.json', 'w') as f:
            json.dump(config, f)
        logged=1
    else:
        logged=0
    
def new_discussion(title, post, tags):
    global bot
    dis_headers={
        'Host': 'URL_OF_THE_SITE',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'DNT': '1',
        'X-CSRF-Token': session_token,
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Content-Type: application/json; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://URL_OF_THE_SITE',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://URL_OF_THE_SITE/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': session_cookies[:55]+' ;'+session_cookies[156:156+55]
    }
    bot.headers.update(dis_headers)
    result=bot.post(dis_url,json={"data":{"type":"discussions","attributes":{"title":title,"content":post},"relationships":{"tags":{"data":[{"type":"tags","id":tags}]}}}},verify=False)
    if(result.status_code == 201):
        print("Discussion successfully created")
    else:
        print("Failed to create discussion")

def new_post(dis_id, post):
    global bot
    post_headers={
        'Host': 'URL_OF_THE_SITE',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'DNT': '1',
        'X-CSRF-Token': session_token,
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://URL_OF_THE_SITE',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://URL_OF_THE_SITE',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': session_cookies[:55]+'; '+session_cookies[156:156+55]
    }
    bot.headers.update(post_headers)
    result=bot.post(post_url,json={"data":{"type":"posts","attributes":{"content":post},"relationships":{"discussion":{"data":{"type":"discussions","id":dis_id}}}}},verify=False)
    if(result.status_code == 201):
        print("Post successfully created")
    else:
        print("Failed to create post")
    


if Path('config.json').is_file():
    print ("Found previous session in config.json. If a new session is needed please delete config.json first.")
    read_session()
    
else:
    print ("Session not found. A new session will be created.")
    get_session()
    if(pagefetch == 1):
        user=input("Username / Email: ")
        password=getpass()
        credentials={"identification":user,"password":password,"remember":'true'}
        login()

