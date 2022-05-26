from os import system 
system("pip3 install -U amino.fix pip")
from keep_alive import keep_alive
keep_alive()
import amino
#from amino import client
from alice import chatbot
from BotAmino import BotAmino
import sys
import threading
from threading import Thread
import os
import urllib
import string
from hashlib import sha1
import time
import base64
from uuid import uuid4
from io import BytesIO
import requests
import json
from gtts import gTTS, lang
from contextlib import suppress
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from unicodedata import normalize
from string import punctuation
from random import uniform, choice, randint
from youtube_dl import YoutubeDL
from google_trans_new import google_translator
from constant import LANGUAGES,DEFAULT_SERVICE_URLS
from json import dumps, load
import random
from joke.jokes import *

path_utilities = "utilities"
path_download = "audio"
path_lock = f"{path_utilities}/locked"

client = BotAmino("oaz7zgj9oa@vddaz.com","indian4321")
client.prefix = "/"


def print_exception(exc):
    print(repr(exc))


def nope(data):
    return False

def is_it_me(data):
    return data.authorId in ('ba6b54f2-29fa-4917-bdf1-70e7c6e28ded')

def is_staff(data):
    return data.authorId in ('ba6b54f2-29fa-4917-bdf1-70e7c6e28ded') or data.subClient.is_in_staff(data.authorId)

def join_community(comId: str = None, inv: str = None):
    if inv:
        try:
            client.client.request_join_community(comId=comId, message='Hello everyone!!')
            return True
        except Exception as e:
            print_exception(e)
    else:
        try:
            client.client.join_community(comId=comId, invitationId=inv)
            return True
        except Exception as e:
            print_exception(e)

@client.command(condition=is_it_me)
def joinamino(args):
    invit = None
    if client.len_community >= 20 and not (is_it_me(authorId)
    or
    is_it_admin(authorId)):
        args.subClient.send_message(args.chatId, "The bot has joined too many communities!")
        return

    staff = args.subClient.get_staff(args.message)
    if not staff:
        args.subClient.send_message(args.chatId, "Wrong amino ID!")
        return

    try:
        test = args.message.strip().split()
        amino_c = test[0]
        invit = test[1]
        invit = invit.replace("http://aminoapps.com/invite/", "")
    except Exception:
        amino_c = args.message
        invit = None

    try:
        val = args.subClient.client.get_from_code(f"http://aminoapps.com/c/{amino_c}")
        comId = val.json["extensions"]["community"]["ndcId"]
    except Exception:
        val = ""

    isJoined = val.json["extensions"]["isCurrentUserJoined"]
    if not isJoined:
    	join_community(comId, invit)
    	val = client.get_from_code(f"http://aminoapps.com/c/{amino_c}")
    	isJoined = val.json["extensions"]["isCurrentUserJoined"]
    	if isJoined:
    	       Thread(target=client.threadLaunch, args=[comId, True]).start() 
    	       auth = client.get_community(comId).get_user_info(args.authorId).nickname 
    	       client.get_community(comId).ask_amino_staff(f"Hello! I am a bot and i can do a lot of stuff!\nI've been invited here by {auth}.\nIf you need help, you can do !help.\nEnjoy^^") 
    	       args.subClient.send_message(args.chatId, "Joined!") 
    	       return 
    	       args.subClient.send_message(args.chatId, "Waiting for join!")
    	       return
    else:
        args.subClient.send_message(args.chatId, "Allready joined!")
        return

    args.subClient.send_message(args.chatId, "Something went wrong!")

@client.command()
def cb(data):
    message=('data.message')
    chatbot_ai=chatbot()
    response=chatbot_ai.text(message)
    message = {
        'chatId': data.chatId,
        'message': f"{response}",
        'replyTo': data.messageId
    }
    data.subClient.send_message(**message)

@client.command()
def frame(data):
	data.subClient.subclient.apply_avatar_frame(avatarId=data.message, applyToAll= True)

@client.command(condition=is_staff)
def chatbubbles(args):
	args.subClient.send_message(args.chatId, f"""Select the chatbubbles:
1. pictureframe 
2. neon""")

@client.command(condition=is_staff)
def pictureframe(data):
    bubble = "f83337a0-4383-4935-bb09-633dc29f89d3"
    data.subClient.apply_bubble(chatId=data.chatId, bubbleId=bubble, applyToAll=True)

@client.command(condition=is_staff)
def neon(data):
    bubble = "817c94af-9311-4856-b0a2-f02c031a09f5"
    data.subClient.apply_bubble(chatId=data.chatId, bubbleId=bubble, applyToAll=True)

@client.command()
def startvc(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    client.start_vc(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
    data.subClient.send_message(data.chatId, "Started Vc!")

@client.command()
def endvc(data):
      data.subClient.delete_message(data.chatId, data.messageId) 
      client.end_vc(comId=data.subClient.community_id,chatId=data.chatId,joinType=2) 
      data.subClient.send_message(data.chatId, "Ended Vc!")

@client.command()
def startsc(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    client.start_screen_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
    data.subClient.send_message(data.chatId, "Started Screening!")

@client.command()
def endsc(data):
      data.subClient.delete_message(data.chatId, data.messageId) 
      client.end_voice_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=2) 
      data.subClient.send_message(data.chatId, "Ended Screening!")

@client.command()
def notifyall(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    users = data.subClient.get_online_users(start=0, size=1000)
    for user in users.profile.userId:
        data.subClient.live_notify(chatId=data.chatId,userId=user)
        data.subClient.send_message(chatId=data.chatId,message=f"[ic]Notified to all gc members")
        return True

@client.command()
def inviteall(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    users = data.subClient.get_all_users(start=0, size=1000)
    for user in users.profile.userId:
        data.subClient.invite_to_vc(chatId=data.chatId,userId=user)
        data.subClient.send_message(chatId=data.chatId,message=f"[ic]Invited all Users in gc")
        return True

@client.command()
def pvp(data):
    import time
    msg = data.message + " null null "
    msg = msg.split(" ")
    try:
        rounds = int(msg[0])
    except (TypeError, ValueError):
        rounds = 5
        msg[2] = msg[1]
        msg[1] = msg[0]
        msg[0] = 5

    if msg[1] == '' or msg[1] == ' ' or msg[1] == 'null':
        msg[1] = data.author
    if msg[2] == '' or msg[1] == ' ' or msg[2] == 'null':
        msg[2] = data.author
    if msg[1] == msg[2]:
        msg[2] = f'Reverse_{msg[1]}'

    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message=f"[icu]{data.author} started a PvP."
                                                                    f"\n[ci]{msg[1]} ⚔ {msg[2]}"
                                                                    f'\n[ci]May the best win!')
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)
    win1 = 0
    win2 = 0
    round = 0
    for tpvp in range(0, rounds):
        round = round + 1
        punch = randint(0, 1)
        if punch == 0:
            win1 = win1 + 1
            agress = msg[1]
            defens = msg[2]
        else:
            win2 = win2 + 1
            agress = msg[2]
            defens = msg[1]
        time.sleep(4)
        while True:
            try:
                data.subClient.send_message(chatId=data.chatId, message=f"[cu]Round {round}"
                                                                        f"\n[ci]{msg[1]} ⚔ {msg[2]}"
                                                                        f"\n[ic] {agress} destroyed {defens}!")
                break
            except:
                print(f"Error... Retrying in 5 seconds")
                time.sleep(5)
    while True:
        try:
            if win1 > win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[bcu]{msg[1]} has won!"
                                                                        f"\n[ciu][{win1} x {win2}]")
            elif win1 < win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[bcu]{msg[2]} has won!"
                                                                        f"\n[cic][{win1}x{win2}]")
            elif win1 == win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[iC]Tie.")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command(condition=is_it_me)
def leaveamino(args):
    args.subClient.send_message(args.chatId, "Leaving the amino!")
    args.subClient.stop_instance()
    args.subClient.leave_amino()

def extra(uid : str):
    event=uuid4()
    data = {
        "reward":{"ad_unit_id":"255884441431980_807351306285288","credentials_type":"publisher","custom_json":{"hashed_user_id":f"{uid}"},"demand_type":"sdk_bidding","event_id":f"{event}","network":"facebook","placement_tag":"default","reward_name":"Amino Coin","reward_valid":"true","reward_value":2,"shared_id":"dc042f0c-0c80-4dfd-9fde-87a5979d0d2f","version_id":"1569147951493","waterfall_id":"dc042f0c-0c80-4dfd-9fde-87a5979d0d2f"},
        "app":{"bundle_id":"com.narvii.amino.master","current_orientation":"portrait","release_version":"3.4.33567","user_agent":"Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)"},"date_created":1620295485,"session_id":"49374c2c-1aa3-4094-b603-1cf2720dca67","device_user":{"country":"US","device":{"architecture":"aarch64","carrier":{"country_code":602,"name":"Vodafone","network_code":0},"is_phone":"true","model":"GT-S5360","model_type":"Samsung","operating_system":"android","operating_system_version":"29","screen_size":{"height":2260,"resolution":2.55,"width":1080}},"do_not_track":"false","idfa":"7495ec00-0490-4d53-8b9a-b5cc31ba885b","ip_address":"","locale":"en","timezone":{"location":"Asia\/Seoul","offset":"GMT+09:00"},"volume_enabled":"true"}
        }

    headers={
        "cookies":"__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096",
        "authorization":"Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA=="
    }
    requests.post("https://ads.tapdaq.com/v4/analytics/reward",json=data, headers=headers)

@client.command()
def tap(args):
  args.subClient.send_message(args.chatId,"Done")
  for _ in range(140):
    threading.Thread(target=extra(args.authorId))

@client.command("title")
def title(args):
    if client.check(args, 'staff', id_=client.botId):
        try:
            title, color = args.message.split("color=")
            color = color if color.startswith("#") else f'#{color}'
        except Exception:
            title = args.message
            color = None

        if args.subClient.add_title(args.authorId, title, color):
            args.subClient.send_message(args.chatId, f"The titles of {args.author} has changed")

@client.command("ship")
def ship(data):
    couple = data.message + " null null "
    people = couple.split(" ")
    percentage = uniform(0, 100)
    quote = ' '
    if percentage <= 10:
        quote = 'No way.'
    elif 10 <= percentage <= 25:
        quote = 'Eh...'
    elif 25 <= percentage <= 50:
        quote = 'Maybe one day?'
    elif 50 <= percentage <= 75:
        quote = 'My couple ❤'
    elif 75 <= percentage <= 100:
        quote = 'Top couple'
    data.subClient.send_message(chatId=data.chatId, message=f"{people[0]} x {people[1]} has {percentage:.2f}% "
                                                            f"of chance to work.")
    data.subClient.send_message(chatId=data.chatId, message=quote)
    value = int(''.join(open("value", 'r').readlines()))
    value = value + 1
    print(value)

@client.command(condition=is_staff)
def prefix(args):
    if args.message:
        args.subClient.set_prefix(args.message)
        args.subClient.send_message(args.chatId, f"prefix set as {args.message}")

@client.command()
def rainbow(data):
    url = f"https://some-random-api.ml/canvas/gay/?avatar={data.info.message.author.icon}"
    file = upload(url)

    data.subClient.send_message(chatId=data.chatId, embedTitle="A rainbow overlay",file=file, fileType="image")

@client.command("follow")
def follow(args):
    args.subClient.follow_user(args.authorId)
    args.subClient.send_message(args.chatId, "Now following you!")

@client.command("unfollow")
def unfollow(args):
    args.subClient.unfollow_user(args.authorId)
    args.subClient.send_message(args.chatId, "Unfollow!")

@client.command(condition=is_it_me)
def stopamino(args):
    args.subClient.stop_instance()
    del client[args.subClient.community_id]

def deviceaoss():
    return requests.get("https://aminohub.sirlez.repl.co/deviceId").text
device=deviceaoss()

@client.command()
def deviceid(data):
     genids = deviceaoss()
     data.subClient.send_message(data.chatId, message=genids)

@client.command(condition=is_staff)
def name(data):
	data.subClient.edit_profile(nickname=data.message)
	data.subClient.send_message(chatId=data.chatId,message=f"name changed to {data.message}")

@client.command(condition=is_staff)
def vm(data):
    id = data.subClient.get_chat_threads(start=0, size=40).chatId
    for chat in id:
        #with suppress(Exception):
            data.subClient.edit_chat(chatId=chat, viewOnly=True)

@client.command(condition=is_staff)
def unvm(data):
    id = data.subClient.get_chat_threads(start=0, size=40).chatId
    for chat in id:
        with suppress(Exception):
            data.subClient.edit_chat(chatId=chat, viewOnly=False)

def telecharger(url):
    music = None
    if ("=" in url and "/" in url and " " not in url) or ("/" in url and " " not in url):
        if "=" in url and "/" in url:
            music = url.rsplit("=", 1)[-1]
        elif "/" in url:
            music = url.rsplit("/")[-1]

        if music in os.listdir(path_download):
            return music

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            'extract-audio': True,
            'outtmpl': f"{path_download}/{music}.webm",
            }

        with YoutubeDL(ydl_opts) as ydl:
            video_length = ydl.extract_info(url, download=True).get('duration')
            ydl.cache.remove()

        url = music+".mp3"

        return url, video_length
    return False, False


def decoupe(musical, temps):
    size = 170
    with open(musical, "rb") as fichier:
        nombre_ligne = len(fichier.readlines())

    if temps < 180 or temps > 540:
        return False

    decoupage = int(size*nombre_ligne / temps)

    t = 0
    file_list = []
    for a in range(0, nombre_ligne, decoupage):
        b = a + decoupage
        if b >= nombre_ligne:
            b = nombre_ligne

        with open(musical, "rb") as fichier:
            lignes = fichier.readlines()[a:b]

        with open(musical.replace(".mp3", "PART"+str(t)+".mp3"),  "wb") as mus:
            for ligne in lignes:
                mus.write(ligne)

        file_list.append(musical.replace(".mp3", "PART"+str(t)+".mp3"))
        t += 1
    return file_list


@client.command()
def play(args):
    music, size = telecharger(args.message)
    if music:
        music = f"{path_download}/{music}"
        val = decoupe(music, size)

        if not val:
            try:
                with open(music, 'rb') as fp:
                    args.subClient.send_message(args.chatId, file=fp, fileType="audio")
            except Exception:
                args.subClient.send_message(args.chatId, "Error! File too heavy (9 min max)")
            os.remove(music)
            return

        os.remove(music)
        for elem in val:
            with suppress(Exception):
                with open(elem, 'rb') as fp:
                    args.subClient.send_message(args.chatId, file=fp, fileType="audio")
            os.remove(elem)
        return
    args.subClient.send_message(args.chatId, "Error! Wrong link")

@client.command(condition=is_staff)
def join(args):
    val = args.subClient.join_chatroom(args.message, args.chatId)
    if val or val == "":
        args.subClient.send_message(args.chatId, f"Chat {val} joined".strip())
    else:
        args.subClient.send_message(args.chatId, "No chat joined")
        
@client.command(condition=is_staff)
def leave(args):
    if args.message:
        chat_ide = args.subClient.get_chat_id(args.message)
        if chat_ide:
            args.chatId = chat_ide
    args.subClient.leave_chat(args.chatId)

@client.command("block", False)
def block(args):
    val = args.subClient.get_user_id(args.message)
    if val:
        args.subClient.client.block(val[1])
        args.subClient.send_message(args.chatId, f"User {val[0]} blocked!")

@client.command("unblock", False)
def unblock(args):
    val = args.subClient.client.get_blocked_users()
    for aminoId, userId in zip(val.aminoId, val.userId):
        if args.message in aminoId:
            args.subClient.client.unblock(userId)
            args.subClient.send_message(args.chatId, f"User {aminoId} unblocked!")

@client.command(condition=is_staff)
def gethost(data):
	data.subClient.transfer_host(data.chatId,userIds=[client.userId])
	info=data.subClient.get_chat_thread(data.chatId)
	x=info.json['extensions']['organizerTransferRequest']['requestId']
	data.subClient.accept_organizer(chatId=data.chatId,requestId=x)
	data.subClient.send_message(data.chatId,message="Host changed")

@client.command()
def accept(args):
    if args.subClient.accept_role(args.chatId):
        args.subClient.send_message(args.chatId, "Accepted!")
        return
    val = args.subClient.get_notices(start=0, size=25)
    for elem in val:
        print(elem["title"])

    res = None

    for elem in val:
        if 'become' in elem['title'] or "host" in elem['title']:
            res = elem['noticeId']

        if res and args.subClient.accept_role(res):
            args.subClient.send_message(args.chatId, "Accepted!")
            return
    else:
        args.subClient.send_message(args.chatId, "Error!")

@client.command("announce")
def announce(args):
    if client.check(args,'staff',):
    	try:
    		val = args.subClient.get_chats()
    		#val1=args.subClient.get_chats().titl
    		val3=args.subClient.get_chat_thread(args.chatId).title
    		for g, in zip(val.chatId):
    			args.subClient.send_message(chatId=g,message=f"""

{args.message}""")

    	except Exception:
    		  	args.subClient.send_message(args.chatId,message=f"""
Finished Announcement
""")

@client.command(condition=is_it_me)
def ask(args):
    lvl = ""
    boolean = 1
    if "lvl=" in args.message:
        lvl = args.message.rsplit("lvl=", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl="+lvl, "").strip()
    elif "lvl<" in args.message:
        lvl = args.message.rsplit("lvl<", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl<"+lvl, "").strip()
        boolean = 2
    elif "lvl>" in args.message:
        lvl = args.message.rsplit("lvl>", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl>"+lvl, "").strip()
        boolean = 3
    try:
        lvl = int(lvl)
    except ValueError:
        lvl = 20

    args.subClient.ask_all_members(args.message+f"\n[CUI]This message was sent by {args.author}\n[CUI]I am a bot and have a nice day^^", lvl, boolean)
    args.subClient.send_message(args.chatId, "Asking...")

@client.command("askstaff", False)
def ask_staff(args):
    amino_list = client.client.sub_clients()
    for commu in amino_list.comId:
        client[commu].ask_amino_staff(message=args.message)
    args.subClient.send_message(args.chatId, "Asking...")

@client.command("lock", is_staff)
def lock_command(args):
    if not args.message or args.message in args.subClient.locked_command or args.message not in client.commands_list() or args.message in ("lock", "unlock"):
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.add_locked_command(args.message)
    args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("unlock", is_staff)
def unlock_command(args):
    if args.message:
        try:
            args.message = args.message.lower().strip().split()
        except Exception:
            args.message = [args.message.lower().strip()]
        args.subClient.remove_locked_command(args.message)
        args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("llock")
def locked_command_list(args):
    val = ""
    if args.subClient.locked_command:
        for elem in args.subClient.locked_command:
            val += elem+"\n"
    else:
        val = "No locked command"
    args.subClient.send_message(args.chatId, val)

@client.command("alock")
def admin_lock_command(args):
    if client.check(args, 'me', 'admin'):
        if not args.message or args.message not in client.get_commands_names() or args.message == "alock":
            return

        command = args.subClient.admin_locked_command
        args.message = [args.message]

        if args.message[0] in command:
            args.subClient.remove_admin_locked_command(args.message)
        else:
            args.subClient.add_admin_locked_command(args.message)

        args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("allock")
def locked_admin_command_list(args):
    if client.check(args, 'me', 'admin'):
        val = ""
        if args.subClient.admin_locked_command:
            for elem in args.subClient.admin_locked_command:
                val += elem+"\n"
        else:
            val = "No locked command"
        args.subClient.send_message(args.chatId, val)

@client.command("mention")
def mention(args):
    try:
        size = int(args.message.strip().split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        size = 1

    val = args.subClient.get_user_id(args.message)
    if not val:
        args.subClient.send_message(chatId=args.chatId, message="Username not found")
        return

    if size > 5:
        size = 5

    if val:
        for _ in range(size):
            with suppress(Exception):
                args.subClient.send_message(chatId=args.chatId, message=f"‎‏‎‏@{val[0]}‬‭", mentionUserIds=[val[1]])
                
@client.command("msg")
def msg(args):
    value = 0
    size = 1
    ment = None
    with suppress(Exception):
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True, reason="Clear")

    if "chat=" in args.message:
        chat_name = args.message.rsplit("chat=", 1).pop()
        chat_ide = args.subClient.get_chat_id(chat_name)
        if chat_ide:
            args.chatId = chat_ide
        args.message = " ".join(args.message.strip().split()[:-1])

    try:
        size = int(args.message.split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        size = 0

    try:
        value = int(args.message.split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        value = size
        size = 1

    if not args.message and value == 1:
        args.message = f"‎‏‎‏@{args.author}‬‭"
        ment = args.authorId

    if size > 10:
        size = 10

    for _ in range(size):
        with suppress(Exception):
            args.subClient.send_message(chatId=args.chatId, message=f"{args.message}", messageType=value, mentionUserIds=ment)

@client.command()
def check(args):
	args.subClient.send_message(args.chatId, f"--Bot is Online--")

@client.command()
def ghost(args):
      args.subClient.delete_message(args.chatId, args.messageId) 
      args.subClient.send_message(chatId=args.chatId, message=f"{args.message}", messageType=109)

@client.command()
def gspam(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    qte = args.message.rsplit(" ", 1)
    msg, quantity= qte[0], qte[1]
    quantity = 1 if not quantity.isdigit() else int(quantity)
    quantity = 100 if quantity > 100 else quantity

    for _ in range(quantity):
        args.subClient.send_message(args.chatId, msg, messageType=109)

@client.command("mentionco")
def mentionco(data):
    hostlist = data.subClient.get_chat_thread(data.chatId).coHosts
    msg = 'Co-Hosts:\n'
    for item in hostlist:
        n = data.subClient.get_user_info(str(item)).nickname
        msg += f'<$@{n}$>\n'
    data.subClient.send_message(chatId=data.chatId, message=msg, mentionUserIds=hostlist)
                        
@client.command("joke")
def joke(data):
    joke = [chucknorris(), icndb(), icanhazdad(), geek()]
    data.subClient.send_message(data.chatId, message=random.choice(joke))
    
@client.command("8ball")
def height_ball(data):
    ball= choice(["Yes", "No", "Maybe", "of course", "never", "i think so"])
    data.subClient.send_message(data.chatId, ball, replyTo = data.messageId)

@client.command("say")
def say_something(data):
    audio_file = f"{path_download}/ttp.mp3"
    gTTS(text=data.message, lang='hi', slow=False).save(audio_file)
    with open(audio_file, 'rb') as fp:
        data.subClient.send_message(data.chatId, file=fp, fileType="audio")
        os.remove(audio_file)

@client.command()
def prank(args, amt : int , nt = 1):
    with suppress(Exception):
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)

    tId = "0072dbf4-b4ad-4a58-a51c-39c463a67246"
    if args.message:
    	chat_ide = args.subClient.get_chat_id(args.message)
    	if chat_ide:
    		args.chatId = chat_ide
    	amt , nt = int(amt) , int(nt)
    	for _ in range(nt):
    		args.subClient.send_coins(coins=amt, chatId=args.chatId, transactionId=tId)

@client.command()
def bg(data):
    image = data.subClient.get_chat_thread(chatId=data.chatId).backgroundImage
    if image:
        filename = os.path.basename(image)
        urllib.request.urlretrieve(image, filename)
        with open(filename, 'rb') as fp:
            data.subClient.send_message(data.chatId, file=fp, fileType="image")
        os.remove(filename)

@client.command()
def bgi(data):
    image = data.subClient.get_chat_thread(chatId=data.chatId).icon
    if image:
        filename = os.path.basename(image)
        urllib.request.urlretrieve(image, filename)
        with open(filename, 'rb') as fp:
            data.subClient.send_message(data.chatId, file=fp, fileType="image")
        os.remove(filename)

@client.command()
def joinvc(data):
	client.join_voice_chat(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)

@client.command()
def joinsc(data):
	client.join_screen_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
  
@client.command()
def spam(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    qte = args.message.rsplit(" ", 1)
    msg, quantity= qte[0], qte[1]
    quantity = 1 if not quantity.isdigit() else int(quantity)
    quantity = 100 if quantity > 100 else quantity

    for _ in range(quantity):
        args.subClient.send_message(args.chatId, msg)
        
@client.command(condition=is_staff)
def clear(args):
    if client.check(args, 'staff', client.botId):
        try:
            size = int(args.message)
        except Exception:
            size = 1
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True, reason="Clear")

        if size > 99:
            size = 99

        messages = args.subClient.get_chat_messages(chatId=args.chatId, size=size).messageId

        for message in messages:
            args.subClient.delete_message(args.chatId, messageId=message, asStaff=True, reason="Clear")

@client.command("all")
def everyone(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    mention = [userId for userId in args.subClient.get_chat_users(chatId=args.chatId).userId]
    # test = "".join(["‎‏‎‏‬‭" for user in args.subClient.get_chat_users(chatId=args.chatId).userId])
    args.subClient.send_message(chatId=args.chatId, message=f"[iu]@everyone‎‏‎‏‬‭‎‏‎‏‬‭ {args.message}", mentionUserIds=mention)
    
@client.command()
def tr(args):
  data = args.subClient.get_message_info(chatId = args.chatId, messageId = args.messageId)
  reply_message = data.json['extensions']
  if reply_message:
    reply_message = data.json['extensions']['replyMessage']['content']
    reply_messageId = data.json['extensions']['replyMessage']['messageId']
    translator = google_translator() 
    detect_result = translator.detect(reply_message)[1]
    translate_text = translator.translate(reply_message)
    reply = "[IC]"+str(translate_text)+"\n\n[c]Translated Text from "+str(detect_result)
    print(reply)
    args.subClient.send_message(chatId=data.chatId,message=reply,replyTo=reply_messageId)

@client.command()
def gif(args):
  search = (args.message)
  with suppress(Exception):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
  response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=7G8jLZHM52O5YLJ0fPcBOawMvew5a1e1')
  # print(response.text)
  data = json.loads(response.text)
  gif_choice = randint(0, 9)
  image = data['data'][gif_choice]['images']['original']['url']
  print("URL",image)
  if image is not None:
    print(image)
    filename = image.split("/")[-1]
    urllib.request.urlretrieve(image, filename)
    with open(filename, 'rb') as fp:
        args.subClient.send_message(args.chatId, file=fp, fileType="gif")
        print(os.remove(filename))

@client.command("chatlist", condition=is_staff)
def get_chats(args):
    val = args.subClient.get_chats()
    for title, _ in zip(val.title, val.chatId):
        args.subClient.send_message(args.chatId, title)

@client.command("chatid")
def chat_id(args):
    val = args.subClient.get_chats()
    for title, chat_id in zip(val.title, val.chatId):
        if args.message.lower() in title.lower():
            args.subClient.send_message(args.chatId, f"{title} | {chat_id}")

@client.command(condition=is_staff)
def joinall(args):
    #if client.check(args, 'staff'):
        args.subClient.join_all_chat()
        args.subClient.send_message(args.chatId, "All chat joined")

@client.command(condition=is_staff)
def leaveall(args):
    args.subClient.send_message(args.chatId, "Leaving all chat...")
    args.subClient.leave_all_chats()

@client.command()
def sw(args):
    message = args.message.strip()
    val = message.replace("[C]", "[c]").replace("[c]", "\n[c]")
    val = val.replace("[I]", "[i]").replace("[i]", "\n[i]")
    val = val.replace("[U]", "[u]").replace("[u]", "\n[u]")
    val = val.replace("[S]", "[s]").replace("[s]", "\n[s]")
    val = val.replace("[B]", "[b]").replace("[b]", "\n[b]")
    val = val.replace("[CU]", "[cu]").replace("[cu]", "\n[cu]")
    val = val.replace("[BC]", "[bc]").replace("[bc]", "\n[bc]")

    args.subClient.set_welcome_message(val)
    args.subClient.send_message(args.chatId, "Welcome message changed")
     
@client.command("help")
def help(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]BoT Menu

➼ help           ➼ fun
➼ check        ➼ modonly
➼ chat""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("fun")
def fun(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]Fun Menu
➼say 
➼prank
➼gif
➼msg
➼dice
➼cb
➼quote
➼joke
➼play
➼rainbow
➼dictionary
➼tap 
➼global2
➼kill
➼slap
➼ship""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("modonly")
def modonly(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]Modonly Menu
➼name
➼block
➼unblock
➼ask
➼accept
➼leaveall
➼abw
➼rbw
➼spam
➼gethost""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command("chat")
def chat(data):
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message="""[BC]Chat Menu
➼startvc    ➼bgi
➼endvc      ➼restart
➼joinvc      ➼profile
➼startsc    ➼llock
➼joinsc      ➼mention
➼inviteall   ➼mentionco
➼notifyall   ➼deviceid
➼ghost       ➼pvp
➼tr               ➼follow
➼chatlist    ➼unfollow 
➼all             ➼bg
➼google    ➼global
➼join          ➼joinall""")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)
            
@client.command()
def dictionary(data):
    link = f"https://some-random-api.ml/dictionary?word={data.message}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['definition']
    data.subClient.send_message(chatId=data.chatId, message=f"{msg}")

@client.command()
def quote(data):
    var = "quote"
    link = f"https://some-random-api.ml/animu/{var}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['sentence']
    data.subClient.send_message(chatId=data.chatId, message=f"{msg}")
            
@client.command()
def google(data):
    msg = data.message.split(" ")
    msg = '+'.join(msg)
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message=f"https://www.google.com/search?q={msg}")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)
            
@client.command("global")
def globall(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
	   AID=client.get_user_info(userId=str(user)).aminoId
	   data.subClient.send_message(data.chatId,message="https://aminoapps.com/u/"+str(AID))
	   	 	   
@client.command("global2")
def globall(data):
	   id=client.get_from_code(data.message).objectId
	   AID=client.get_user_info(id).aminoId
	   data.subClient.send_message(data.chatId,message="https://aminoapps.com/u/"+str(AID))

@client.command("dice")
def dice(args):
    if not args.message:
        args.subClient.send_message(args.chatId, f"🎲 -{randint(1, 20)},(1-20)- 🎲")
    else:
        try:
            n1, n2 = map(int, args.message.split('d'))
            times = n1 if n1 < 20 else 20
            max_num = n2 if n2 < 1_000_000 else 1_000_000
            numbers = [randint(1, (max_num)) for _ in range(times)]

            args.subClient.send_message(args.chatId, f'🎲 -{sum(numbers)},[ {" ".join(map(str, numbers))}](1-{max_num})- 🎲')
        except Exception as e:
            print_exception(e)

@client.command("kill")
def kill(data):
			img=open("sword.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				response=requests.get(f"{h}")
				file=open(".aiyijhale.png","wb")
				file.write(response.content)
				file.close()
				img = Image.open("sword.png")
				img1 = Image.open(".aiyijhale.png").resize((175,175))
				img.paste(img1, (295,670))
				#img.paste(img1, (750,1250))
				img=img.save(".yihh3.png")
				imgg=open(".yihh3.png","rb")
				try:
					data.subClient.send_message(chatId=data.chatId,file=imgg,fileType="image")
				except:
					pass
					
@client.command("slap")
def slap(data):
			img=open("slap.png","rb")
			mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
			for user in mention:
				h=data.subClient.get_user_info(str(user)).icon
				n=data.subClient.get_user_info(userId=str(user)).nickname
				response=requests.get(f"{h}")
				file=open(".haas.png","wb")
				file.write(response.content)
				file.close()
				x=data.subClient.get_user_info(data.authorId).icon
				response=requests.get(f"{x}")
				file=open(".aie.png","wb")
				file.write(response.content)
				file.close()
				#img2 = Image.open(".aie.png")
				img = Image.open("slap.png") 
				img1 = Image.open(".haas.png").resize((250,250)) 
				img2= Image.open(".aie.png").resize((240,240))
				img.paste(img1, (850,350))
				img.paste(img2, (500,90))
				img=img.save(".ijs.png")
				imgg=open(".ijs.png","rb")
				try:
					data.subClient.send_message(chatId=data.chatId,file=imgg,fileType="image")
				except:
					pass

@client.command(condition=is_staff)
def abw(args):
    if not args.message or args.message in args.subClient.banned_words:
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.add_banned_words(args.message)
    args.subClient.send_message(args.chatId, "Banned word list updated")

@client.command(condition=is_staff)
def rbw(args):
    if not args.message:
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.remove_banned_words(args.message)
    args.subClient.send_message(args.chatId, "Banned word list updated")
        
@client.command("bwl")
def banned_word_list(args):
    val = ""
    if args.subClient.banned_words:
        for elem in args.subClient.banned_words:
            val += elem + "\n"
    else:
        val = "No words in the list"
    args.subClient.send_message(args.chatId, val)

@client.command("welcome", condition=is_staff)
def welcome_channel(args):
    args.subClient.set_welcome_chat(args.chatId)
    args.subClient.send_message(args.chatId, "Welcome channel set!")

@client.command("unwelcome", condition=is_staff)
def unwelcome_channel(args):
    args.subClient.unset_welcome_chat()
    args.subClient.send_message(args.chatId, "Welcome channel unset!")

@client.command(condition=is_it_me)
def restart(self):
  sys.argv
  sys.executable
  print("restarting")
  os.execv(sys.executable, ['python'] + sys.argv)

@client.command(condition=is_it_me)
def stop(args):
    args.subClient.send_message(args.chatId, "Stopping Bot")
    os.execv(sys.executable, ["None", "None"])

@client.command(condition=is_it_me)
def stopamino(args):
    args.subClient.stop_instance()
    del client[args.subClient.community_id]

link_list = ["https://amino.com/c/"]

@client.on_message()
def on_message(data):
    [data.subClient.delete_message(data.chatId, data.messageId, reason=f"{data.message}", asStaff=True) for elem in link_list if elem in data.message]

@client.event("on_chat_invite")
def on_chat_invite(data):
    try:
        commuId = data.json["ndcId"]
        subClient = client.get_community(commuId)
    except Exception:
        return

    args = Parameters(data, subClient)

    subClient.join_chatroom(chatId=args.chatId)
    subClient.send_message(args.chatId, f"Hello!\n[B]I am a bot, if you have any question ask a staff member!\nHow can I help you?\n(you can do {subClient.prefix}help if you need help)")

@client.command("profile")
def profileinfo(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
	   	repa = data.subClient.get_user_info(userId=str(user)).reputation
	   	lvl = data.subClient.get_user_info(userId=str(user)).level
	   	crttime = data.subClient.get_user_info(userId=str(user)).createdTime
	   	followers = data.subClient.get_user_achievements(userId=str(user)).numberOfFollowersCount
	   	profilchange = data.subClient.get_user_info(userId=str(user)).modifiedTime
	   	commentz = data.subClient.get_user_info(userId=str(user)).commentsCount
	   	posts = data.subClient.get_user_achievements(userId=str(user)).numberOfPostsCreated
	   	followed = data.subClient.get_user_info(userId=str(user)).followingCount
	   	sysrole = data.subClient.get_user_info(userId=str(user)).role
	   	h=data.subClient.get_user_info(userId=str(user)).nickname
	   	id=data.subClient.get_user_info(userId=str(user)).userId
	   	data.subClient.send_message(data.chatId, message=f"""
[CB]Profile Info
[C]┅┅┅┅┅┅┅༻❁༺┅┅┅┅┅┅┅
❖Nickname: {h}

❖UserId: {id}

❖Account created time: {crttime}

❖Last time the profile was changed: {profilchange}

❖Reputation points: {repa}

❖Account level: {lvl}

❖Number of posts created in the profile: {posts}

❖Number of comments on the profile wall: {commentz}

❖The number of people you follow: {followed}

❖Account followers: {followers}

❖Account number in system: {sysrole}
	""")

@client.on_member_join_chat()
def welcome(data):
    data.subClient.send_message(data.chatId, f'''♡    ∩_∩
 （„• ֊ •„)♡
 ┏━━∪∪━━━ღ❦ღ━━┓

[BC]❀❀✿✿❀❀✿✿❀❀✿✿❀❀
 ᕼOᒪᗩ ✿
[C]༄ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴄʜᴀᴛ
[C]༄ʀᴇᴀᴅ ᴀɴᴅ ғᴏʟʟᴏᴡ ᴛʜᴇ ɢᴄ ʀᴜʟᴇs
[C]༄ᴀɴᴅ ᴇɴᴊᴏʏ ʏᴏᴜʀ sᴛᴀʏ ʜᴇʀᴇ 
[C]༄ᴀɴᴅ ᴍᴀᴋᴇ ɴᴇᴡ ғʀɪᴇɴᴅs 

[BC]❀❀✿✿❀❀✿✿❀❀✿✿❀❀

                        ┗ღ❦ღ━━━━━━━━┛
                                            ヽ(‧ω‧`)ﾉ
                                                 |    |
                                                 UU
''', embedTitle=data.author,embedLink=f"ndc://user-profile/{data.authorId}", embedImage=upload(data.info.message.author.icon))
def upload(url):
    link = requests.get(url)
    result = BytesIO(link.content)
    return result

@client.on_member_leave_chat()
def goodbye(data):
    data.subClient.send_message(data.chatId, '''[BC]━❃❃❃┅━Rip━┅❃❃❃━
[C]「 OH NOO !! 」
[C]Someone has left 💀 the
[C]group chat.
[BC]━❃❃❃┅━Rip━┅❃❃❃━''')

client.launch("online")
print("ready")

def Root():
    j = 0
    while True:
        if j >= 300:
            client.close()
            print("socket close")
            client.start()
            print("socket start")
            j = 0
        j += 1
        time.sleep(1)
Root()