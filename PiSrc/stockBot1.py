import requests
from bs4 import BeautifulSoup
import telepot
from telepot.loop import MessageLoop
import time
import pandas as pd
import os

my_token = '8122523141:AAE_XLPGXdpa_kcu0TUWnC62O5ZxIyMOP_E'
telegram_id = '5996719385'
bot = telepot.Bot(my_token)

def download_krx_stock_list(filepath='CORP_LIST.xlsx'):
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
    headers = { 'User-Agent' : 'Mozilla/5.0', 'Referer' : 'http://kind.krx.co.kr/'}
    res = requests.get(url, headers=headers)
    with open(filepath, 'wb') as f:
        f.write(res.content)

def get_stock_code(name, filepath='CORP_LIST.xlsx'):
    if not os.path.exists(filepath):
        download_krx_stock_list(filepath)
    df = pd.read_excel(filepath, dtype=str, engine='openpyxl')
    df['종목코드'] = df['종목코드'].str.zfill(6)
    result = df[df['회사명'] == name]

    if not result.empty:
        return result.iloc[0]['종목코드']
    else:
        return None

def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            return
        name = msg['text'].strip()
        code = get_stock_code(name)

        if code:
            price = get_price(code)
            bot.sendMessage(chat_id, f'{name} 현재가: {price}원 (코드: {code})')
        else:
            bot.sendMessage(chat_id, f'{name}에 해당하는 종목을 찾을 수 없습니다.')
        print('message received')
        print(msg)

def get_price(code):
        url = 'https://finance.naver.com/item/main.naver?code=' + code
        result = requests.get(url, headers={'User-agent' : 'Mozilla/5.0'})
        bs_obj = BeautifulSoup(result.content, 'html.parser')
        no_today = bs_obj.find('p', {'class' : 'no_today'})
#       blind_now = no_today.find('span', {'class' : 'blind'})
        if not no_today:
            return '주가 정보 없음'
        blind_now = no_today.find('span', {'class' : 'blind'})

        return blind_now.text if blind_now else '데이터 없음'

MessageLoop(bot, handle).run_as_thread()
# bot.message_loop(handle).run_as_thread()
print('프로그램 실행')
while True:
    time.sleep(10)
