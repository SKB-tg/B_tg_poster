from fastapi import FastAPI
import uvicorn
from typing import Callable, Dict, Any, Awaitable, Union, List, Optional, BinaryIO
import requests
from aiogram import Bot, F, Router, Dispatcher
from aiogram.filters import Command, BaseFilter
import asyncio
import io
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    MenuButtonCommands,
    Message,
    WebAppInfo,
    BotCommand,
    MessageEntity,
    Update,
    


)
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.text import Text
from aiogram.methods.copy_message import CopyMessage
from aiogram.methods.delete_message import DeleteMessage
from aiogram.methods.get_file import GetFile


from aiogram.types.bot_command_scope_all_chat_administrators import BotCommandScopeAllChatAdministrators
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, KeyboardBuilder
from app.settings import settings
from service import (scan_all_channals,
    scan_messages, send_messages, send_message_uan, run_client, save_data_channel, upload_image_in_telegraph,
    inicialisiren_bot, is_channel_managet, read_fileBot, has_channel, find_words, file_info
)
from aiogram import flags, html
from aiogram.dispatcher.flags import get_flag


bot_post = Bot(settings.TELEBOT_BOT_TOKEN)
#form_router = Router()
#dp = Dispatcher()
#dp.include_router(form_router)
#print(ACCESS_ID)

_dispatcher=Dispatcher()
mp_router = Router()
m_router = Router()

_dispatcher.include_router( mp_router)
mp_router.include_router(m_router)

base_url="https://tbf-b1-editor.onrender.com/shop-online/"
#************************************
Ch_id=0
List_data_channel_admin=[]
List_data_channel_source=[]
Curent_Channal={}
Create_message_id=[]
Mode_select_channel_admin=False

def cur_channal_admin(value: Optional[int]=None) -> Union[dict, None]:
    if value == None:
        return List_data_channel_admin[0]
    for item in List_data_channel_admin:
        if int(item["id_channel"]) == int(value):
            curent_channal=item
            return curent_channal
    #return None

async def restart(messs):
    await command_start(messs)


#************************************************

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, input_text_message_content
from aiogram.methods.get_chat_administrators import GetChatAdministrators
from aiogram.types.input_text_message_content import InputTextMessageContent



class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data_time = get_flag(data, "data_time")
        global Ch_id
        Ch_id=data["event_update"].message.chat.id
        global List_data_channel_admin
        List_data_channel_admin= inicialisiren_bot(Ch_id, True)
        #if data["event_update"].message.photo != None:
            #print(92, Ch_id)
        global Curent_Channal
        #Curent_Channal= List_data_channel_admin[0]

        # chat_id_as_post1: Union[List, None] = data["event_update"].message.forward_from_chat
        # if chat_id_as_post1 is not None:
        #     chat_id_as_post="@" + chat_id_as_post1.title #for item in chat_id_as_post:
        #     try:
        #         result = await bot_post.get_chat_administrators(chat_id_as_post)
        #         print(75, result[1].user.id, 7777, event.chat.id )
        #         if result[1].user.id == event.chat.id:

        #         #data["event_update"].message.forward_from_chat.type="channell"
        #     except Exception as e:
        #print(84, data)
        # # Если такого флага на хэндлере нет
        # # if not :
        #     return await handler(event, data)
        # #f_channal()
        #     print(61, data_time)# data["channal_"]
        # # event.forward_from_chat.type="channel_managet"
        return await handler(event, data)

m_router.message.middleware(SomeMiddleware())

#****************************************************
class SomeRouterPostMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        print("Получил ---- POST")
        
        return await handler(event, data)

mp_router.channel_post.outer_middleware(SomeRouterPostMiddleware())
#****************************************************

class HasAdminStatusFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Если entities вообще нет, вернётся None,
        # в этом случае считаем, что это пустой список
        chat = message.chat or []
        chat_as_post1=message.forward_from_chat or []
        if (chat_as_post1 != None) & (Mode_select_channel_admin == True):
            chat_id_as_post="@" + chat_as_post1.username if chat_as_post1.username != "" else "@" + chat_as_post1.title #for item in chat_id_as_post:
            try:
                result = await bot_post.get_chat_administrators(chat_id_as_post)
                for item in result:
                    if item.user.id == chat.id: ##владелец бота явл. админом канала(группы мегагруппы)
                        #print(75, item.user, chat.id, 7777 )

                        return True

            except Exception as e:
                print(70, e, chat_id_as_post)

                return False
            return False

# class HasInputTextFilter(BaseFilter):
#     async def __call__(self, message: Message) -> bool:

#****************************************************
def get_list_button(key: str) -> list:
    """Возвращает сообщение для отправки из db(json)"""
    list_b=get_message(key)[1].split('=')
    list_button=[l.split("'")[1] for l in list_b if l.count("'") > 0]
    return list_button

#****************************************************

@m_router.message(Command(commands=["start"]))
async def command_start(message: Message, base_url: str = base_url):
    await bot_post.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonCommands(type="commands"),# "Меню\n/newpost     Создать новы пост\n/newdraft     Создать черновой пост\n/newpost     Создать новы пост\n/newpost     Создать новы пост\n/newpost     Создать  новы пост\nМеню\n/newpost     Создать новы пост\n/newdraft     Создать черновой пост\n/newpost     Создать новы пост\n/newpost     Создать новы пост\n/newpost     Создать  новы пост\n"
    )
    #print(message)
    _command1: BotCommand = None
    _commands1: list = []
    _commands1 = [{"command": "repost_plus", "description": "команда кланирующая пост"},
    {"command": "addchannel", "description": "подключает новый канал"},
    {"command": "newpost", "description": " создать новый пост"},
    {"command": "editpost", "description": "редактировать пост"},
    {"command": "draftpost", "description": "создать черновик поста"},
    {"command": "notes", "description": "заметки"},
    {"command": "settings", "description": "настройки бота"},
    {"command": "statistic", "description": "статистика"},
    {"command": "help", "description": "помощь"},
    {"command": "start", "description": "рестарт"}]
    await bot_post.set_my_commands(_commands1)
    global Ch_id
    Ch_id=message.chat.id
    global List_data_channel_admin
    if List_data_channel_admin == []:
        List_data_channel_admin=inicialisiren_bot(message.chat.id, True)
    global Curent_Channal
    print(169, Curent_Channal, List_data_channel_admin)
    Curent_Channal= {}
    #print(89, List_data_channel_admin)
    await message.answer("""Это ваш личный Notepost-бот для подготовки контента, постинга и автоприёма заявок:\n\n

— ChatGPT поможет в генерации текста 🔥\n
— шаблоны автоматически добавят кнопки, реакции и водяной знак\n
— сценарии запланируют посты без единого клика\n
— функция автоповтора обеспечит циклическую публикацию объявлений\n
— бот автоматически примет заявки, отправит приветствия и сохранит пользователей в базу для дальнейшей рассылки\n
— NEW: появилась кнопка "репост+" 🔥, позволяющая клонировать посты с любимых каналов\n
Для начала работы подключите канал или группу:\n

/addchannel – новый канал\n
/addgroup – новая группа\n
/repost_plus - команда кланирующая пост\n
Если что-то непонятно:\n

/help – полезная информация и техподдержка""",
        reply_markup=get_reply_keyboard()

     )
    await message.answer("` 👨‍🎓   Успешного развития вашему каналу!!!   👨‍🎓 `",

        reply_markup= InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Далее', callback_data=f'Continue_start')],
        ])
        
        )

@m_router.callback_query(Text(startswith="Continue_"))
async def send_value2(callback: CallbackQuery):
    sufix = callback.data.split("_")[1]
    global List_data_channel_admin
    global Mode_select_channel_admin
    if List_data_channel_admin == []:
        List_data_channel_admin= inicialisiren_bot(callback.message.chat.id, True)
    print(235, List_data_channel_admin)

    curent_channel= [] #[curent_channel1: str, curent_channel2: str, curent_channel3: str]
    for n in range(len(List_data_channel_admin)):
        curent_channel.append("\n@" + str(List_data_channel_admin[n]["username_channel"]))
    b=curent_channel[1] if len(curent_channel) > 1 else ''
    c=curent_channel[2] if len(curent_channel) > 2 else ''
    #if List_data_channel_admin != []:
    # curent_channel1=List_data_channel_admin[n]["username_channel"] or ""
    # curent_channel2=List_data_channel_admin[len(List_data_channel_admin)-2]["username_channel"] if len(List_data_channel_admin) > 1 else ""
    # curent_channel3=List_data_channel_admin[len(List_data_channel_admin)-1]["username_channel"] if len(List_data_channel_admin) > 2 else ""

    if sufix == "start":
        #print(206, (curent_channel["username_channel"] == ""))
        if curent_channel[0] == "\n@":
            await callback.message.answer(
                """ __--__\n\nНачните с добавления канала для администрирования\n\n
                Чтобы добавить канал, вы должны выполнить два следующих шага:\n\n
                1. Добавьте @cripto_fack_new_bot в администраторы вашего канала.\n
                2. Перешлите мне любое сообщение из вашего канала (вы также можете отправить @username или Group ID) """,
                #show_alert=True
            )
            Mode_select_channel_admin=True
            return
        await callback.message.answer(
            f"""У вас подключены следующие каналы:{curent_channel[0]}{b}{c}\n они в списке администрируемых каналов. 
                """,
            reply_markup=get_inline_keyboard2() ,

                )

    await callback.answer()
#********************************************************************

def get_reply_keyboard():
    reply_markup_buttons=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Контент-план"), KeyboardButton(text="Статистика")],
        [KeyboardButton(text="Заметки"), KeyboardButton(text="Настройки")]],
        one_time_keyboard=False, resize_keyboard=True,
    )
    return reply_markup_buttons

def get_inline_keyboard2(curent_channel_id: Optional[str] = ""):
    buttons =[
        [InlineKeyboardButton(text='Создать пост', callback_data=f'post-create_create_{curent_channel_id}')],#_{message_channel_id}')],
        [InlineKeyboardButton(text='Клонировать', callback_data=f'repost_clone_{curent_channel_id}')], 
        [InlineKeyboardButton(text='Отложенные', callback_data=b'scheduled'), InlineKeyboardButton(text='Редактировать', callback_data=b'edit')], 
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, one_time_keyboard=False)
    return keyboard


def get_inline_keyboard(curent_channel_id: Optional[str] = ""):
    buttons =[
            [InlineKeyboardButton(text="Прикрепить медиафайл", callback_data=f"repost_media_{curent_channel_id}")],
            [InlineKeyboardButton(text="Добавить комментарии", callback_data="repost_plus"),
            InlineKeyboardButton(text="Предпросмотр", callback_data="PPP")],
            [InlineKeyboardButton(text="Добавить реакции", callback_data="Edit")],
            [InlineKeyboardButton(text="Добавить URL-кнопки", callback_data="Edit")],
            [InlineKeyboardButton(text="Удалить сообщение", callback_data=f"repost_delete_{curent_channel_id}"),
            InlineKeyboardButton(text="Далее", callback_data=f"repost_continue_{curent_channel_id}")]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def get_inline_keyboard0(curent_channel_id: Optional[str] = ""):
    buttons =[
            [InlineKeyboardButton(text="Удалить сообщение", callback_data=f"repost_delete_{curent_channel_id}"),
            InlineKeyboardButton(text="🔥 Отправить", callback_data=f"repost_Send_{curent_channel_id}")]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

#********************************************************************

@m_router.message(((F.text == "addchannel_") | (F.Command == "addchannel"))) #(Command(commands=["addchannel"]))
async def command_addchannel(message: Message):
    #list_channel=read_fileBot()
    global Mode_select_channel_admin
    Mode_select_channel_admin=True
    await message.answer(
        """Добавление канала\n\n

Чтобы добавить канал, вы должны выполнить два следующих шага:\n\n

1. Добавьте @cripto_fack_new_bot в администраторы вашего канала.\n
2. Перешлите мне любое сообщение из вашего канала (вы также можете отправить @username или Group ID)""",  ##(https://telegra.ph/How-to-add-a-chat-Controller-FAQ-10-12)
    )

#@flags.data_time(event1=True)
@m_router.message(F.forward_from_chat.type == "channel", HasAdminStatusFilter())#, F.forward_from_chat.as_("channel_managet"))  # Echo to all messages except messages via bot
async def forward_mess(message: Message):#, channel_managet):
    #print(channel_managet)
    global List_data_channel_admin #= inicialisiren_bot(message.chat.id, True)
    #print(299, message)
    if is_channel_managet(message.chat.id, message.forward_from_chat.username):
        await message.answer(
       f"""Я уже подключен к этому каналу.\n\n
            Теперь мы готовы приступить к работе\n\nдля создания поста.\n
    отправьте боту то, что хотите опубликовать. Это может быть всё, что угодно – текст, фото, видео, даже
     стикеры.\n\nA также можете воспользоваться волшебной кнопкой /repost_plus
""",
        reply_markup=get_inline_keyboard2() ,
               # reply_markup=InlineKeyboardMarkup(
        #     inline_keyboard=[
        #         [InlineKeyboardButton(text="Репост+", callback_data="repost_plus")]
        #     ]
        # ),
        )
    else:
        #print(message.forward_from_chat.username)
        data_channel_admin_new={}
        data_channel_admin_new["username_channel"]=message.forward_from_chat.username
        data_channel_admin_new["id_channel"]=message.forward_from_chat.id
        data_channel_admin_new["chat_id"] =message.chat.id
        data_channel_admin_new["is_managet"] =True
        # global Curent_Channal
        # if List_data_channel_admin[0]["chat_id"] == 0:
        #     List_data_channel_admin[0]=data_channel_admin_new
        # #Curent_Channal=data_channel_admin_new
        List_data_channel_admin.append(data_channel_admin_new)
        res = save_data_channel(data_channel_admin_new)
        #res = save_data_channel(data_channel) if save_data_channel(data_channel) else print("net")
        await message.answer(
            f"""Вы добавили канал «{message.forward_from_chat.title}» @{message.forward_from_chat.username} в список администрируемых каналов. 
            и\nмы готовы приступить к работе\n\nдля создания поста.\n
    отправьте боту то, что хотите опубликовать. Это может быть всё, что угодно – текст, фото, видео, даже
     стикеры.\n\nA также можете воспользоваться волшебной кнопкой /repost_plus""",

            reply_markup=get_inline_keyboard2(),

        )



@m_router.callback_query(Text(startswith="repost_"))
async def run_repost_plus(callback: CallbackQuery):
    sufix_full=callback.data.split("_")
    sufix = callback.data.split("_")[1]
    #Curent_channel=has_channel(Ch_id, id_channel=sufix_full[2] if sufix_full[2] != None else None)
    #cur_channal_admin(Curent_channel)
    global List_data_channel_admin
    if List_data_channel_admin == []:
        List_data_channel_admin= inicialisiren_bot(callback.message.chat.id, True)
    asu=dict(create_mess_id=callback.message.message_id)

    global Curent_Channal
    curent_channel_id=sufix_full[2] if sufix_full[2] != "" else ""
    if (Curent_Channal == {}) & (curent_channel_id != ""):
        Curent_Channal.update(cur_channal_admin(curent_channel_id))
        Curent_Channal.update(asu)
    #(319, Curent_Channal, sufix_full[2], Ch_id)
    username_channel=[]
    id_channel=[]
    button=[]
    if (sufix == "clone") & (curent_channel_id == ""):
        #List_data_channel_admin=inicialisiren_bot(message.chat.id, True)
        for n in range(len(List_data_channel_admin)):
            username_channel.append(List_data_channel_admin[n]["username_channel"])
            id_channel.append(List_data_channel_admin[n]["id_channel"])
            button.append(InlineKeyboardButton(text=username_channel[n], callback_data=f"repost_create_{id_channel[n]}"))

        #(388, List_data_channel_admin, id_channel, callback.data)
        await callback.message.answer(
            "выбирите канал с которым будете работать",
           reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[button]
            ),
                )
        return
    elif (sufix == "edit") & (curent_channel_id != ""):
        await callback.message.answer(
                f"""
                Наберите текст и отправте"""
            )
        # await callback.message.edit_text(" ",
        #     inline_message_id = callback.message.message_id-2)


    elif (sufix == "clone") & (curent_channel_id != ""):
        #global Curent_Channal
        # Curent_Channal=cur_channal_admin(curent_channel_id)
        # print(384, curent_channel_id, Curent_Channal)
        await callback.message.answer(
                f"""
                Для успешного маневра,\n перейдя в канал выберите любое сообщение,\n
  нажмите на значок переслать, выберите моё имя -\n\n "Cripto-fack" (@cripto_fack_new_bot) и отправте пост."""
            )
    elif (sufix == "create") & (curent_channel_id != ""):
        # Curent_Channal=cur_channal_admin(curent_channel_id)
        await callback.message.answer(
                f"""
        мы готовы приступить к работе\n\nдля создания поста.\n
    отправьте боту то, что хотите опубликовать. Это может быть всё, что угодно – текст, фото, видео, даже
     стикеры.""",
        )
    elif (sufix == "delete") & (curent_channel_id != ""):
        await callback.message.answer(
                f"""
        вы хотите удалить текущий пост?\n
        """,
        reply_markup= InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подтвердите', callback_data=f'repost_okdelete_{curent_channel_id}')],
        ])
        )
    elif (sufix == "okdelete") & (sufix_full[2] != None):
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-3 )
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-2 )
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-1 )
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id )

        await callback.message.answer(
            f""" ` _ _ ~ Сообщения удалены. Можно продолжать. ~ _ _ `
                """,
            reply_markup=get_inline_keyboard2() ,

                )
    elif (sufix == "Send") & (curent_channel_id != None):
        #curent_chat_id = callback.data.split("_")[1]
        await callback.message.copy_to(curent_channel_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[]))
        await callback.message.answer(
            text="~ Сообщение успешно отправлено в канал! ~",
            #show_alert=True
            reply_markup= InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔙 Вернуться', callback_data=f'Continue_start_{curent_channel_id}')], 
            ])
        )
        Curent_Channal={}

    elif (sufix == "media") & (curent_channel_id != None):
        await callback.message.answer(
            text="Вышлите медиафайл",
            #show_alert=True
        )

    await callback.answer()
#**********************************************************************************************
@m_router.message(Command(commands=["repost_plus"]))  # Echo to all messages except messages via bot
async def run_repost_plus(message: Message):
    List_data_channel_source= inicialisiren_bot(message.chat.id, False)
    #(266, List_data_channel_source)
    username_channel=[]
    chat_id=[]
    List_data_channel_admin=inicialisiren_bot(message.chat.id, True)
    for n in List_data_channel_admin:
        username_channel.append(n["username_channel"])
        chat_id.append(n["chat_id"])
    #(username_channel, chat_id)
    await message.answer(
        "выбирите канал с которым будете работать",
       reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=str(username_channel[0]), callback_data=f"repost_{chat_id[0]}_{chat_id[0]}"),
                InlineKeyboardButton(text="username_channel", callback_data=f"repost_{chat_id[0]}")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="repost_back")]
            ]
        ),
            )

#**********************************************основной обработчик при клоне******************************



from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

@m_router.message(F.forward_from_chat.type == "channel")#, flags={"data_time": {"event": True}})  # Echo to all messages except messages via bot
async def forward_mess_clone(message: Message, base_url: str=base_url):
    List_data_channel_source= inicialisiren_bot(message.chat.id, False)
    #(474, message)
    for item in List_data_channel_source:
        try:
            if int(item["id_channel"]) != message.forward_from_chat.id:
                data_channel_source_new["username_channel"]=message.forward_from_chat.username
                data_channel_source_new["id_channel"]=message.forward_from_chat.id
                data_channel_source_new["chat_id"] =message.chat.id
                data_channel_source_new["is_managet"] =False
                List_data_channel_source.append(data_channel_source_new)
                res = save_data_channel(data_channel_source_new)
            #data_curent_channel=item
        except Exception as e:
            print(e)
    mess=message.text
    mess_channal=message.forward_from_chat
    mess_entity=message.entities
    #print(442, message, 119988 )
    forward_mess_id=message.message_id #message.forward_from_message_id-1
    await message.answer(
    f"""Я получил пост из этого канала @{mess_channal.username}.
    """)
    global Curent_Channal
    curent_channel=Curent_Channal
    if (message.photo == None) & (message.animation == None):
        id_channel='@' + curent_channel["username_channel"]
        id_channel_source=message.chat.id #'@' + data_curent_channel["username_channel"]
        sim=find_words(str(mess), "@")
        sim1 = sim[0] if sim != [""] else ""
        #print(sim1, message.photo,33333 , message.caption)
        mess = str(mess).replace(str(sim1), "").replace("|", '')

        await message.answer(text=mess, entities=mess_entity, reply_markup=get_inline_keyboard0(curent_channel["id_channel"]))
    elif message.photo != None :
        #await show_summary(message=message, data=[id_channel, id_channel_source, forward_mess_id])
        with suppress(TelegramBadRequest):
            await message.answer_photo(message.photo[-1].file_id, caption=message.caption, caption_entities=message.caption_entities, reply_markup=get_inline_keyboard0(curent_channel["id_channel"]))

    elif message.animation != None :
        with suppress(TelegramBadRequest):
            await message.answer_animation(message.animation.file_id, caption=message.caption, caption_entities=message.caption_entities, reply_markup=get_inline_keyboard0(curent_channel["id_channel"]))


#********************************************************************

async def show_summary(message: Message, data: List) -> None:
    try:
        #mess = " \n" + str(message.text).replace(find_words(message.text, "@")[0], "")
        message1= await message.send_copy(data[0])

        await message.answer(text="mess ok",
                #entities = message.entities,
        reply_markup=get_inline_keyboard()
        )
    except Exception as e:
        print(e)
    # async def my_middleware(handler, event, data):
    # typing = get_flag(data, "typing")  # Check that handler marked with `typing` flag
    # if not typing:
    #     return await handler(event, data)

    # async with ChatActionSender.typing(chat_id=event.chat.id):
    #     return await handler(event, data)


#*******************************************обработчик creat**************
def get_inline_keyboard_creat(curent_channel_id: Optional[str] = ""):
    buttons =[
            [InlineKeyboardButton(text="Прикрепить медиафайл", callback_data=f"post-create_media_{curent_channel_id}")],
            [InlineKeyboardButton(text="Добавить комментарии", callback_data="post-create_plus"),
            InlineKeyboardButton(text="Предпросмотр", callback_data="PPP")],
            [InlineKeyboardButton(text="Добавить реакции", callback_data="Edit")],
            [InlineKeyboardButton(text="Добавить URL-кнопки", callback_data="Edit")],
            [InlineKeyboardButton(text="Удалить сообщение", callback_data=f"post-create_delete_{curent_channel_id}"),
            InlineKeyboardButton(text="Далее", callback_data=f"post-create_continue_{curent_channel_id}")]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_inline_keyboard3(curent_channel_id: Optional[str] = ""):
    buttons =[
            [InlineKeyboardButton(text="Отменить", callback_data=f"post-create_delete_{curent_channel_id}")],
            [InlineKeyboardButton(text="Опубликовать", callback_data=f"post-create_Send_{curent_channel_id}"),
            InlineKeyboardButton(text="Отложить", callback_data="Edit")],
            [InlineKeyboardButton(text="🔙 Вернуться", callback_data=f"Continue_start_{curent_channel_id}")]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
#******************************************Calback******
@m_router.callback_query(Text(startswith="post-create_"))
async def run_create(callback: CallbackQuery):
    sufix_full=callback.data.split("_")
    sufix = callback.data.split("_")[1]

    global List_data_channel_admin
    if List_data_channel_admin == []:
        List_data_channel_admin= inicialisiren_bot(callback.message.chat.id, True)
    asu=dict(create_mess_id=callback.message.message_id)

    global Curent_Channal
    curent_channel_id=sufix_full[2] if sufix_full[2] != "" else ""
    if (Curent_Channal == {}) & (curent_channel_id != ""):
        #if Curent_Channal["id_channel"] != curent_channel_id:
        Curent_Channal.update(cur_channal_admin(curent_channel_id))
        Curent_Channal.update(asu)
    #print(646, Curent_Channal, sufix_full[2])
    username_channel=[]
    id_channel=[]
    button=[]
    if (sufix == "create") & (curent_channel_id == ""):
        #List_data_channel_admin=inicialisiren_bot(message.chat.id, True)
        for n in range(len(List_data_channel_admin)):
            username_channel.append(List_data_channel_admin[n]["username_channel"])
            id_channel.append(List_data_channel_admin[n]["id_channel"])
            button.append(InlineKeyboardButton(text=username_channel[n], callback_data=f"post-create_create_{id_channel[n]}"))

        #print(654, List_data_channel_admin, id_channel, callback.data)
        await callback.message.answer(
            "выбирите канал с которым будете работать",
           reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[button]
            ),
                )
        return
    elif (sufix == "media") & (curent_channel_id != None):
        #Curent_Channal=cur_channal_admin(curent_channel_id)
        await callback.message.answer(
            text=f"Вышлите медиафайл {callback.message.message_id}",
            #show_alert=True
        )
    elif (sufix == "edit") & (curent_channel_id != ""):
        await callback.message.answer(
                f"""
                Наберите текст и отправте{callback.message.message_id}"""
            )
        # await callback.message.edit_text(" ",
        #     inline_message_id = callback.message.message_id-2)

    elif (sufix == "create") & (curent_channel_id != ""):
        #Curent_Channal=cur_channal_admin(curent_channel_id)
        await callback.message.answer(
                f"""
        мы готовы приступить к работе\n\nдля создания поста.\n
    отправьте боту то, что хотите опубликовать. Это может быть всё, что угодно – текст, фото, видео, даже
     стикеры.{callback.message.message_id}""",
        )

    elif (sufix == "delete") & (curent_channel_id != ""):
        await callback.message.answer(
                f"""
        вы хотите удалить текущий пост?\n
        """,
        reply_markup= InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подтвердите', callback_data=f'repost_okdelete_{curent_channel_id}')],
        ])
        )
    elif (sufix == "okdelete") & (sufix_full[2] != None):
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-4 )
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-3 )
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-2 )
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-1 )
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id )

        await callback.message.answer(
            f""" ` _ _ ~ Сообщения удалены. Можно продолжать. ~ _ _ `
                """,
            reply_markup=get_inline_keyboard2() ,

                )
    elif (sufix == "continue") & (curent_channel_id != ""):
        #print(message.message_id)
        await callback.message.answer(
                f"""
        Текущий пост готов к публикации в канал: {Curent_Channal["username_channel"]}\n@{Curent_Channal["username_channel"]}
        """
                )
        await bot_post.copy_message(callback.message.chat.id, callback.message.chat.id, callback.message.message_id-1, reply_markup=get_inline_keyboard3(curent_channel_id))
        await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-2 )
        #await bot_post.delete_message(callback.message.chat.id, callback.message.message_id )
        await callback.answer()


    elif (sufix == "Send") & (curent_channel_id != None):
        #curent_chat_id = callback.data.split("_")[1]
        #print(693, curent_channel_id, callback.message.message_id)
        await callback.message.copy_to(curent_channel_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[]))
        await callback.message.answer(
            text="~ Сообщение успешно отправлено в канал! ~",
            #show_alert=True
            reply_markup= InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔙 Вернуться', callback_data=f'Continue_start_{curent_channel_id}')], 
            ])
        )
        Curent_Channal={}
        #print(699,Curent_Channal, curent_channel_id)




##**********************************обработчик
# @m_router.message(F.message)  # Echo to all messages except messages via bot
# async def echo_all(message: Message, base_url: str=base_url):
#     print(582,message.text, 777, Ch_id)

# @m_router.callback_query()
# async def hengler_post(callback: CallbackQuery):
#     await callback.answer(
#         "Получил ---- callback_query",
#         show_alert=True
#     )

@m_router.message(~F.message & ((F.text != "Настройки") & (F.text != "Заметки") & (F.text != "Контент-план") & (F.text != "Статистика")))  # Echo to all messages except messages via bot
async def echo_all(message: Message):
    global Curent_Channal
    global Create_message_id
    global message2
    #*********************************************************************
    data = {
        "url": "<N/A>",
        "email": "<N/A>",
        "code": "<N/A>"
    }
    entities1 = message.entities or []
    for item in entities1:
        if item.url != None:
            data[item.url] = item.extract_from(message.text)
    #**********************************************************

    #print(538,Curent_Channal, 999, data)
    # await message.edit_text(" ",
    #     inline_message_id = message.message_id)
    if message.text != None :
        Create_message_id.append(str(message.message_id))
        #Create_message_id.append(message.text)
        message2 = message #await message.send_copy(Ch_id)
        print("прилетело сюда", message.message_id)
        #await bot_post.delete_message(Ch_id, message.message_id-1 )

        await message.answer(
            message.text,
            reply_markup=get_inline_keyboard_creat(Curent_Channal["id_channel"])
        )

    elif (message.photo != None) & (message.text == None):
        #await show_summary(message=message, data=[id_channel, id_channel_source, forward_mess_id])
        #with suppress(TelegramBadRequest):
        #await bot_post.copy_message(Ch_id)
        #message2: Message =await message.send_copy(Ch_id)
        new_text=f"{message.message_id}" + str(message2.text)
        file_io: BinaryIO = await bot_post.download(message.photo[-2].file_id)
        url_link_image=upload_image_in_telegraph(file_io)
        #print(697, message.message_id, ) #/file/25b93f3a42027f16c107f.jpg

        entities= [MessageEntity(type='text_link', offset=0, length=1, url=f"https://telegra.ph{url_link_image}", user=None, language=None, custom_emoji_id=None)] #MessageEntity(type='bold', offset=2, length=53, url=None, user=None, language=None, custom_emoji_id=None), MessageEntity(type='italic', offset=320, length=5, url=None, us f'https://telegra.ph/file/{message.photo[-1].file_id}9f0d8.png', user=None, language=None, custom_emoji_id=None)

        await message.answer(text=new_text, entities=entities, disable_web_page_preview=False, reply_markup=get_inline_keyboard_creat(Curent_Channal["id_channel"]))
        #await message.answer(text=Create_message_id[1], photo= message.photo[-1].file_id, caption=message.caption, caption_entities=message.caption_entities, reply_markup=get_inline_keyboard(Create_message_id[0]))

    elif message.animation != None :
        # with suppress(TelegramBadRequest):
        await message.answer_animation(message.animation.file_id, caption=message.caption, caption_entities=message.caption_entities, reply_markup=get_inline_keyboard(Curent_Channal["id_channel"]))
    elif (message.text != None) & (message.entities.url != None):

        #print(756, Curent_Channal["Create_message_id"], message.message_id)
        await bot_post.delete_message(chat.id, message.message_id-1 )

        await message.answer(
            message.text,
            reply_markup=get_inline_keyboard_creat(Curent_Channal["id_channel"])
        )



    # await message.answer(
    #     "Эти функции пока не работают,\nт. к. находятся в разработке!",
    #     reply_markup= InlineKeyboardMarkup(inline_keyboard=[
    #     [InlineKeyboardButton(text='🔙 Вернуться', callback_data=f'Continue_start')], 
    #     ])
    # )

#**************************************************************************
@m_router.message(((F.text == "Настройки") | (F.Command == "settings"))) #(commands=["settings"])))  
async def handler_settings(message: Message, base_url: str=base_url):
    k_id=await bot_post.get_me()
    #result: List[Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned]] = await bot_post.get_chat_administrators("1849731160")
    await message.answer(
       f"""Вы находитесь в разделе общих настроек.\nВыберите, что хотите настроить.\nЕсли что-то непонятно,\nотправьте команду
/help\n\u200b """,
        # reply_markup=InlineKeyboardMarkup(
        # inline_keyboard=[[InlineKeyboardButton(text="Создать ст"), InlineKeyboardButton(text="план")],
        # [InlineKeyboardButton(text="Изменить пост"), InlineKeyboardButton(text="Статика")],
        #  [InlineKeyboardButton(text="Заети"), InlineKeyboardButton(text="Настки")]],
        #  ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
            [InlineKeyboardButton(text='Мои каналы', callback_data=f'settings_mychannels_'), 
            InlineKeyboardButton(text='Добавить канал', callback_data=f'settings_addchannel_')], 

            [InlineKeyboardButton(text='🔙 Вернуться', callback_data=f'Continue_start_')], 
            ]
        ),
    )

@m_router.callback_query(Text(startswith="settings_"))
async def run_settings(callback: CallbackQuery):
    sufix_full=callback.data.split("_")
    sufix = callback.data.split("_")[1]
    #Curent_channel=has_channel(Ch_id, id_channel=sufix_full[2] if sufix_full[2] != None else None)
    #cur_channal_admin(Curent_channel)
    global List_data_channel_admin
    if List_data_channel_admin == []:
        List_data_channel_admin= inicialisiren_bot(callback.message.chat.id, True)
    #     return
    global Curent_Channal
    curent_channel_id=sufix_full[2] if sufix_full[2] != "" else ""
    #print(802, Curent_Channal, sufix_full[2], Ch_id)
    username_channel=[]
    id_channel=[]
    if ((sufix == "clone") & (curent_channel_id == "")) | ((sufix == "create") & (curent_channel_id == "")):
        return
    elif sufix == "settings":
        await handler_settings(callback.message) 
    elif (sufix == "addchannel"):
        #idm=await bot_post.send_message(Ch_id, "addchannel_")
        # await idm.forward(Ch_id)
        # await bot_post.delete_message(callback.message.chat.id, callback.message.message_id-2 )
        await command_addchannel(callback.message)
        #await callback.message.answer()
    elif (sufix == "mychannels"):

        curent_channel1=List_data_channel_admin[0]["username_channel"] or ""
        curent_channel2=List_data_channel_admin[len(List_data_channel_admin)-2]["username_channel"] if len(List_data_channel_admin) > 1 else ""
        curent_channel3=List_data_channel_admin[len(List_data_channel_admin)-1]["username_channel"] if len(List_data_channel_admin) > 2 else ""
        await callback.message.answer(
            f"""У вас подключены следующие каналы: @{curent_channel1},\n@{curent_channel2},\n@{curent_channel3},\n они в списке администрируемых каналов. 
                """,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
            [InlineKeyboardButton(text='🔙 Вернуться', callback_data= "settings_settings_" )], 
            ]
        ),
                )

#***********************************************

# app = FastAPI(title=settings.APP_TITLE)

# @app.on_event("startup")
# async def startup():
#     try:
#         useful_updates = _dispatcher.resolve_used_update_types()
#             # Да, этот метод можно вызвать даже если у вас поллинг
#         await _dispatcher.start_polling(bot_post, allowed_updates=useful_updates)
#     except Exception as e:
#         raise e

# @app.on_event("shutdown")
# async def shutdown():
# #    await db.disconnect()
#     await bot.session.close()

async def run_bot2_backgraund():
    useful_updates = _dispatcher.resolve_used_update_types()
#     # Запускаем бота и пропускаем все накопленные входящие
#     # Да, этот метод можно вызвать даже если у вас поллинг
#     #await bot_post.delete_webhook(drop_pending_updates=True)
    await _dispatcher.start_polling(bot_post, allowed_updates=useful_updates)
#run_bot2_backgraund()
#6157538942:AAH9jbktrh2HabWQdrqxAvS7QTwQ3NV2NCU

if __name__ == '__main__':
    # uvicorn.run(
    #     app="main:app",
    #     host=settings.ALLOWED_HOST,
    #     debug=settings.DEBUG,
    #     port=settings.ALLOWED_PORT,
    #     reload=True,
    #     #log_level=logging.INFO,
    #     use_colors=True,
    # )

#***********************************************************
    asyncio.run(run_bot2_backgraund())
