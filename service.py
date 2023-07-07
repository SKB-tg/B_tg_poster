from telegraph import Telegraph

import pprint ##-----dict в строку
from typing import Dict, List, Union, Optional
import time
import json
import requests
from telethon.sync import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputMessagesFilterPhotos
from telethon.utils import pack_bot_file_id, get_input_photo, resolve_bot_file_id

import configparser
import os, sys

from app.settings import settings


#bot = telebot.TeleBot( settings.TELEBOT_BOT_TOKEN)#'6163364880:AAGSbyRC5avfSuSzCn3whB5vcvwL2QS5mlc')
api_id = settings.API_ID #cpass['cred']['id']
api_hash = settings.API_HASH #cpass['cred']['hash']
phone = settings.PHONE #cpass['cred']['phone']

f_db="json\\Bot_messages_end_button2.json"
#**********************
def run_client() -> TelegramClient:
	try:
		client = TelegramClient(phone, api_id, api_hash)
	except KeyError:
		os.system('clear')
		print("\033[91m[!] run \033[92mpython3 setup.py \033[91mfirst !!\n")
		sys.exit(1)

	client.connect()
	if not client.is_user_authorized():
		client.send_code_request(phone)
		os.system('clear')
		client.sign_in(phone, input(gr+'[+] Enter the verification code: '+yo))
	client.start()
	return client
##**************************
#``` ищет слова, начинающиеся со знака "@" в заданном тексте: ```
import re 
def find_words(text: str, symbol):# -> list:
	#text=str(text).replace("|", ' ') 
	text=text.replace("\n", ' ')
	print(36, text, symbol)
	matches = re.findall(fr'{symbol}\w+\s|\?', text)
	#matches = pattern.findall(text) if pattern.findall(text) else [""]  
	print(40, )
	matches = matches if matches else [""]  
	return matches
##*************************************
def file_info(_file_id):
	#client1=run_client()
	data_file=resolve_bot_file_id(_file_id)

	return data_file
##************************************
# Функция для подписки бота на указанные каналы и чаты
def get_history(client1, chat, reply_to, limit):#забираем последние n собщений пдключаясь через "клиента"

	mess=[]
	for message in client1.iter_messages(chat, limit=limit):
		#print(37, message.message)
		# a=message.text.find('\n')
		# mess.text=message.text[a:]
		mess.append(message)
	return mess #list
#******************************************
def scan_all_channals(client1, chel: str = None, limit=20) -> List:
	List_channel=[]
	print("список любимых каналов")
	for dialog in client1.iter_dialogs( limit=limit):
		#mess.append(message)
		#if dialog.id == -1001663436185 or dialog.id == -1001666122554:
			#print(70, dialog.name, dialog.entity.megagroup, dialog.entity.participants_count, dialog.message.peer_id.channel_id)
		try:

			if dialog.entity.participants_count > 4:
				List_channel.append([dialog.id, dialog.title])
				print('{:>14}: {}'.format(dialog.id, dialog.title))
			# else:
			# 	List_channel.append([dialog])
		except Exception as e:
			print('{:>14}:'.format(dialog.title))

		#List_channel.append({ "Name": '{:>14}: {}'.format(dialog.id, dialog.title), "megagroup": dialog.entity.megagroup, "count": dialog.entity.participants_count, "channel_id": dialog.message.peer_id.channel_id})
		# if dialog.entity.participants_count > 5:
		# 	print('{:>14}: {}'.format(dialog.id, dialog.title))
	client1.disconnect()
	return List_channel

#**********************************************
def enable_waiting_new_mess(client, chats):

	# client.connect()
	# if not client.is_user_authorized():
	# 	client.send_code_request(phone)
	# 	os.system('clear')
	# 	client.sign_in(phone, input(gr+'[+] Enter the verification code: '+yo))

	@client.on(events.NewMessage(chats=chats))
	async def normal_handler(event):
	#    print(event.message)
		curent_mess=[]
		# curent_mess[event.message.to_dict()['id']] = event.message.to_dict()['message']
		curent_mess.append(event.message)
		print(71, curent_mess)
		send_messages(curent_mess)
	client.start()
	# if input('[+] Continue waiting message?(Enter: "y") или\n составить список готовых к обработке каналов (Enter: "h"): ') != 'y':
	# 	scan_all_channals(client)
	# else:
	# 	client(JoinChannelRequest(chats))#Присоединение к группе или чату
	# 	scan_all_channals(client)

	print('[+] Для выхода из режима ожидания - ``Ctrl+C``...')
#Организуем постоянную работу "клиента"
	client.run_until_disconnected()


import ast
# Функция для сканирования последних N сообщений в чатах и каналах
def scan_messages( channel: str, limit: int, subscribeding: bool=False):
	client1=run_client()
	if (subscribeding):
 		client1(JoinChannelRequest(chats))#Присоединение к группе или чату
 		time.sleep(10)
	messages_list = []
	try:
		# Получаем последние 5 сообщений из канала/чата
		for message in client1.iter_messages(chat, limit=limit):
			#print(37, message.message)
			messages_list.append(message)
	except Exception as e:
		print(e)
	client1.disconnect()
	return messages_list

# Функция для анализа сообщений из словаря и их модификации
def analyse_messages(messages_list):
	modified_messages = []
	nom=1
	for n in messages_list:
		#g=client.get_messages(n.chat_id, ids=3418)

		symbol="@"

		n.message=n.message.replace('`', "").replace(find_words(n.message, symbol)[0], "")
		print(135, find_words(n.text, symbol), n.id, n.peer_id)
		modified_messages.append(n)

		print( f"Фильтруем:{nom} ", n.message)
		nom+=1
	return modified_messages #modified_messages_dictionary

# Функция для отправки модифицированных сообщений в канал
def send_messages(bot, channel, modified_messages: list):
	#bot.get_chat_member(channel, bot.get_me().id)
	#bot.send_message('@crypto_bag_develop', 'Привет! Я присоединился к вам!')
	i=0
	#print(122, modified_messages_dictionary)
	#for message_id, message_text in modified_messages_dictionary.items():
	for n in modified_messages:
		n.peer_id=bot.get_me().id
		n.id=0
		try:
			print(n.post)
			client.send_message(channel, n)

		except Exception as e:
			print(e)
			return False
		# else:
		# 	n.message + "Hi!!!"
		# 	id_photo=n.photo
		# 	id_photo_str=pack_bot_file_id(id_photo)
		# 	print(id_photo_str)
		# 	#client.send_p(channels_list1[1], n.message, parse_mode=None)
		# 	#bot.send_photo(channels_list1[1], str(id_photo_str))
		# 	bot.send_message(channel, n.message)
		# 	#bot.send_document()
		i+=1
		return True

def send_message_uan(bot, channel, m):
	m.peer_id=bot.get_me().id
	m.id=0
	client.send_message(channel, m)
	#bot.send_message(channels_list1[1], m)
def dicting(dict_str) -> dict:
    data1 = dict_str
    data2 = data1.strip().replace('{', '').replace('}', "")
    b={i.split(':')[0]:i.split(':')[1] for i in data2.replace('"', "").replace("'", "").replace(' ', "").split(',')}
    print(type(b), b)
    return b
#************************************telegra.ph**********************
def upload_image_in_telegraph(f) -> str:
	telegraph = Telegraph()
	response=telegraph.create_account(short_name='Channel-image') #requests.get(f'https://api.telegra.ph/createAccount?short_name=Channel-image&author_name=Anonymous')
	#token=response['result']['access_token']
	#create_page=requests.get(f'https://api.telegra.ph/createPage?access_token={token}&title=Sample+Page&author_name=Anonymous&content=[{"tag":"p","children":["Приветствую всех, готов к работе!"]}]&return_content=true')
	response2=telegraph. upload_file(f)
	link=response2[0]["src"]
	return link
#***********************************************************
data_all_bot={}
def inicialisiren_bot(chat_id1, is_managet: bool, bot: Optional=None) -> List:
	#data_bot=bot.get_me()
	res_dict={}
	channels_bot=[]
	r_fB=read_fileBot(chat_id1)
	print(192, r_fB) 
	if r_fB != None:
		#a=json.load(r_fB)
		for n in range(len(r_fB)):
			res_dict=dicting(r_fB[n])
			res_dict["is_managet"] = bool(res_dict["is_managet"].strip())
			res_dict["id_channel"] = int(res_dict["id_channel"])
			print(196, type(res_dict), res_dict)
			k=int(res_dict['chat_id'])
			if (k == int(chat_id1)) & (is_managet == res_dict["is_managet"]):
				channels_bot.append(res_dict) #["channel"]       #каналы или группы - список словарей в словарь
			print(209, channels_bot, k, (is_managet == res_dict["is_managet"]))
	else:
		new_data_channel={"chat_id": chat_id1, "username_channel": "", "id_channel": 0, "is_managet": True}
		write_to_fileBot(new_data_channel, chat_id1)
		channels_bot.append(new_data_channel)
		#return new_data_channel
		#data_all_bot["channel"]= chennel_bot_admin
	post_ovner=None    # отложенный посты
	data_all_bot["post_ovner"]=post_ovner
		#import pprint ##-----dict в строку
		# # Convert dictionary into string using pprint.pformat()
		# result = pprint.pformat(d)
	return channels_bot

 #data = await request.json()
def read_fileBot(chat_id,*arg) -> List:
	try:
		with open(f'app/{chat_id}.txt', 'r', encoding="utf-8") as fp:
			cont = fp.readlines() 
	except Exception as e:
		print(e)
		return None
	cont1=[]
	for x in range(len(cont)):
		y=cont[x] #+ ";" + " .."#.replace('\n', "").strip()
		cont1.append(y)
		#cont1[0]=cont1[0].replace("\n", "")
		#cont1.pop()
	print(224, cont1,)
	return cont1[1:]
def has_channel(chat_id, username_channel: Optional[str]=None, id_channel: Optional[int]=None) -> Union[dict, None]:
	has_channel = read_fileBot(chat_id, username_channel)
	if has_channel:
		for l in has_channel:
			ldict=dicting(l)
			if (ldict["username_channel"] == username_channel) | (ldict["id_channel"] == id_channel):
				return ldict
	return None

def save_data_channel(data ):
	has_channels=has_channel(data["chat_id"], data["username_channel"])
	if has_channels is not None:
		return has_channels
	name_file=str(data["chat_id"])
	print(229, name_file)
	result = write_to_fileBot(data, name_file)
	return result


def write_to_fileBot(data: dict, name_file: str):
	try:
		#text = '"'+str(pprint.pformat(data))+'"'
		text = str(data) +"\n"
		# with open('data_bot.txt', 'r', encoding="utf-8") as fp:# считываем последнюю стр и опредляем наличие "\n"
		# 	cont = fp.readlines() 
		# cont_n=[ cont[i] for i in range(len(cont)) if i == len(cont)-1]
		# print(235, cont_n)
		# if cont_n[0].find('\n') == -1:
		# 	text="\n" + text
		  #print(67, text, cont_n, cont_n[0].find('\n'))

		with open(f'app/{name_file}.txt', 'a+', encoding="utf-8") as f:
		# Считать содержимое файла и отправить его в ответе 
			f.write(text)
		  # f.write("\n") 
		return True#data={'m
	except Exception as e:
		# try:
		# 	with open(f'app/database/db/{name_file}.txt', 'w', encoding="utf-8") as f:
		# # Считать содержимое файла и отправить его в ответе 
		# 		f.write(text)
		#   # f.write("\n") 
		# 	return True#data={'m
		# except Exception as e:
		print(e)
		return False

def is_channel_managet(chat_id, username_channel):
	r_fB=read_fileBot(chat_id) 
	if r_fB is not None:
		for n in r_fB:
			n
			m=dicting(n)["username_channel"]
			if m == username_channel:
				print(264, m)
				return True
		return False

def get_list_button(key: str) -> list:
    """Возвращает сообщение для отправки из db(json)"""
    list_b=get_message(key)[1].split('=')
    list_button=[l.split("'")[1] for l in list_b if l.count("'") > 0]
    return list_button

def get_message(key: str) -> tuple:
    """Возвращает сообщение для отправки из db(json)"""
    mess_dict=_read_json(f_db)
    return mess_dict[key]

def _read_json(f_name) -> dict:
    data_dict={}
    with open(f_name, "r", encoding='UTF-8') as f:
        data = json.load(f)
    data_dict = { d[0]:d[1] for d in data.items()}
    return data_dict

# Функция для запуска бота
# def run_bot():
# 	#is_subscribed()
# 	while True:
# 		on_waiting= input('[+] on_scan all channel(Enter: "y"): ')
# 		if on_waiting == 'y':
# 			scan_all_channals(client)
# 		on_waiting= input('[+] Enable waiting message(Enter: "y"): ')
# 		if on_waiting == 'y':
# 			enable_waiting_new_mess(client, chats=channels_list)
# 		on_scan_messages = input('[+] on_scan_messages(Enter: "y"): ')
# 		if on_scan_messages == 'y':
# 			messages_dictionary = scan_messages(client)
# 			time.sleep(3)
# 			#print(messages_dictionary)
# 			modified_messages_dictionary = analyse_messages(messages_dictionary)

# 		on_send_messages = int(input('[+] послать пост № '))
# 		if on_send_messages > 0:
# 			send_message_uan(modified_messages_dictionary[on_send_messages-1])

# 		if input('[+] Continue?(Enter: "y"): ') != 'y':
# 			break




		#time.sleep(260)

# run_bot()


# python import telebot bot = telebot.TeleBot('YOUR_TOKEN') # создаем словарь сообщений 
# messages = {} # получаем список каналов 
# channels_list = bot.get_chat_administrators('channel_name') # перебираем все каналы и сканируем последние 5 сообщений 

# for channel in channels_list:
# 	messages[channel] = bot.get_chat_history(channel, limit=5) # анализируем сообщения и фильтруем по ключевым словам 
# filtered_messages = {} 
# for channel, messages in messages.items():
#  filtered_messages[channel] = [message for message in messages if 'keyword' in message.text] # отправляем модифицированные сообщения в указанный канал 

# for channel in filtered_messages: 
# 	for message in filtered_messages[channel]:
# 	bot.send_message(channel, message.text, reply_to_message_id=message.message_id, from_user="channel_owner") 


