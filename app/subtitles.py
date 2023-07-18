from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from googletrans import Translator
from telegraph import Telegraph

import requests
import json

video_url="https://www.youtube.com/watch?v=BXAeMICmUSQ&list=PLMHZ9bb1pnLv_MGPeezESZnQvGFRLOVHR&index=2"

def  tx(text1, dest, src) -> list:
	try:
		translator = Translator(service_urls=['translate.google.by','translate.google.ru'])
		translation =translator.translate(text=text1, dest=dest, src=src)
		#print(10, translation)
		return translation.text
	except Exception as ex:
		print(ex)
		return "Error"

def send_to_telegraph(post: str, short_name: str) -> str:
	telegraph = Telegraph()
	telegraph.create_account(short_name=short_name)

	response = telegraph.create_page(
	    'Субтитры к видосам на Youtube',
	    html_content=f'<p>{post}</p>'
	)
	print(response['url'])
	return response['url']

def youtube_transcript(video_url: str, username: str) -> list:

	video_id=video_url.split('=')[1].split('&')[0] 
	# assigning srt variable with the list
	# of dictionaries obtained by the get_transcript() function
	srt_ru = YouTubeTranscriptApi.get_transcript(video_id)#, languages=['ru', 'en']) #AsOssGeuFUw&t")
	# transcript_list = YouTubeTranscriptApi.list_transcripts("BXAeMICmUSQ&t")
	# srt_ru = transcript_list.find_manually_created_transcript(['ru', 'en'])

	formatter = TextFormatter()

	# .format_transcript(transcript) turns the transcript into a JSON string.
	txt_formatted = formatter.format_transcript(srt_ru)

	cont1=txt_formatted.replace("\n", " ")
	cont2=cont1.split(".")
	cont2=[i+". " for i in cont2]
	cont3=""
	trsl=""
	for i in range(len(cont2)):
		cont3+=cont2[i]
		if len(cont3) > 4600:
			trsl+=tx(cont3, dest="ru", src="en")
			cont3=""
	list_out=[]
	trsl2=trsl.replace(".", ".\n")
	list_out.append(trsl2)
	# with open('subtitles6.txt', 'w', encoding='utf-8') as _file6:
	# 	_file6.write(trsl2)
	link_telegraph=send_to_telegraph(trsl2, username)
	list_out.append(link_telegraph)

	return list_out

# youtube_transcript(video_url)

# url1 = 'https://api.telegram.org/bot1699887557:AAGvYsHg0IjLplNPmWiBRwbWfQrXVIRzZmU/sendMessage?chat_id=422838854&text='

# while True:
# 	on_waiting= input('[+] Отправить в телеграмм?(Enter: "y"): ')
# 	if on_waiting == 'y':
# 		try:
# 			requests.get(url1 , 'hi!!!!+uuu')
# 		except Exception as e:
# 			raise e
# 	if input('[+] Continue?(Enter: "y"): ') != 'y':
# 		break
