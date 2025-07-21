import requests
from bs4 import BeautifulSoup
import telepot
import time

my_token = '8122523141:AAE_XLPGXdpa_kcu0TUWnC62O5ZxIyMOP_E'
telegram_id = '5996719385'
bot = telepot.Bot(my_token)

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print('chat_id', chat_id)
	bot.sendMessage(chat_id, 'id: '+ str(chat_id))

def get_price(code):
	url = 'https://finance.naver.com/item/main.naver?code=' + code
	result = requests.get(url, headers={'User-agent' : 'Mozilla/5.0'})
	bs_obj = BeautifulSoup(result.content, 'html.parser')
	no_today = bs_obj.find('p', {'class' : 'no_today'})
	blind_now = no_today.find('span', {'class' : 'blind'})
	return blind_now.text

try:
	while True:
		msg = '삼성전자 현재가 : ' + get_price('005930')
		print(msg)
		bot.sendMessage(chat_id = telegram_id, text = msg)
		time.sleep(60000*10)

except KeyboardInterrupt:
	pass
