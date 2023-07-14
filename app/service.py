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
from app.models import add_tg_channel, get_channel, get_channels, Channel


#bot = telebot.TeleBot( settings.TELEBOT_BOT_TOKEN)#'6163364880:AAGSbyRC5avfSuSzCn3whB5vcvwL2QS5mlc')
api_id = settings.API_ID #cpass['cred']['id']
api_hash = settings.API_HASH #cpass['cred']['hash']
phone = settings.PHONE #cpass['cred']['phone']

f_db="json\\Bot_messages_end_button2.json"
#**********************


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
##**************************
#``` ищет слова, начинающиеся со знака "@" в заданном тексте: ```
import re 
def find_words(text: str, symbol):# -> list:
	#text=str(text).replace("|", ' ') 
	text=text.replace("\n", ' ')
	print(36, text, symbol)
	matches = re.findall(fr'{symbol}\w+\s', text)
	#matches = pattern.findall(text) if pattern.findall(text) else [""]  
	print(40, )
	matches = matches if matches else [""]  
	return matches

#***********************************************************

def inicialisiren_bot(chat_id1: dict, is_managet: Optional[bool], bot: Optional=None) -> List:
	channels=get_channels(chat_id1)
	if channels != None:
		channels_bot_admin=[i for i in channels if i.is_managet == is_managet]
		print(68, channels_bot_admin)
		# if channel.is_managet == is_managet:
		# 	channels_bot_admin.append(channel)
		# 	return channels_bot_admin
		# channels_bot_no_admin.append(channel)
		return channels_bot_admin
	else:
		return [Channel()]

def save_data_channel(data ):
	is_channel=get_channel(data["chat_id"], data["id_channel"])
	if is_channel != None:
		return is_channels

	print(229, is_channel)
	result = add_tg_channel(data)
	return result

def is_channel_managet(chat_id, id_channel):
	is_channel=get_channel(chat_id, id_channel)
	if is_channel != None:
		return True
	return False
 #***************************************************
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


def get_cmozi() -> List:
	try:
		with open(f'app/Cmozi.txt', 'r', encoding="utf-8") as fp:
			cont = fp.readlines() 
	except Exception as e:
		print(e)
		return None
	cont1=[]
	print(282, cont)
	for x in range(len(cont)):
		y=cont[x] #+ ";" + " .."#.replace('\n', "").strip()
		cont1.append(y)
	return cont1
def save_cmozi(data: str, ):
	try:
		#text = '"'+str(pprint.pformat(data))+'"'
		text = str(data) +"\n"
		with open(f'app/Cmozi.txt', 'w+', encoding="utf-8") as f:
		# Считать содержимое файла и отправить его в ответе 
			f.write(text)
		  # f.write("\n") 
		return True#data={'m
	except Exception as e:
		print(e)
		return False

def write_to_fileBot(data: dict, name_file: str):
	try:
		text = str(data) +"\n"
		with open(f'app/{name_file}.txt', 'a+', encoding="utf-8") as f:
		# Считать содержимое файла и отправить его в ответе 
			f.write(text)
		  # f.write("\n") 
		return True#data={'m
	except Exception as e:

		print(e)
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
